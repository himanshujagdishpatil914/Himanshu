"""
SignAI Project Report — Part 4
Chapter 3: System Design and Architecture
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
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Circle
import math

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
TEAL    = colors.HexColor("#004d40")
AMBER   = colors.HexColor("#e65100")
PURPLE  = colors.HexColor("#4a148c")
CYAN    = colors.HexColor("#006064")
LGREEN  = colors.HexColor("#388e3c")
LORANGE = colors.HexColor("#f57c00")


def box(d, x, y, w, h, label, sub="", fill=LBLUE, tc=WHITE, fs=9):
    d.add(Rect(x, y, w, h, fillColor=fill, strokeColor=NAVY, strokeWidth=0.8,
               rx=4, ry=4))
    mid_y = y + h/2 + (4 if sub else 0)
    d.add(String(x+w/2, mid_y, label, fontSize=fs, fontName="Helvetica-Bold",
                 fillColor=tc, textAnchor="middle"))
    if sub:
        d.add(String(x+w/2, y+h/2-8, sub, fontSize=7, fontName="Helvetica",
                     fillColor=tc, textAnchor="middle"))


def arr(d, x1, y1, x2, y2):
    d.add(Line(x1, y1, x2, y2, strokeColor=GRAY, strokeWidth=1.0))
    ang = math.atan2(y2-y1, x2-x1)
    for da in (0.5, -0.5):
        ax = x2 - 6*math.cos(ang+da)
        ay = y2 - 6*math.sin(ang+da)
        d.add(Line(x2, y2, ax, ay, strokeColor=GRAY, strokeWidth=1.0))


def build_ch3(styles):
    from report_p1 import rule, thin_rule, sp, info_table, left_table

    story = []

    # ── Chapter banner ────────────────────────────────────────────────────────
    d = Drawing(PAGE_W, 52)
    d.add(Rect(0, 0, PAGE_W, 52, fillColor=NAVY, strokeColor=NAVY))
    d.add(String(16, 32, "CHAPTER 3", fontSize=12, fontName="Helvetica-Bold",
                 fillColor=colors.HexColor("#90caf9"), textAnchor="start"))
    d.add(String(16, 11, "System Design and Architecture", fontSize=20,
                 fontName="Helvetica-Bold", fillColor=WHITE, textAnchor="start"))
    story.append(d)
    story.append(sp(14))

    # ── 3.1 Overall Architecture ──────────────────────────────────────────────
    story.append(Paragraph("3.1  Overall System Architecture", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "SignAI follows a <b>three-tier client-server architecture</b> with real-time bidirectional "
        "communication via WebSockets. The system is divided into three major subsystems: "
        "(1) the Data Collection and Training Pipeline, (2) the Backend Inference Server, "
        "and (3) the React.js Frontend Application.",
        styles["body"]))

    # Architecture diagram
    story.append(sp(8))
    dw = PAGE_W
    dh = 200
    arch = Drawing(dw, dh)
    arch.add(Rect(0, 0, dw, dh, fillColor=colors.HexColor("#f8f9fa"),
                  strokeColor=GRAY_LN))

    # Column 1 — User / Frontend
    box(arch, 10, 140, 100, 36, "User / Browser", "React.js App",
        fill=colors.HexColor("#1565c0"))
    box(arch, 10, 95,  100, 36, "Webcam Feed", "15 fps frames",
        fill=colors.HexColor("#1976d2"), fs=8)
    box(arch, 10, 50,  100, 36, "Sentence Builder", "+ TTS Output",
        fill=colors.HexColor("#1976d2"), fs=8)
    box(arch, 10, 8,   100, 34, "Sign Display", "Confidence + Top-5",
        fill=colors.HexColor("#1976d2"), fs=8)

    # Arrow col1 → col2
    arr(arch, 110, 158, 148, 158)
    arch.add(String(128, 162, "WS", fontSize=7, fontName="Helvetica-Bold",
                    fillColor=GRAY_LT, textAnchor="middle"))

    # Column 2 — Backend
    box(arch, 148, 140, 120, 36, "FastAPI Server", "WebSocket + REST",
        fill=colors.HexColor("#00695c"))
    box(arch, 148, 95,  120, 36, "MediaPipe", "Hands (max=2)",
        fill=colors.HexColor("#00796b"), fs=8)
    box(arch, 148, 50,  120, 36, "LSTM Inference", "(30, 126) → softmax",
        fill=colors.HexColor("#00796b"), fs=8)
    box(arch, 148, 8,   120, 34, "gTTS Engine", "Text-to-Speech",
        fill=colors.HexColor("#00796b"), fs=8)

    # Vertical arrows in col2
    arr(arch, 208, 140, 208, 131)
    arr(arch, 208, 95,  208, 86)
    arr(arch, 208, 50,  208, 42)

    # Arrow col2 → col3
    arr(arch, 268, 158, 306, 158)

    # Column 3 — ML Pipeline
    box(arch, 306, 140, 120, 36, "Trained Model", "sign_model.h5",
        fill=colors.HexColor("#4a148c"))
    box(arch, 306, 95,  120, 36, "Model Training", "TensorFlow/Keras",
        fill=colors.HexColor("#6a1b9a"), fs=8)
    box(arch, 306, 50,  120, 36, "Data Collection", "collect_data.py",
        fill=colors.HexColor("#6a1b9a"), fs=8)
    box(arch, 306, 8,   120, 34, "Keypoint Storage", ".npy (30,126)",
        fill=colors.HexColor("#6a1b9a"), fs=8)

    # Vertical arrows col3
    arr(arch, 366, 95, 366, 86)
    arr(arch, 366, 50, 366, 42)

    # Labels
    arch.add(String(60,  185, "FRONTEND", fontSize=8, fontName="Helvetica-Bold",
                    fillColor=colors.HexColor("#1565c0"), textAnchor="middle"))
    arch.add(String(208, 185, "BACKEND", fontSize=8, fontName="Helvetica-Bold",
                    fillColor=colors.HexColor("#00695c"), textAnchor="middle"))
    arch.add(String(366, 185, "ML PIPELINE", fontSize=8, fontName="Helvetica-Bold",
                    fillColor=colors.HexColor("#4a148c"), textAnchor="middle"))

    story.append(arch)
    story.append(Paragraph("Fig 3.1 — Overall SignAI System Architecture",
                            styles["caption"]))
    story.append(sp(8))

    story.append(Paragraph(
        "The data flow in SignAI proceeds as follows: the user's webcam captures frames "
        "at 15 fps in the browser. Each frame is encoded as a base64 JPEG and sent over "
        "a WebSocket connection to the FastAPI backend. The backend decodes the frame, "
        "extracts 126 hand keypoints using MediaPipe, accumulates a 30-frame sliding window, "
        "and runs the LSTM model to produce a sign prediction with confidence score. "
        "The prediction is streamed back to the frontend where it is displayed and optionally "
        "spoken aloud via the TTS engine.",
        styles["body"]))
    story.append(sp(10))

    # ── 3.2 Data Collection Module ────────────────────────────────────────────
    story.append(Paragraph("3.2  Data Collection Module", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The data collection module (<code>collect_data.py</code>) provides an interactive "
        "webcam interface for recording training samples. For each of the 40 supported signs, "
        "the user performs the sign while the script records 30 consecutive frames, extracting "
        "126 keypoints per frame and saving the resulting (30, 126) numpy array as a <code>.npy</code> "
        "file.",
        styles["body"]))

    # Data collection flow diagram
    story.append(sp(6))
    dc = Drawing(PAGE_W, 60)
    dc.add(Rect(0, 0, PAGE_W, 60, fillColor=GRAY_BG, strokeColor=GRAY_LN))
    bw = (PAGE_W - 20) / 6
    labels = ["Webcam\nOpen", "User\nPerforms\nSign", "MediaPipe\nExtracts\nLandmarks",
              "Keypoints\nArray\n(126,)", "30-Frame\nWindow\n(30,126)", "Save\n.npy\nFile"]
    fills  = [LBLUE, LBLUE, LGREEN, LGREEN, LORANGE, colors.HexColor("#c62828")]
    for i, (lbl, fill) in enumerate(zip(labels, fills)):
        bx = 10 + i*(bw+2)
        dc.add(Rect(bx, 10, bw, 44, fillColor=fill, strokeColor=WHITE,
                    rx=3, ry=3))
        lines = lbl.split("\n")
        base_y = 10 + 44/2 + (len(lines)-1)*5
        for j, ln in enumerate(lines):
            dc.add(String(bx+bw/2, base_y-j*11, ln, fontSize=7.5,
                          fontName="Helvetica-Bold", fillColor=WHITE,
                          textAnchor="middle"))
        if i < len(labels)-1:
            arr(dc, bx+bw+2, 32, bx+bw+2, 32)

    story.append(dc)
    story.append(Paragraph("Fig 3.2 — Data Collection Pipeline Flow",
                            styles["caption"]))
    story.append(sp(10))

    # ── 3.3 Hand Landmark Extraction ──────────────────────────────────────────
    story.append(Paragraph("3.3  Hand Landmark Extraction", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "Hand landmark extraction is the core feature engineering step in SignAI. "
        "Google MediaPipe Hands detects up to two hands simultaneously in each video frame "
        "and provides the (x, y, z) coordinates of 21 landmarks per hand, all normalised "
        "to the range [0, 1] relative to the image dimensions.",
        styles["body"]))
    story.append(Paragraph(
        "The <code>extract_keypoints()</code> function separates detected hands by their "
        "handedness label ('Left' or 'Right') and concatenates them into a 126-dimensional "
        "feature vector. If only one hand is detected, the missing hand's 63-dimensional "
        "slot is filled with zeros, ensuring a consistent input dimensionality for the model.",
        styles["body"]))

    # Keypoint feature table
    story.append(sp(6))
    story.append(Paragraph("Table 3.1 — Keypoint Feature Vector Structure",
                            styles["caption"]))
    kp_data = [
        ["Index Range", "Content", "Dimension", "Description"],
        ["[0 – 62]",    "Left Hand",  "63",
         "21 landmarks × 3 (x, y, z) — zeros if not detected"],
        ["[63 – 125]",  "Right Hand", "63",
         "21 landmarks × 3 (x, y, z) — zeros if not detected"],
        ["Total",       "Both Hands", "126",
         "Concatenated feature vector per frame"],
        ["Sequence",    "30 Frames",  "30 × 126 = 3,780",
         "LSTM input window per prediction"],
    ]
    story.append(info_table(kp_data,
        [PAGE_W*0.18, PAGE_W*0.17, PAGE_W*0.15, PAGE_W*0.50]))
    story.append(sp(10))

    # ── 3.4 LSTM Model Architecture ───────────────────────────────────────────
    story.append(Paragraph("3.4  LSTM Model Architecture", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The classification model is a <b>Stacked LSTM</b> neural network with three LSTM "
        "layers followed by two Dense layers and a Softmax output. BatchNormalization and "
        "Dropout are applied after each LSTM layer to improve generalisation and reduce "
        "overfitting.",
        styles["body"]))

    # Model diagram
    story.append(sp(6))
    ml = Drawing(PAGE_W, 220)
    ml.add(Rect(0, 0, PAGE_W, 220, fillColor=GRAY_BG, strokeColor=GRAY_LN))

    layers = [
        ("Input", "(30, 126)",       colors.HexColor("#0277bd"), 196),
        ("LSTM-1 (128)", "return_seq=True", colors.HexColor("#1565c0"), 164),
        ("BatchNorm + Dropout(0.3)", "", colors.HexColor("#283593"), 138),
        ("LSTM-2 (256)", "return_seq=True", colors.HexColor("#1565c0"), 108),
        ("BatchNorm + Dropout(0.3)", "", colors.HexColor("#283593"), 82),
        ("LSTM-3 (128)", "return_seq=False", colors.HexColor("#1565c0"), 52),
        ("BatchNorm + Dropout(0.3)", "", colors.HexColor("#283593"), 26),
    ]
    bw2 = PAGE_W * 0.52
    bx2 = (PAGE_W - bw2) / 2
    for lbl, sub, fill, y in layers:
        ml.add(Rect(bx2, y, bw2, 22, fillColor=fill,
                    strokeColor=WHITE, strokeWidth=0.5, rx=3, ry=3))
        ml.add(String(PAGE_W/2, y+14, lbl, fontSize=8.5,
                      fontName="Helvetica-Bold", fillColor=WHITE,
                      textAnchor="middle"))
        if sub:
            ml.add(String(PAGE_W/2, y+4, sub, fontSize=7,
                          fontName="Helvetica", fillColor=colors.HexColor("#bbdefb"),
                          textAnchor="middle"))
        if y > 26:
            arr(ml, PAGE_W/2, y, PAGE_W/2, y-4)

    # Right side dense layers
    dense_layers = [
        ("Dense(256) + ReLU + Dropout(0.4)", colors.HexColor("#1b5e20"), 196),
        ("Dense(128) + ReLU + Dropout(0.3)", colors.HexColor("#2e7d32"), 164),
        ("Dense(40) + Softmax",              colors.HexColor("#c62828"), 132),
        ("Predicted Sign + Confidence",      colors.HexColor("#e65100"), 100),
    ]
    bx3 = PAGE_W * 0.56
    bw3 = PAGE_W * 0.40
    ml.add(String(bx3+bw3/2, 218, "CLASSIFIER", fontSize=8,
                  fontName="Helvetica-Bold", fillColor=LGREEN, textAnchor="middle"))
    for lbl, fill, y in dense_layers:
        ml.add(Rect(bx3, y, bw3, 20, fillColor=fill,
                    strokeColor=WHITE, strokeWidth=0.5, rx=3, ry=3))
        ml.add(String(bx3+bw3/2, y+11, lbl, fontSize=7.5,
                      fontName="Helvetica-Bold", fillColor=WHITE,
                      textAnchor="middle"))
        if y > 100:
            arr(ml, bx3+bw3/2, y, bx3+bw3/2, y-4)

    # connector from encoder to classifier
    arr(ml, bx2+bw2, 37, bx3, 185)

    ml.add(String(bx2/2+10, 218, "ENCODER", fontSize=8,
                  fontName="Helvetica-Bold",
                  fillColor=colors.HexColor("#1565c0"), textAnchor="middle"))

    story.append(ml)
    story.append(Paragraph("Fig 3.5 — Stacked LSTM Model Architecture",
                            styles["caption"]))

    story.append(sp(8))
    story.append(Paragraph("Table 3.2 — LSTM Model Hyperparameters", styles["caption"]))
    hp_data = [
        ["Hyperparameter", "Value", "Hyperparameter", "Value"],
        ["Input shape",      "(30, 126)",        "Optimiser",    "Adam (lr=0.001)"],
        ["LSTM-1 units",     "128",              "Loss function","Categorical Crossentropy"],
        ["LSTM-2 units",     "256",              "Metrics",      "Accuracy"],
        ["LSTM-3 units",     "128",              "Max epochs",   "200"],
        ["Dense-1 units",    "256",              "Batch size",   "32"],
        ["Dense-2 units",    "128",              "Early stopping","Patience = 20"],
        ["Output units",     "40 (# classes)",  "LR reduction", "Factor=0.5, Patience=8"],
        ["Dropout rate",     "0.3 / 0.4",       "Validation %", "15% of training data"],
    ]
    story.append(info_table(hp_data,
        [PAGE_W*0.25, PAGE_W*0.25, PAGE_W*0.28, PAGE_W*0.22]))
    story.append(sp(10))

    # ── 3.5 Backend API Design ────────────────────────────────────────────────
    story.append(Paragraph("3.5  Backend API Design", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The backend is built with <b>FastAPI</b>, a modern, high-performance Python web "
        "framework. It exposes a WebSocket endpoint for real-time prediction streaming and "
        "REST endpoints for TTS, sign listing, and health checking.",
        styles["body"]))

    story.append(sp(6))
    story.append(Paragraph("Table 3.3 — API Endpoint Specifications", styles["caption"]))
    api_data = [
        ["Method", "Endpoint", "Description", "Request", "Response"],
        ["WS",   "/ws/predict",  "Real-time sign prediction",
         "JSON: {frame: base64}", "JSON: {sign, confidence, top5}"],
        ["POST", "/api/tts",     "Text-to-Speech (MP3)",
         "JSON: {text, lang}",   "MP3 audio stream"],
        ["GET",  "/api/signs",   "List all 40 supported signs",
         "—",                    "JSON: {signs[], count}"],
        ["GET",  "/api/health",  "Server health check",
         "—",                    "JSON: {status, model_loaded}"],
    ]
    story.append(left_table(api_data,
        [PAGE_W*0.08, PAGE_W*0.18, PAGE_W*0.24,
         PAGE_W*0.24, PAGE_W*0.26]))
    story.append(sp(10))

    # ── 3.6 Frontend Design ───────────────────────────────────────────────────
    story.append(Paragraph("3.6  Frontend Design", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The frontend is built with <b>React.js 18</b> and uses <b>Framer Motion</b> for "
        "smooth animations. It consists of six key components arranged in a two-column grid "
        "layout with a dark glassmorphism theme.",
        styles["body"]))

    comp_data = [
        ["Component", "File", "Responsibility"],
        ["App",             "App.jsx",              "Root layout, tab routing, state management"],
        ["Header",          "Header.jsx",           "Logo, badge display, navigation hints"],
        ["StatusBar",       "StatusBar.jsx",        "WS connection status, hand detection indicator"],
        ["Camera",          "Camera.jsx",           "Webcam capture, WebSocket client, frame streaming"],
        ["SignDisplay",     "SignDisplay.jsx",       "Current sign, confidence bar, top-5 predictions"],
        ["SentenceBuilder", "SentenceBuilder.jsx",  "Word chips, sentence mode, TTS, Copy, Undo"],
        ["SignList",        "SignList.jsx",          "Sign dictionary with categories and search"],
    ]
    story.append(info_table(comp_data,
        [PAGE_W*0.22, PAGE_W*0.28, PAGE_W*0.50]))
    story.append(sp(10))

    # ── 3.7 Technology Stack ──────────────────────────────────────────────────
    story.append(Paragraph("3.7  Technology Stack", styles["h2"]))
    story.append(rule())
    story.append(Paragraph("Table 3.4 — Complete Technology Stack Summary",
                            styles["caption"]))
    tech_data = [
        ["Layer",          "Technology",        "Version",  "Purpose"],
        ["Hand Detection", "MediaPipe Hands",   "0.10.14",  "21 landmark keypoint extraction"],
        ["ML Framework",   "TensorFlow/Keras",  "2.16.1",   "LSTM model training and inference"],
        ["Data Science",   "NumPy",             "1.26.4",   "Keypoint array processing"],
        ["Data Science",   "scikit-learn",      "1.4.2",    "Train/test split, metrics"],
        ["Backend",        "FastAPI",           "0.111.0",  "REST + WebSocket API server"],
        ["Backend",        "Uvicorn",           "0.29.0",   "ASGI server for FastAPI"],
        ["Backend",        "Python-multipart",  "0.0.9",    "Multipart form data handling"],
        ["TTS",            "gTTS (Google TTS)", "2.5.1",    "Text-to-Speech MP3 generation"],
        ["Computer Vision","OpenCV (headless)", "4.9.0",    "Frame decoding and processing"],
        ["Frontend",       "React.js",          "18.3.1",   "Component-based UI"],
        ["Frontend",       "react-webcam",      "7.2.0",    "Webcam stream in browser"],
        ["Frontend",       "Framer Motion",     "11.2.10",  "Smooth sign transition animations"],
        ["Frontend",       "Lucide React",      "0.390.0",  "Icon library"],
        ["Styling",        "Custom CSS",        "—",        "Dark glassmorphism theme"],
        ["Runtime",        "Python",            "3.11+",    "Backend runtime environment"],
        ["Runtime",        "Node.js",           "18 LTS+",  "Frontend build and dev server"],
    ]
    story.append(left_table(tech_data,
        [PAGE_W*0.22, PAGE_W*0.22, PAGE_W*0.14, PAGE_W*0.42]))

    story.append(PageBreak())
    return story


def build_ch3_extra(styles):
    """Extra design content — data flow sequence diagram and UML-style tables."""
    from report_p1 import rule, thin_rule, sp, info_table, left_table
    from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle
    from reportlab.lib import colors as c
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    import math
    W2, _ = A4; PAGE_W2 = W2 - 50*mm
    NAVY  = c.HexColor("#1a237e"); BLUE = c.HexColor("#1565c0")
    LBLUE = c.HexColor("#1976d2"); WHITE = c.white
    GRAY  = c.HexColor("#424242"); GRAY_LN = c.HexColor("#e0e0e0")
    LGREEN= c.HexColor("#388e3c"); GRAY_BG = c.HexColor("#f5f5f5")
    GRAY_DK = c.HexColor("#212121")

    story = []

    story.append(Paragraph("3.8  Detailed Data Flow Diagram", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The sequence diagram below shows the exact data flow between the user, "
        "browser frontend, WebSocket channel, FastAPI backend, MediaPipe engine, "
        "and the LSTM model during a single prediction cycle:", styles["body"]))
    story.append(sp(8))

    # Sequence diagram
    dw = PAGE_W2; dh = 200
    seq = Drawing(dw, dh)
    seq.add(Rect(0, 0, dw, dh, fillColor=GRAY_BG, strokeColor=GRAY_LN))

    actors = ["User", "Browser\n(React)", "WebSocket", "FastAPI\nBackend",
              "MediaPipe", "LSTM\nModel"]
    n = len(actors); col_w = dw / n
    xs = [col_w*(i+0.5) for i in range(n)]
    top_y = dh - 16; bot_y = 12

    for i, (lbl, x) in enumerate(zip(actors, xs)):
        col = LBLUE if i in (1,2,3) else (LGREEN if i in (4,5) else NAVY)
        seq.add(Rect(x-30, top_y-14, 60, 18, fillColor=col,
                     strokeColor=WHITE, rx=3, ry=3))
        lines_a = lbl.split("\n")
        for j, ln in enumerate(lines_a):
            seq.add(String(x, top_y-5-j*8, ln, fontSize=7,
                           fontName="Helvetica-Bold", fillColor=WHITE,
                           textAnchor="middle"))
        seq.add(Line(x, top_y-14, x, bot_y,
                     strokeColor=GRAY_LN, strokeWidth=0.8,
                     strokeDashArray=[3,2]))

    messages = [
        (0, 1, dh-38, "Perform sign gesture"),
        (1, 2, dh-55, "Send frame (base64 JPEG)"),
        (2, 3, dh-72, "Receive frame bytes"),
        (3, 4, dh-89, "Process frame"),
        (4, 3, dh-106, "Return keypoints (126,)"),
        (3, 5, dh-120, "Predict (30,126)"),
        (5, 3, dh-134, "Return probs (40,)"),
        (3, 2, dh-148, "Send {sign, confidence}"),
        (2, 1, dh-162, "Display prediction"),
        (1, 0, dh-176, "Show sign + update sentence"),
    ]
    for src, dst, y, label in messages:
        x1 = xs[src]; x2 = xs[dst]
        seq.add(Line(x1, y, x2, y, strokeColor=NAVY, strokeWidth=1.0))
        ang = math.atan2(0, x2-x1)
        for da in (0.5, -0.5):
            ax = x2 - 5*math.cos(ang+da)
            ay = y  - 5*math.sin(ang+da)
            seq.add(Line(x2, y, ax, ay, strokeColor=NAVY, strokeWidth=1.0))
        mx = (x1+x2)/2
        seq.add(String(mx, y+3, label, fontSize=6.5,
                       fontName="Helvetica", fillColor=GRAY, textAnchor="middle"))

    story.append(seq)
    story.append(Paragraph("Fig 3.8 — Sequence Diagram: Single Prediction Cycle",
                            styles["caption"]))
    story.append(sp(10))

    story.append(Paragraph("3.9  State Machine — Prediction System", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The prediction subsystem operates as a finite state machine with the following states:",
        styles["body"]))
    story.append(sp(6))

    state_data = [
        ["State", "Description", "Entry Condition", "Exit Condition"],
        ["IDLE",
         "System waiting; no frames being sent",
         "App loaded or Stop clicked",
         "User clicks Start Detecting"],
        ["CONNECTING",
         "WebSocket connection being established",
         "Start Detecting clicked",
         "WS opens successfully (→ DETECTING) or fails (→ ERROR)"],
        ["DETECTING",
         "Frames being sent at 15fps; keypoints accumulated",
         "WS connection open",
         "30 frames accumulated (→ PREDICTING) or WS closed (→ IDLE)"],
        ["PREDICTING",
         "LSTM model running on 30-frame window",
         "Sequence buffer full",
         "Prediction returned (→ DISPLAYING or DETECTING if low conf)"],
        ["DISPLAYING",
         "Sign shown on screen; cooldown timer running",
         "Conf ≥ 75%; new sign or cooldown expired",
         "Cooldown elapsed (→ DETECTING)"],
        ["ERROR",
         "Connection or model error",
         "WS error or model not loaded",
         "User retries (→ CONNECTING)"],
    ]
    story.append(left_table(state_data,
        [PAGE_W2*0.16, PAGE_W2*0.26, PAGE_W2*0.27, PAGE_W2*0.31]))
    story.append(sp(10))

    story.append(Paragraph("3.10  Non-Functional Requirements", styles["h2"]))
    story.append(rule())
    nfr_data = [
        ["NFR Category", "Requirement", "Target", "Achieved?"],
        ["Performance",  "End-to-end latency",          "< 200 ms",  "✓  ~67 ms"],
        ["Performance",  "Frame capture rate",           "≥ 10 fps",  "✓  15 fps"],
        ["Accuracy",     "Test accuracy",                "≥ 90%",     "✓  96.8%"],
        ["Accuracy",     "Confidence threshold",         "≥ 75%",     "✓  Configurable"],
        ["Usability",    "No specialised hardware",      "Webcam only","✓  Standard RGB"],
        ["Usability",    "Browser-based access",         "No install", "✓  React web app"],
        ["Usability",    "TTS output",                   "Required",   "✓  gTTS + fallback"],
        ["Reliability",  "Auto-reconnect on WS drop",    "Required",   "✓  Implemented"],
        ["Scalability",  "Support 40+ signs",            "40 minimum", "✓  40 signs"],
        ["Compatibility","Modern browsers",               "Chrome/FF",  "✓  Both supported"],
        ["Portability",  "OS independence",              "Win/Mac/Linux","✓  All supported"],
    ]
    story.append(info_table(nfr_data,
        [PAGE_W2*0.22, PAGE_W2*0.28, PAGE_W2*0.22, PAGE_W2*0.28]))

    from reportlab.platypus import PageBreak
    story.append(PageBreak())
    return story
