"""
FastAPI Backend — Sign Language Translator
==========================================
Endpoints:
  WS  /ws/predict          — real-time frame prediction via WebSocket
  POST /api/tts            — text-to-speech (returns MP3 bytes)
  GET  /api/signs          — list all supported signs
  GET  /api/health         — health check

Run:
  uvicorn app:app --host 0.0.0.0 --port 8000 --reload
"""

import os, io, json, base64, time, logging
from collections import deque
from typing import List

import cv2
import numpy as np
import mediapipe as mp
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from gtts import gTTS
import tensorflow as tf

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(levelname)s │ %(message)s")
log = logging.getLogger("slt")

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE       = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE, "data/sign_model.h5")
LABEL_PATH = os.path.join(BASE, "data/label_encoder.npy")
SIGNS_PATH = os.path.join(BASE, "data/signs.json")

# ── MediaPipe ─────────────────────────────────────────────────────────────────
mp_hands    = mp.solutions.hands
HANDS       = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6,
)

# ── Model loading (lazy, once) ────────────────────────────────────────────────
_model  = None
_labels: List[str] = []

def get_model():
    global _model, _labels
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            log.warning("Model file not found — running in DEMO mode")
            return None, []
        _model  = tf.keras.models.load_model(MODEL_PATH)
        _labels = list(np.load(LABEL_PATH, allow_pickle=True))
        log.info(f"Model loaded │ {len(_labels)} classes")
    return _model, _labels

# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(title="Sign Language Translator API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Helpers ───────────────────────────────────────────────────────────────────
SEQUENCE_LEN   = 30
CONF_THRESHOLD = 0.75          # minimum confidence to emit a prediction
COOLDOWN_SECS  = 1.2           # seconds between repeated identical predictions


def extract_keypoints(frame_bgr: np.ndarray) -> np.ndarray:
    """Run MediaPipe on one BGR frame → 63-d keypoint vector."""
    rgb     = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    results = HANDS.process(rgb)
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        return np.array([[lm.x, lm.y, lm.z] for lm in hand.landmark]).flatten()
    return np.zeros(63)


def decode_frame(b64_data: str) -> np.ndarray:
    """Decode a base64-encoded JPEG/PNG frame → BGR numpy array."""
    if "," in b64_data:
        b64_data = b64_data.split(",", 1)[1]
    raw   = base64.b64decode(b64_data)
    arr   = np.frombuffer(raw, dtype=np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return frame


# ── Per-connection state ──────────────────────────────────────────────────────
class PredictorState:
    def __init__(self):
        self.sequence: deque = deque(maxlen=SEQUENCE_LEN)
        self.last_sign: str  = ""
        self.last_time: float = 0.0


# ── WebSocket endpoint ────────────────────────────────────────────────────────
@app.websocket("/ws/predict")
async def ws_predict(websocket: WebSocket):
    await websocket.accept()
    model, labels = get_model()
    state         = PredictorState()
    log.info("WS │ client connected")

    try:
        while True:
            raw = await websocket.receive_text()

            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                continue

            # ── Decode frame ──────────────────────────────────────────────────
            frame = decode_frame(msg.get("frame", ""))
            if frame is None:
                continue

            keypoints = extract_keypoints(frame)
            state.sequence.append(keypoints)

            response = {"type": "keypoints", "hand_detected": bool(keypoints.any())}

            # ── Predict once we have a full sequence ──────────────────────────
            if len(state.sequence) == SEQUENCE_LEN and model is not None:
                seq_arr = np.expand_dims(list(state.sequence), axis=0)   # (1,30,63)
                probs   = model.predict(seq_arr, verbose=0)[0]
                top_idx = int(np.argmax(probs))
                conf    = float(probs[top_idx])

                if conf >= CONF_THRESHOLD:
                    sign = labels[top_idx]
                    now  = time.time()
                    new  = (sign != state.last_sign) or \
                           (now - state.last_time > COOLDOWN_SECS)

                    if new:
                        state.last_sign = sign
                        state.last_time = now
                        response.update({
                            "type":       "prediction",
                            "sign":       sign,
                            "confidence": round(conf * 100, 1),
                            "top5": [
                                {"sign": labels[i], "prob": round(float(probs[i]) * 100, 1)}
                                for i in np.argsort(probs)[::-1][:5]
                            ],
                        })
                    else:
                        response.update({"type": "hold", "sign": sign})
                else:
                    response.update({"type": "low_conf", "confidence": round(conf * 100, 1)})

            elif model is None:
                # Demo mode — cycle through signs for testing UI
                import random
                demo_signs = ["hello", "yes", "no", "thankyou", "iloveyou"]
                if len(state.sequence) % 30 == 0:
                    response.update({
                        "type": "prediction",
                        "sign": random.choice(demo_signs),
                        "confidence": round(random.uniform(82, 99), 1),
                        "top5": [],
                        "demo": True,
                    })

            await websocket.send_text(json.dumps(response))

    except WebSocketDisconnect:
        log.info("WS │ client disconnected")
    except Exception as e:
        log.error(f"WS │ error: {e}")
        await websocket.close()


# ── TTS endpoint ──────────────────────────────────────────────────────────────
class TTSRequest(BaseModel):
    text: str
    lang: str = "en"
    slow: bool = False


@app.post("/api/tts")
async def text_to_speech(req: TTSRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="text cannot be empty")

    buf = io.BytesIO()
    tts = gTTS(text=req.text.strip(), lang=req.lang, slow=req.slow)
    tts.write_to_fp(buf)
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline; filename=speech.mp3"},
    )


# ── Signs list ────────────────────────────────────────────────────────────────
@app.get("/api/signs")
async def list_signs():
    _, labels = get_model()
    if labels:
        return {"signs": labels, "count": len(labels)}

    # fallback: read signs.json
    if os.path.exists(SIGNS_PATH):
        with open(SIGNS_PATH) as f:
            signs = json.load(f)
        return {"signs": signs, "count": len(signs)}

    return {"signs": [], "count": 0}


# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/api/health")
async def health():
    _, labels = get_model()
    return {
        "status":       "ok",
        "model_loaded": _model is not None,
        "sign_count":   len(labels),
        "version":      "2.0.0",
    }


# ── Entry ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
