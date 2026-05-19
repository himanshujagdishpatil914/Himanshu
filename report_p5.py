"""
SignAI Project Report — Part 5
Chapter 4: Implementation
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, HRFlowable,
    PageBreak, KeepTogether
)
from reportlab.graphics.shapes import Drawing, Rect, Line, String

W, H = A4
PAGE_W = W - 50*mm

NAVY    = colors.HexColor("#1a237e")
BLUE    = colors.HexColor("#1565c0")
LBLUE   = colors.HexColor("#1976d2")
GRAY_DK = colors.HexColor("#212121")
GRAY    = colors.HexColor("#424242")
GRAY_LT = colors.HexColor("#757575")
GRAY_BG = colors.HexColor("#f5f5f5")
GRAY_LN = colors.HexColor("#e0e0e0")
WHITE   = colors.white
GREEN   = colors.HexColor("#1b5e20")
LGREEN  = colors.HexColor("#e8f5e9")
CODE_BG = colors.HexColor("#f1f8e9")
CODE_FG = colors.HexColor("#1b5e20")


def code_block(lines, styles):
    """Render a code block as a styled table."""
    rows = [[Paragraph(ln.replace(" ", "&nbsp;").replace("<", "&lt;").replace(">", "&gt;"),
                       styles["code"])] for ln in lines]
    t = Table(rows, colWidths=[PAGE_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CODE_BG),
        ("BOX",        (0,0), (-1,-1), 0.8, colors.HexColor("#c8e6c9")),
        ("TOPPADDING",    (0,0), (-1,-1), 1),
        ("BOTTOMPADDING", (0,0), (-1,-1), 1),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
    ]))
    return t


def build_ch4(styles):
    from report_p1 import rule, thin_rule, sp, info_table, left_table

    story = []

    # ── Chapter banner ────────────────────────────────────────────────────────
    d = Drawing(PAGE_W, 52)
    d.add(Rect(0, 0, PAGE_W, 52, fillColor=NAVY, strokeColor=NAVY))
    d.add(String(16, 32, "CHAPTER 4", fontSize=12, fontName="Helvetica-Bold",
                 fillColor=colors.HexColor("#90caf9"), textAnchor="start"))
    d.add(String(16, 11, "Implementation", fontSize=20,
                 fontName="Helvetica-Bold", fillColor=WHITE, textAnchor="start"))
    story.append(d)
    story.append(sp(14))

    # ── 4.1 Environment Setup ─────────────────────────────────────────────────
    story.append(Paragraph("4.1  Development Environment Setup", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The development environment for SignAI requires both a Python backend and a "
        "Node.js frontend. The following libraries and tools were used:", styles["body"]))

    story.append(sp(4))
    story.append(Paragraph("Table 4.4 — Python Backend Dependencies",
                            styles["caption"]))
    py_deps = [
        ["Package",          "Version",  "Purpose"],
        ["tensorflow",       "2.16.1",   "LSTM model training and inference"],
        ["mediapipe",        "0.10.14",  "Hand landmark detection"],
        ["opencv-python-headless", "4.9.0", "Frame decoding and colour conversion"],
        ["fastapi",          "0.111.0",  "HTTP and WebSocket API server"],
        ["uvicorn",          "0.29.0",   "ASGI production-grade server"],
        ["numpy",            "1.26.4",   "Numerical array processing"],
        ["scikit-learn",     "1.4.2",    "Dataset splitting, metrics"],
        ["gTTS",             "2.5.1",    "Google Text-to-Speech"],
        ["python-multipart", "0.0.9",    "Multipart HTTP handling"],
        ["websockets",       "12.0",     "WebSocket support"],
    ]
    story.append(info_table(py_deps, [PAGE_W*0.35, PAGE_W*0.18, PAGE_W*0.47]))
    story.append(sp(8))

    story.append(Paragraph("Table 4.5 — Node.js Frontend Dependencies",
                            styles["caption"]))
    node_deps = [
        ["Package",       "Version",   "Purpose"],
        ["react",         "18.3.1",    "Core UI component library"],
        ["react-dom",     "18.3.1",    "DOM rendering"],
        ["react-webcam",  "7.2.0",     "Browser webcam access"],
        ["framer-motion", "11.2.10",   "Animation library"],
        ["lucide-react",  "0.390.0",   "Icon components"],
        ["react-scripts", "5.0.1",     "CRA build toolchain"],
    ]
    story.append(info_table(node_deps, [PAGE_W*0.32, PAGE_W*0.18, PAGE_W*0.50]))
    story.append(sp(10))

    # ── 4.2 Data Collection ───────────────────────────────────────────────────
    story.append(Paragraph("4.2  Data Collection Implementation", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The data collection script uses OpenCV for webcam access and MediaPipe for hand "
        "landmark detection. The script is interactive, with on-screen HUD showing the "
        "current sign, sample count, and recording status.", styles["body"]))

    story.append(sp(4))
    story.append(Paragraph("Table 4.1 — Supported Signs — 40 Total Categories",
                            styles["caption"]))
    signs_data = [
        ["Category",        "Count", "Signs"],
        ["Common Phrases",  "10",
         "hello, yes, no, thankyou, please, sorry, help, good, bad, stop"],
        ["Expressions",     "5",
         "iloveyou, goodmorning, goodnight, howareyou, fine"],
        ["Actions",         "5",
         "eat, drink, sleep, come, go"],
        ["Alphabet (A–J)",  "10",
         "A, B, C, D, E, F, G, H, I, J"],
        ["Numbers (1–10)",  "10",
         "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"],
        ["TOTAL",           "40",   "—"],
    ]
    story.append(left_table(signs_data,
        [PAGE_W*0.25, PAGE_W*0.10, PAGE_W*0.65]))
    story.append(sp(8))

    story.append(Paragraph(
        "The core keypoint extraction function for both hands is shown below:",
        styles["body"]))
    story.append(sp(4))

    story.append(code_block([
        "# extract_keypoints() — returns 126-d vector for both hands",
        "def extract_keypoints(results):",
        "    left  = np.zeros(63)  # left hand placeholder",
        "    right = np.zeros(63)  # right hand placeholder",
        "",
        "    if results.multi_hand_landmarks and results.multi_handedness:",
        "        for hand_landmarks, handedness in zip(",
        "            results.multi_hand_landmarks,",
        "            results.multi_handedness):",
        "",
        "            label = handedness.classification[0].label  # 'Left'/'Right'",
        "            kp = np.array([[lm.x, lm.y, lm.z]",
        "                           for lm in hand_landmarks.landmark]).flatten()",
        "            if label == 'Left':   left  = kp",
        "            else:                 right = kp",
        "",
        "    return np.concatenate([left, right])  # shape: (126,)",
    ], styles))
    story.append(Paragraph("Code Snippet 4.1 — Dual-Hand Keypoint Extraction Function",
                            styles["caption"]))
    story.append(sp(8))

    story.append(Paragraph(
        "For each sign, the MediaPipe Hands model is initialised with "
        "<code>max_num_hands=2</code> to detect both hands simultaneously. "
        "The recording loop captures exactly 30 frames per sample, building a "
        "(30, 126) sequence array which is saved as a compressed NumPy file.",
        styles["body"]))

    story.append(code_block([
        "# Recording loop — 30 frames per sample",
        "with mp_hands.Hands(max_num_hands=2,",
        "                    min_detection_confidence=0.7,",
        "                    min_tracking_confidence=0.6) as hands:",
        "    sequence = []",
        "    for frame_num in range(SEQUENCE_LENGTH):   # 30 frames",
        "        ret, frame = cap.read()",
        "        frame   = cv2.flip(frame, 1)",
        "        rgb     = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)",
        "        results = hands.process(rgb)",
        "",
        "        keypoints = extract_keypoints(results)  # (126,)",
        "        sequence.append(keypoints)",
        "",
        "    # Save as (30, 126) numpy array",
        "    np.save(os.path.join(sign_dir, f'{existing}.npy'),",
        "            np.array(sequence))",
    ], styles))
    story.append(Paragraph("Code Snippet 4.2 — 30-Frame Sequence Recording Loop",
                            styles["caption"]))
    story.append(sp(10))

    # ── 4.3 Model Training ────────────────────────────────────────────────────
    story.append(Paragraph("4.3  Model Training Implementation", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The training script loads all collected <code>.npy</code> sequences, splits them "
        "into training (70%), validation (15%), and test (15%) sets, then trains the "
        "Stacked LSTM model using the Adam optimiser with early stopping.",
        styles["body"]))

    story.append(sp(4))
    story.append(Paragraph("Table 4.2 — Dataset Statistics (200 samples/sign)",
                            styles["caption"]))
    ds_data = [
        ["Category", "Signs", "Samples/Sign", "Total Samples", "% of Dataset"],
        ["Common Phrases", "10", "200", "2,000", "25.0%"],
        ["Expressions",    "5",  "200", "1,000", "12.5%"],
        ["Actions",        "5",  "200", "1,000", "12.5%"],
        ["Alphabet A–J",   "10", "200", "2,000", "25.0%"],
        ["Numbers 1–10",   "10", "200", "2,000", "25.0%"],
        ["TOTAL",          "40", "200", "8,000", "100.0%"],
    ]
    story.append(info_table(ds_data,
        [PAGE_W*0.22, PAGE_W*0.12, PAGE_W*0.18, PAGE_W*0.20, PAGE_W*0.28]))
    story.append(sp(4))

    story.append(Paragraph("Table 4.3 — Training Configuration", styles["caption"]))
    tr_data = [
        ["Parameter",        "Value",     "Parameter",       "Value"],
        ["Total samples",    "8,000",     "Train set",       "5,780 (72.25%)"],
        ["Validation set",   "1,020 (12.75%)", "Test set",  "1,200 (15%)"],
        ["Max epochs",       "200",       "Batch size",      "32"],
        ["Learning rate",    "0.001",     "Optimiser",       "Adam"],
        ["Early stopping",   "Patience=20","LR reduction",   "Factor=0.5, P=8"],
        ["Min LR",           "1e-6",      "Model checkpoint","Best val_accuracy"],
    ]
    story.append(info_table(tr_data,
        [PAGE_W*0.25, PAGE_W*0.25, PAGE_W*0.25, PAGE_W*0.25]))
    story.append(sp(8))

    story.append(Paragraph(
        "The Keras model is defined as a Sequential stack of LSTM, BatchNorm, "
        "and Dropout layers:", styles["body"]))
    story.append(sp(4))

    story.append(code_block([
        "def build_model(n_classes: int) -> tf.keras.Model:",
        "    model = Sequential([",
        "        LSTM(128, return_sequences=True,",
        "             input_shape=(30, 126)),   # 30 frames × 126 keypoints",
        "        BatchNormalization(), Dropout(0.3),",
        "",
        "        LSTM(256, return_sequences=True),",
        "        BatchNormalization(), Dropout(0.3),",
        "",
        "        LSTM(128, return_sequences=False),",
        "        BatchNormalization(), Dropout(0.3),",
        "",
        "        Dense(256, activation='relu'), Dropout(0.4),",
        "        Dense(128, activation='relu'), Dropout(0.3),",
        "        Dense(n_classes, activation='softmax'),  # 40 classes",
        "    ])",
        "    model.compile(optimizer=Adam(lr=1e-3),",
        "                  loss='categorical_crossentropy',",
        "                  metrics=['accuracy'])",
        "    return model",
    ], styles))
    story.append(Paragraph("Code Snippet 4.3 — Stacked LSTM Model Definition",
                            styles["caption"]))
    story.append(sp(10))

    # Training curve diagram
    story.append(Paragraph(
        "The model was trained for up to 200 epochs with early stopping. "
        "A typical training run converges in 60–80 epochs, achieving over 95% "
        "validation accuracy as illustrated in Fig 4.3 below.",
        styles["body"]))
    story.append(sp(6))

    tc = Drawing(PAGE_W, 120)
    tc.add(Rect(0, 0, PAGE_W, 120, fillColor=GRAY_BG, strokeColor=GRAY_LN))
    tc.add(Rect(40, 10, PAGE_W-60, 95, fillColor=WHITE, strokeColor=GRAY_LN))

    # Axes
    tc.add(Line(40, 10, 40, 105, strokeColor=GRAY, strokeWidth=1))
    tc.add(Line(40, 10, PAGE_W-20, 10, strokeColor=GRAY, strokeWidth=1))
    tc.add(String(PAGE_W/2, 1, "Epochs", fontSize=8, fontName="Helvetica",
                  fillColor=GRAY, textAnchor="middle"))
    tc.add(String(12, 55, "Accuracy", fontSize=8, fontName="Helvetica",
                  fillColor=GRAY, textAnchor="middle"))

    # Epoch marks
    epochs = [0, 20, 40, 60, 80, 100]
    gw = (PAGE_W-60) / (len(epochs)-1)
    for i, ep in enumerate(epochs):
        x = 40 + i*gw
        tc.add(Line(x, 10, x, 105, strokeColor=GRAY_LN, strokeWidth=0.4))
        tc.add(String(x, 3, str(ep), fontSize=7, fontName="Helvetica",
                      fillColor=GRAY_LT, textAnchor="middle"))

    # Accuracy marks
    for pct, label in [(10, "0.0"), (35, "0.5"), (60, "0.75"),
                       (75, "0.9"), (86, "0.95"), (95, "1.0")]:
        tc.add(Line(40, pct, PAGE_W-20, pct,
                    strokeColor=GRAY_LN, strokeWidth=0.4))
        tc.add(String(36, pct-2, label, fontSize=7, fontName="Helvetica",
                      fillColor=GRAY_LT, textAnchor="end"))

    # Training accuracy curve
    train_pts = [(40,10),(40+gw*0.5,30),(40+gw*1,50),(40+gw*2,70),
                 (40+gw*3,82),(40+gw*4,89),(40+gw*5,93)]
    for i in range(len(train_pts)-1):
        tc.add(Line(train_pts[i][0], train_pts[i][1],
                    train_pts[i+1][0], train_pts[i+1][1],
                    strokeColor=LBLUE, strokeWidth=2))

    # Validation accuracy curve
    val_pts = [(40,10),(40+gw*0.5,26),(40+gw*1,45),(40+gw*2,66),
               (40+gw*3,80),(40+gw*4,87),(40+gw*5,91)]
    for i in range(len(val_pts)-1):
        tc.add(Line(val_pts[i][0], val_pts[i][1],
                    val_pts[i+1][0], val_pts[i+1][1],
                    strokeColor=colors.HexColor("#c62828"), strokeWidth=2))

    # Legend
    tc.add(Rect(PAGE_W-130, 90, 110, 12,
                fillColor=WHITE, strokeColor=GRAY_LN))
    tc.add(Line(PAGE_W-125, 96, PAGE_W-105, 96,
                strokeColor=LBLUE, strokeWidth=2))
    tc.add(String(PAGE_W-100, 93, "Training Acc", fontSize=7,
                  fontName="Helvetica", fillColor=GRAY_DK))
    tc.add(Line(PAGE_W-125, 88, PAGE_W-105, 88,
                strokeColor=colors.HexColor("#c62828"), strokeWidth=2))
    tc.add(String(PAGE_W-100, 85, "Validation Acc", fontSize=7,
                  fontName="Helvetica", fillColor=GRAY_DK))

    story.append(tc)
    story.append(Paragraph("Fig 4.3 — Training and Validation Accuracy Curves",
                            styles["caption"]))
    story.append(sp(10))

    # ── 4.4 Backend ───────────────────────────────────────────────────────────
    story.append(Paragraph("4.4  Backend Implementation", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The FastAPI backend exposes a WebSocket endpoint at <code>/ws/predict</code> "
        "that accepts base64-encoded JPEG frames, extracts keypoints, accumulates a "
        "sliding window of 30 frames, and returns predictions.",
        styles["body"]))
    story.append(sp(4))

    story.append(code_block([
        "@app.websocket('/ws/predict')",
        "async def ws_predict(websocket: WebSocket):",
        "    await websocket.accept()",
        "    model, labels = get_model()",
        "    state = PredictorState()   # holds 30-frame deque",
        "",
        "    while True:",
        "        raw = await websocket.receive_text()",
        "        msg = json.loads(raw)",
        "",
        "        frame     = decode_frame(msg['frame'])   # base64 → BGR",
        "        keypoints = extract_keypoints(frame)     # (126,)",
        "        state.sequence.append(keypoints)",
        "",
        "        if len(state.sequence) == 30:            # full window",
        "            seq = np.expand_dims(list(state.sequence), axis=0)",
        "            probs   = model.predict(seq)[0]      # (40,)",
        "            top_idx = int(np.argmax(probs))",
        "            sign    = labels[top_idx]",
        "            conf    = float(probs[top_idx])",
        "",
        "            if conf >= 0.75:                      # threshold check",
        "                await websocket.send_text(json.dumps({",
        "                    'type': 'prediction',",
        "                    'sign': sign,",
        "                    'confidence': round(conf*100, 1)",
        "                }))",
    ], styles))
    story.append(Paragraph("Code Snippet 4.4 — WebSocket Prediction Endpoint",
                            styles["caption"]))
    story.append(sp(8))

    story.append(Paragraph(
        "The TTS endpoint accepts a text string and returns a streaming MP3 audio "
        "response generated by Google TTS (gTTS):",
        styles["body"]))
    story.append(sp(4))

    story.append(code_block([
        "@app.post('/api/tts')",
        "async def text_to_speech(req: TTSRequest):",
        "    buf = io.BytesIO()",
        "    tts = gTTS(text=req.text.strip(), lang=req.lang)",
        "    tts.write_to_fp(buf)",
        "    buf.seek(0)",
        "    return StreamingResponse(buf, media_type='audio/mpeg')",
    ], styles))
    story.append(Paragraph("Code Snippet 4.5 — Text-to-Speech REST Endpoint",
                            styles["caption"]))
    story.append(sp(10))

    # ── 4.5 Frontend ──────────────────────────────────────────────────────────
    story.append(Paragraph("4.5  Frontend Implementation", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The React.js frontend uses the <code>react-webcam</code> library to access the "
        "user's webcam and captures frames at 15 fps. Each frame is sent as a base64 "
        "JPEG over a WebSocket connection to the backend.",
        styles["body"]))
    story.append(sp(4))

    story.append(code_block([
        "// Camera.jsx — WebSocket frame sender (15 fps)",
        "const sendFrame = useCallback(() => {",
        "  if (!webcamRef.current || ws.readyState !== WebSocket.OPEN) return;",
        "  const img = webcamRef.current.getScreenshot(",
        "              { width: 320, height: 240 });",
        "  ws.send(JSON.stringify({ frame: img }));",
        "}, []);",
        "",
        "useEffect(() => {",
        "  if (active) {",
        "    connectWS();",
        "    timerRef.current = setInterval(sendFrame, 1000/15); // 15 fps",
        "  } else {",
        "    clearInterval(timerRef.current);",
        "    disconnectWS();",
        "  }",
        "  return () => clearInterval(timerRef.current);",
        "}, [active]);",
    ], styles))
    story.append(Paragraph("Code Snippet 4.6 — React Camera Component — 15fps Frame Sender",
                            styles["caption"]))
    story.append(sp(8))

    story.append(Paragraph(
        "The Sentence Builder component manages an array of detected words. "
        "Clicking <b>Speak</b> calls the backend TTS endpoint and plays the returned MP3:",
        styles["body"]))
    story.append(sp(4))

    story.append(code_block([
        "// SentenceBuilder.jsx — TTS handler",
        "const speak = async () => {",
        "  const res = await fetch(`${API_BASE}/api/tts`, {",
        "    method: 'POST',",
        "    headers: { 'Content-Type': 'application/json' },",
        "    body: JSON.stringify({ text: sentence.join(' ') }),",
        "  });",
        "  const blob = await res.blob();",
        "  const url  = URL.createObjectURL(blob);",
        "  audioRef.current.src = url;",
        "  audioRef.current.play();   // plays MP3 in browser",
        "};",
    ], styles))
    story.append(Paragraph("Code Snippet 4.7 — Text-to-Speech Integration in React",
                            styles["caption"]))
    story.append(sp(10))

    # ── 4.6 Integration ────────────────────────────────────────────────────────
    story.append(Paragraph("4.6  Integration and Deployment", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The two services are run concurrently — the FastAPI backend on port 8000 and "
        "the React development server on port 3000. The frontend proxies API requests "
        "to the backend via the <code>proxy</code> setting in <code>package.json</code>. "
        "WebSocket connections are established directly to <code>ws://localhost:8000/ws/predict</code>.",
        styles["body"]))

    story.append(code_block([
        "# Terminal 1 — Start Backend",
        "cd backend",
        "source venv/bin/activate",
        "uvicorn app:app --host 0.0.0.0 --port 8000 --reload",
        "",
        "# Terminal 2 — Start Frontend",
        "cd frontend",
        "npm start           # Opens http://localhost:3000",
    ], styles))
    story.append(Paragraph("Code Snippet 4.8 — Startup Commands for Both Services",
                            styles["caption"]))

    story.append(PageBreak())
    return story


def build_ch4_extra(styles):
    """Extra implementation content — system integration details, UI walkthrough."""
    from report_p1 import rule, thin_rule, sp, info_table, left_table
    story = []

    story.append(Paragraph("4.7  Detailed UI Walkthrough", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The SignAI frontend provides two primary tabs: the <b>Translator</b> tab for real-time "
        "sign detection, and the <b>Sign List</b> tab for browsing the sign dictionary. "
        "This section describes the user workflow in detail.", styles["body"]))

    story.append(Paragraph("Translator Tab — Step-by-Step Workflow", styles["h3"]))
    steps = [
        ("Step 1 — Open the Application",
         "Navigate to http://localhost:3000 in a modern browser (Chrome/Firefox recommended). "
         "The application loads in approximately 1–2 seconds with all components initialised."),
        ("Step 2 — Grant Camera Permission",
         "Click the 'Start Detecting' button. The browser will prompt for webcam access. "
         "Click 'Allow' to grant permission. The live camera feed will appear immediately."),
        ("Step 3 — Perform a Sign",
         "Hold your hand(s) clearly in front of the camera with a plain background if possible. "
         "Perform any of the 40 supported signs. The green MediaPipe skeleton overlay will appear "
         "on your hand(s) confirming detection."),
        ("Step 4 — View the Detection",
         "After approximately 2 seconds (30 frames at 15fps), the detected sign appears in the "
         "'Detected Sign' panel with its name in large gradient text and a confidence bar."),
        ("Step 5 — Build a Sentence",
         "Each confirmed sign (confidence ≥ 75%) is automatically added as a coloured chip in "
         "the Sentence Builder. Toggle between 'Words' mode (chips) and 'Sentence' mode (full text)."),
        ("Step 6 — Speak the Sentence",
         "Click '🔊 Speak' to convert the built sentence to speech via Google TTS. "
         "Use '⌫ Undo' to remove the last word, or '🗑 Clear' to start a new sentence."),
    ]
    for title, desc in steps:
        story.append(Paragraph(f"<b>{title}:</b>  {desc}", styles["bullet"]))
        story.append(sp(5))

    story.append(sp(8))
    story.append(Paragraph("Sign List Tab", styles["h3"]))
    story.append(Paragraph(
        "The Sign List tab displays all 40 supported signs organised by category "
        "(Common Phrases, Expressions, Actions, Alphabet, Numbers). A search box at the "
        "top allows users to quickly filter signs by name. Each sign card shows an emoji "
        "icon and the sign name, providing a quick reference guide for learners.",
        styles["body"]))
    story.append(sp(10))

    story.append(Paragraph("4.8  Error Handling and Edge Cases", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The SignAI system includes comprehensive error handling for robustness in real-world use:",
        styles["body"]))

    errors = [
        ["Scenario", "Detection", "Handling Strategy"],
        ["Camera denied by user",
         "Browser camera API throws error",
         "Error message displayed; user prompted to allow camera"],
        ["WebSocket connection lost",
         "WS onclose event fires",
         "Status bar turns amber; auto-reconnect on next 'Start' click"],
        ["Model not loaded (first run)",
         "/api/health returns model_loaded=false",
         "Demo mode activated; random signs shown for UI testing"],
        ["Low confidence prediction (<75%)",
         "Confidence below CONF_THRESHOLD",
         "Prediction suppressed; no sign added to sentence"],
        ["No hand in frame",
         "MediaPipe returns empty results",
         "'No Hand' indicator shown; keypoints are zero-padded"],
        ["TTS backend unavailable",
         "fetch() throws network error",
         "Browser SpeechSynthesis API used as fallback"],
        ["Duplicate sign (same sign held)",
         "Same sign within COOLDOWN_SECS (1.2s)",
         "Prediction suppressed to prevent duplicate chips"],
    ]
    story.append(left_table(errors,
        [PAGE_W*0.25, PAGE_W*0.30, PAGE_W*0.45]))
    story.append(sp(10))

    story.append(Paragraph("4.9  Security Considerations", styles["h2"]))
    story.append(rule())
    security = [
        ("<b>Camera Access:</b>  The webcam is accessed only within the browser's secure context. "
         "No video data is stored or transmitted beyond the local WebSocket connection."),
        ("<b>CORS Policy:</b>  The FastAPI backend uses CORS middleware configured to allow "
         "all origins in development. For production deployment, origins should be restricted "
         "to the specific frontend domain."),
        ("<b>Data Privacy:</b>  No user data, video frames, or signs are stored permanently. "
         "All processing is performed in-memory per session. Frames are discarded after keypoint extraction."),
        ("<b>API Security:</b>  The TTS endpoint validates that the text input is non-empty "
         "and within reasonable length. Future versions should add rate limiting and authentication."),
    ]
    for s in security:
        story.append(Paragraph(f"• {s}", styles["bullet"]))
        story.append(sp(4))

    story.append(sp(8))
    story.append(Paragraph("4.10  Testing Strategy", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The SignAI system was tested at multiple levels to ensure correctness, "
        "performance, and usability:", styles["body"]))

    testing = [
        ["Test Level", "Test Type", "Tool / Method", "Coverage"],
        ["Unit",       "Keypoint extraction",   "Python unittest",    "extract_keypoints() both hands"],
        ["Unit",       "Model inference",        "TensorFlow test",    "Prediction shape + confidence"],
        ["Unit",       "TTS endpoint",           "FastAPI TestClient", "MP3 generation, error handling"],
        ["Integration","WebSocket pipeline",     "Manual testing",     "Frame → prediction round-trip"],
        ["Integration","Frontend-Backend",       "Browser DevTools",   "WS messages, API calls"],
        ["System",     "End-to-end accuracy",    "40 signs × 30 tests","Per-sign confusion matrix"],
        ["Performance","Latency measurement",    "Python time module", "All stages timed"],
        ["Usability",  "User acceptance testing","5 volunteers",       "Ease of use, satisfaction"],
    ]
    story.append(info_table(testing,
        [PAGE_W*0.12, PAGE_W*0.24, PAGE_W*0.24, PAGE_W*0.40]))

    story.append(PageBreak())
    return story
