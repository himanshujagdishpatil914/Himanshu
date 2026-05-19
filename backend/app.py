"""
FastAPI Backend — Sign Language Translator
==========================================
Endpoints:
  WS  /ws/predict          — real-time frame prediction via WebSocket
  POST /api/tts            — text-to-speech (returns MP3 bytes)
  GET  /api/signs          — list all supported signs
  GET  /api/health         — health check

Both hands are now detected and encoded into 126 keypoints per frame:
  [left_hand_63_values, right_hand_63_values]
Missing hand is zero-padded automatically.

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

# ── Keypoint config ───────────────────────────────────────────────────────────
KEYPOINTS_PER_HAND = 63          # 21 landmarks × 3 (x, y, z)
TOTAL_KEYPOINTS    = KEYPOINTS_PER_HAND * 2   # 126  (left + right)

# ── MediaPipe — detect BOTH hands ─────────────────────────────────────────────
mp_hands = mp.solutions.hands
HANDS    = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,                 # ← both hands
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
app = FastAPI(title="Sign Language Translator API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Runtime constants ─────────────────────────────────────────────────────────
SEQUENCE_LEN   = 30     # frames in one prediction window
CONF_THRESHOLD = 0.75   # minimum confidence to emit a prediction
COOLDOWN_SECS  = 1.2    # seconds between repeated identical predictions


# ── Keypoint extraction (BOTH HANDS) ─────────────────────────────────────────
def extract_keypoints(frame_bgr: np.ndarray) -> np.ndarray:
    """
    Run MediaPipe on one BGR frame.
    Returns a flat (126,) array:
        [left_hand_63_values, right_hand_63_values]
    Missing hand → zeros.
    """
    left  = np.zeros(KEYPOINTS_PER_HAND)
    right = np.zeros(KEYPOINTS_PER_HAND)

    rgb     = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    results = HANDS.process(rgb)

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(
            results.multi_hand_landmarks,
            results.multi_handedness,
        ):
            label = handedness.classification[0].label   # 'Left' or 'Right'
            kp    = np.array(
                [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]
            ).flatten()   # (63,)

            if label == "Left":
                left = kp
            else:
                right = kp

    return np.concatenate([left, right])   # (126,)


# ── Frame decode ──────────────────────────────────────────────────────────────
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
        self.sequence: deque  = deque(maxlen=SEQUENCE_LEN)
        self.last_sign: str   = ""
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

            # ── Extract both-hand keypoints (126,) ────────────────────────────
            keypoints = extract_keypoints(frame)
            state.sequence.append(keypoints)

            hand_detected = bool(keypoints.any())
            response = {"type": "keypoints", "hand_detected": hand_detected}

            # ── Predict once we have a full sequence ──────────────────────────
            if len(state.sequence) == SEQUENCE_LEN and model is not None:
                # shape: (1, 30, 126)
                seq_arr = np.expand_dims(list(state.sequence), axis=0)
                probs   = model.predict(seq_arr, verbose=0)[0]
                top_idx = int(np.argmax(probs))
                conf    = float(probs[top_idx])

                if conf >= CONF_THRESHOLD:
                    sign = labels[top_idx]
                    now  = time.time()
                    is_new = (sign != state.last_sign) or \
                             (now - state.last_time > COOLDOWN_SECS)

                    if is_new:
                        state.last_sign = sign
                        state.last_time = now
                        response.update({
                            "type":       "prediction",
                            "sign":       sign,
                            "confidence": round(conf * 100, 1),
                            "top5": [
                                {
                                    "sign": labels[i],
                                    "prob": round(float(probs[i]) * 100, 1),
                                }
                                for i in np.argsort(probs)[::-1][:5]
                            ],
                        })
                    else:
                        response.update({"type": "hold", "sign": sign})
                else:
                    response.update({
                        "type":       "low_conf",
                        "confidence": round(conf * 100, 1),
                    })

            elif model is None:
                # ── Demo mode — random signs for UI testing ───────────────────
                import random
                demo_signs = ["hello", "yes", "no", "thankyou", "iloveyou"]
                if len(state.sequence) % SEQUENCE_LEN == 0:
                    response.update({
                        "type":       "prediction",
                        "sign":       random.choice(demo_signs),
                        "confidence": round(random.uniform(82, 99), 1),
                        "top5":       [],
                        "demo":       True,
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
        "status":          "ok",
        "model_loaded":    _model is not None,
        "sign_count":      len(labels),
        "keypoints_frame": TOTAL_KEYPOINTS,
        "hands_supported": 2,
        "version":         "3.0.0",
    }


# ── Entry ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
