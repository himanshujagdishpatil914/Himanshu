from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import PageBreak

OUTPUT = "SignAI_Setup_Guide.pdf"

# ── Colours ───────────────────────────────────────────────────────────────────
INDIGO      = colors.HexColor("#6366f1")
INDIGO_DARK = colors.HexColor("#4338ca")
SLATE_900   = colors.HexColor("#0f172a")
SLATE_800   = colors.HexColor("#1e293b")
SLATE_700   = colors.HexColor("#273548")
SLATE_400   = colors.HexColor("#94a3b8")
WHITE       = colors.white
GREEN       = colors.HexColor("#22c55e")
AMBER       = colors.HexColor("#f59e0b")
RED         = colors.HexColor("#ef4444")
CYAN        = colors.HexColor("#06b6d4")

W, H = A4

def make_styles():
    base = getSampleStyleSheet()

    def ps(name, **kw):
        return ParagraphStyle(name, **kw)

    return {
        "cover_title": ps("cover_title",
            fontSize=32, fontName="Helvetica-Bold",
            textColor=WHITE, alignment=TA_CENTER, spaceAfter=6),
        "cover_sub": ps("cover_sub",
            fontSize=14, fontName="Helvetica",
            textColor=SLATE_400, alignment=TA_CENTER, spaceAfter=4),
        "cover_badge": ps("cover_badge",
            fontSize=11, fontName="Helvetica-Bold",
            textColor=INDIGO, alignment=TA_CENTER, spaceAfter=2),
        "h1": ps("h1",
            fontSize=18, fontName="Helvetica-Bold",
            textColor=INDIGO, spaceBefore=14, spaceAfter=6),
        "h2": ps("h2",
            fontSize=13, fontName="Helvetica-Bold",
            textColor=WHITE, spaceBefore=10, spaceAfter=4),
        "h3": ps("h3",
            fontSize=11, fontName="Helvetica-Bold",
            textColor=CYAN, spaceBefore=8, spaceAfter=3),
        "body": ps("body",
            fontSize=10, fontName="Helvetica",
            textColor=SLATE_400, spaceBefore=2, spaceAfter=2,
            leading=15),
        "code": ps("code",
            fontSize=9, fontName="Courier",
            textColor=GREEN, backColor=SLATE_800,
            spaceBefore=2, spaceAfter=2, leading=13,
            leftIndent=10, rightIndent=10,
            borderPadding=(6, 8, 6, 8)),
        "tip": ps("tip",
            fontSize=9, fontName="Helvetica",
            textColor=AMBER, spaceBefore=2, spaceAfter=2, leading=13,
            leftIndent=8),
        "warn": ps("warn",
            fontSize=9, fontName="Helvetica",
            textColor=RED, spaceBefore=2, spaceAfter=2, leading=13,
            leftIndent=8),
        "bullet": ps("bullet",
            fontSize=10, fontName="Helvetica",
            textColor=SLATE_400, spaceBefore=1, spaceAfter=1,
            leading=14, leftIndent=16, bulletIndent=6),
    }


def divider(color=INDIGO, thickness=1):
    return HRFlowable(width="100%", thickness=thickness,
                      color=color, spaceAfter=6, spaceBefore=6)


def code_block(text, styles):
    lines = text.strip().split("\n")
    rows  = [[Paragraph(l.replace(" ", "&nbsp;"), styles["code"])] for l in lines]
    t = Table(rows, colWidths=[W - 60*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), SLATE_800),
        ("BOX",        (0,0), (-1,-1), 1, INDIGO_DARK),
        ("ROUNDEDCORNERS", [6]),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
    ]))
    return t


def info_table(rows, col_widths, styles, header=None):
    data   = []
    ts     = [
        ("BACKGROUND", (0,0), (-1,-1), SLATE_800),
        ("GRID",       (0,0), (-1,-1), 0.5, SLATE_700),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [SLATE_800, SLATE_900]),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("FONTNAME",   (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE",   (0,0), (-1,-1), 9),
        ("TEXTCOLOR",  (0,0), (-1,-1), SLATE_400),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ]
    if header:
        data.append([Paragraph(f"<b>{h}</b>", ParagraphStyle("th",
            fontSize=9, fontName="Helvetica-Bold", textColor=WHITE)) for h in header])
        ts += [
            ("BACKGROUND", (0,0), (-1,0), INDIGO_DARK),
            ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
        ]
    for r in rows:
        data.append([Paragraph(str(c), ParagraphStyle("td",
            fontSize=9, fontName="Helvetica", textColor=SLATE_400, leading=13)) for c in r])
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle(ts))
    return t



def build_cover(story, styles):
    story.append(Spacer(1, 30*mm))
    # Big emoji-style header
    story.append(Paragraph("🤟", ParagraphStyle("emoji",
        fontSize=48, alignment=TA_CENTER, spaceAfter=8)))
    story.append(Paragraph("SignAI", styles["cover_title"]))
    story.append(Paragraph("Real-time AI Sign Language Translator", styles["cover_sub"]))
    story.append(Spacer(1, 6*mm))
    story.append(divider(INDIGO, 2))
    story.append(Spacer(1, 4*mm))

    badges = [
        ["🎓 Final Year Project", "🧠 AI / Deep Learning", "40 Signs Supported"],
        ["95%+ Accuracy",         "🔊 Text-to-Speech",     "💬 Sentence Builder"],
    ]
    for row in badges:
        story.append(Paragraph("    ".join(row), styles["cover_badge"]))
        story.append(Spacer(1, 2*mm))

    story.append(Spacer(1, 10*mm))
    story.append(divider(INDIGO_DARK))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("👤  Himanshu Jagdish Patil", ParagraphStyle("author",
        fontSize=11, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER)))
    story.append(Paragraph("BTech CSE (AI &amp; ML)  |  Final Year", ParagraphStyle("dept",
        fontSize=10, fontName="Helvetica", textColor=SLATE_400, alignment=TA_CENTER, spaceAfter=2)))
    story.append(Spacer(1, 6*mm))

    # Tech stack row
    tech = ["Python 3.11", "FastAPI", "TensorFlow", "MediaPipe", "React 18", "gTTS"]
    tech_data = [[Paragraph(t, ParagraphStyle("tech",
        fontSize=8, fontName="Helvetica-Bold", textColor=INDIGO, alignment=TA_CENTER)) for t in tech]]
    tech_table = Table(tech_data, colWidths=[(W-60*mm)/6]*6)
    tech_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), SLATE_800),
        ("BOX",           (0,0), (-1,-1), 1, INDIGO_DARK),
        ("INNERGRID",     (0,0), (-1,-1), 0.5, SLATE_700),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(tech_table)
    story.append(PageBreak())


def build_overview(story, styles):
    story.append(Paragraph("📌  Project Overview", styles["h1"]))
    story.append(divider())
    story.append(Paragraph(
        "SignAI is a real-time sign language translator that uses a webcam to detect hand signs "
        "and converts them into text and speech. It is built with a React frontend, FastAPI backend, "
        "MediaPipe for hand landmark detection, and a stacked LSTM neural network for classification.",
        styles["body"]))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("How It Works", styles["h2"]))
    flow = [
        ["Step", "Component",         "Description"],
        ["1",    "Webcam",            "Captures live video at 15 fps"],
        ["2",    "MediaPipe Hands",   "Extracts 21 hand landmarks (63 values)"],
        ["3",    "Sliding Window",    "Groups 30 frames into one sequence"],
        ["4",    "LSTM Model",        "Predicts sign with confidence score"],
        ["5",    "FastAPI WebSocket", "Streams prediction to React frontend"],
        ["6",    "Sentence Builder",  "Builds words into full sentences"],
        ["7",    "gTTS / Browser TTS","Speaks the sentence aloud"],
    ]
    story.append(info_table(flow[1:],
        [15*mm, 45*mm, W-60*mm-15*mm-45*mm], styles, header=flow[0]))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Supported Signs (40 Total)", styles["h2"]))
    signs = [
        ["Category",        "Signs"],
        ["Common Phrases",  "hello, yes, no, thankyou, please, sorry, help, good, bad, stop"],
        ["Expressions",     "iloveyou, goodmorning, goodnight, howareyou, fine"],
        ["Actions",         "eat, drink, sleep, come, go"],
        ["Alphabet",        "A, B, C, D, E, F, G, H, I, J"],
        ["Numbers",         "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"],
    ]
    story.append(info_table(signs[1:], [45*mm, W-60*mm-45*mm], styles, header=signs[0]))
    story.append(PageBreak())


def build_prerequisites(story, styles):
    story.append(Paragraph("⚙️  Prerequisites", styles["h1"]))
    story.append(divider())
    story.append(Paragraph(
        "Install the following software before starting. All are free and open source.",
        styles["body"]))
    story.append(Spacer(1, 3*mm))

    prereqs = [
        ["Software",    "Version",   "Download URL",                   "Purpose"],
        ["Python",      "3.11+",     "python.org/downloads",           "Backend + ML"],
        ["Node.js",     "18 LTS+",   "nodejs.org",                     "Frontend"],
        ["Git",         "Latest",    "git-scm.com",                    "Clone repo"],
        ["Webcam",      "Any",       "Built-in or USB",                "Data collection"],
    ]
    story.append(info_table(prereqs[1:],
        [30*mm, 22*mm, 65*mm, W-60*mm-30*mm-22*mm-65*mm],
        styles, header=prereqs[0]))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Step 1 — Install Python 3.11", styles["h2"]))
    story.append(Paragraph("1.  Go to python.org/downloads and download Python 3.11", styles["bullet"]))
    story.append(Paragraph("2.  During install — CHECK ✅ <b>'Add Python to PATH'</b>", styles["bullet"]))
    story.append(Paragraph("3.  Verify in terminal:", styles["bullet"]))
    story.append(code_block("python --version\n# Expected: Python 3.11.x", styles))

    story.append(Paragraph("Step 2 — Install Node.js 18+", styles["h2"]))
    story.append(Paragraph("1.  Go to nodejs.org and download the LTS version", styles["bullet"]))
    story.append(Paragraph("2.  Install normally with default settings", styles["bullet"]))
    story.append(Paragraph("3.  Verify:", styles["bullet"]))
    story.append(code_block("node --version    # Expected: v18.x.x or v20.x.x\nnpm --version     # Expected: 9.x.x or 10.x.x", styles))

    story.append(Paragraph("Step 3 — Install Git", styles["h2"]))
    story.append(Paragraph("1.  Go to git-scm.com and install with default settings", styles["bullet"]))
    story.append(Paragraph("2.  Verify:", styles["bullet"]))
    story.append(code_block("git --version", styles))
    story.append(PageBreak())



def build_setup(story, styles):
    story.append(Paragraph("📥  Step 4 — Clone the Project", styles["h1"]))
    story.append(divider())
    story.append(code_block(
        "git clone https://github.com/himanshujagdishpatil914/Himanshu.git\ncd Himanshu", styles))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Your folder structure after cloning:", styles["body"]))
    story.append(code_block(
        "Himanshu/\n"
        "├── backend/\n"
        "│   ├── app.py\n"
        "│   ├── requirements.txt\n"
        "│   └── model/\n"
        "│       ├── collect_data.py\n"
        "│       └── train.py\n"
        "└── frontend/\n"
        "    ├── package.json\n"
        "    └── src/", styles))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("🐍  Step 5 — Setup Python Backend", styles["h1"]))
    story.append(divider())

    story.append(Paragraph("5.1  Navigate to backend folder", styles["h3"]))
    story.append(code_block("cd backend", styles))

    story.append(Paragraph("5.2  Create a Python Virtual Environment", styles["h3"]))
    story.append(code_block(
        "python -m venv venv\n\n"
        "# Activate — Windows:\n"
        "venv\\Scripts\\activate\n\n"
        "# Activate — Mac / Linux:\n"
        "source venv/bin/activate", styles))
    story.append(Paragraph(
        "✅  You will see (venv) at the start of your terminal line when activated.",
        styles["tip"]))

    story.append(Paragraph("5.3  Install Python Packages", styles["h3"]))
    story.append(code_block("pip install -r requirements.txt", styles))
    story.append(Paragraph(
        "⏳  This takes 5–10 minutes. TensorFlow and MediaPipe are large packages.",
        styles["tip"]))

    story.append(Paragraph("5.4  Verify Installation", styles["h3"]))
    story.append(code_block(
        'python -c "import mediapipe; import tensorflow; print(\'All good!\')"\n'
        "# Expected output: All good!", styles))
    story.append(PageBreak())


def build_data_collection(story, styles):
    story.append(Paragraph("📷  Step 6 — Collect Training Data", styles["h1"]))
    story.append(divider())
    story.append(Paragraph(
        "⚠  You need a working webcam for this step.", styles["warn"]))
    story.append(Spacer(1, 2*mm))
    story.append(code_block(
        "# Make sure you are in backend/ with venv activated\n"
        "cd model\n"
        "python collect_data.py", styles))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Keyboard Controls", styles["h2"]))
    controls = [
        ["Key",    "Action"],
        ["ENTER",  "Record one sample (30 frames)"],
        ["N",      "Move to next sign"],
        ["P",      "Move to previous sign"],
        ["Q",      "Quit data collection"],
    ]
    story.append(info_table(controls[1:], [30*mm, W-60*mm-30*mm], styles, header=controls[0]))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("How Many Samples to Collect", styles["h2"]))
    samples = [
        ["Samples / Sign", "Expected Accuracy", "Time (40 signs)"],
        ["50",             "~80%",              "~10 minutes"],
        ["100",            "~90%",              "~20 minutes"],
        ["200 (Recommended)", "~95–98%",        "~40 minutes"],
    ]
    story.append(info_table(samples[1:],
        [55*mm, 50*mm, W-60*mm-55*mm-50*mm], styles, header=samples[0]))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Tips for High Quality Data", styles["h2"]))
    tips = [
        "✅  Use good lighting — face a window or bright lamp",
        "✅  Use a plain background — white or light-coloured wall",
        "✅  Slightly vary your hand angle and distance each sample",
        "✅  Keep signs clear and deliberate",
        "❌  Do not collect in dark rooms",
        "❌  Do not rush — blurry frames reduce accuracy",
    ]
    for t in tips:
        story.append(Paragraph(t, styles["bullet"]))
    story.append(PageBreak())


def build_training(story, styles):
    story.append(Paragraph("🧠  Step 7 — Train the AI Model", styles["h1"]))
    story.append(divider())
    story.append(code_block(
        "# Still inside backend/model/ with venv activated\n"
        "python train.py", styles))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Expected Terminal Output", styles["h2"]))
    story.append(code_block(
        "[INFO] Loading data for 40 signs ...\n"
        "  hello                → 200 samples\n"
        "  yes                  → 200 samples\n"
        "  ...\n"
        "[INFO] Dataset: 8000 samples, shape (8000, 30, 63)\n"
        "[INFO] Train: 5780 | Val: 1020 | Test: 1200\n"
        "[INFO] Training ...\n"
        "Epoch 1/200  - accuracy: 0.43\n"
        "Epoch 10/200 - accuracy: 0.78\n"
        "Epoch 50/200 - accuracy: 0.96\n"
        "...\n"
        "[RESULT] Test Accuracy: 96.5%  |  Loss: 0.1243\n"
        "[SAVED]  Model   -> backend/data/sign_model.h5  ✅\n"
        "[SAVED]  Labels  -> backend/data/label_encoder.npy", styles))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "⏳  Training takes 10–30 minutes depending on your hardware.",
        styles["tip"]))
    story.append(Paragraph(
        "💡  A GPU (NVIDIA) will speed up training significantly.",
        styles["tip"]))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Files Created After Training", styles["h2"]))
    story.append(code_block(
        "backend/data/\n"
        "├── sign_model.h5          ← The trained AI brain\n"
        "├── label_encoder.npy      ← Sign label names\n"
        "└── training_history.json  ← Accuracy/loss history", styles))
    story.append(PageBreak())


def build_backend(story, styles):
    story.append(Paragraph("⚡  Step 8 — Start the Backend Server", styles["h1"]))
    story.append(divider())
    story.append(code_block(
        "# Go back to backend/ folder\n"
        "cd ..          # (if you are in backend/model/)\n\n"
        "# Make sure venv is still active, then:\n"
        "uvicorn app:app --host 0.0.0.0 --port 8000 --reload", styles))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Expected Output", styles["h2"]))
    story.append(code_block(
        "INFO:  Started server process\n"
        "INFO:  Waiting for application startup.\n"
        "INFO:  Model loaded | 40 classes   ✅\n"
        "INFO:  Application startup complete.\n"
        "INFO:  Uvicorn running on http://0.0.0.0:8000", styles))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Test the Server", styles["h2"]))
    story.append(Paragraph(
        "Open your browser and visit the following URL to confirm the server is running:",
        styles["body"]))
    story.append(code_block("http://localhost:8000/api/health", styles))
    story.append(Paragraph("You should see:", styles["body"]))
    story.append(code_block(
        '{\n'
        '  "status":       "ok",\n'
        '  "model_loaded": true,\n'
        '  "sign_count":   40\n'
        '}', styles))
    story.append(Paragraph(
        "🔴  Keep this terminal open — do not close it while using the app!",
        styles["warn"]))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Available API Endpoints", styles["h2"]))
    endpoints = [
        ["Method",  "Endpoint",        "Description"],
        ["WS",      "/ws/predict",     "Real-time sign prediction via WebSocket"],
        ["POST",    "/api/tts",        "Convert text to speech (returns MP3)"],
        ["GET",     "/api/signs",      "List all supported signs"],
        ["GET",     "/api/health",     "Server health check"],
    ]
    story.append(info_table(endpoints[1:],
        [20*mm, 45*mm, W-60*mm-20*mm-45*mm], styles, header=endpoints[0]))
    story.append(PageBreak())


def build_frontend(story, styles):
    story.append(Paragraph("⚛️   Step 9 — Setup and Start Frontend", styles["h1"]))
    story.append(divider())
    story.append(Paragraph(
        "Open a NEW terminal window (keep the backend terminal running!).",
        styles["warn"]))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("9.1  Go to frontend folder", styles["h3"]))
    story.append(code_block("cd Himanshu/frontend", styles))

    story.append(Paragraph("9.2  Install Node packages", styles["h3"]))
    story.append(code_block("npm install", styles))
    story.append(Paragraph("⏳  Takes 2–5 minutes.", styles["tip"]))

    story.append(Paragraph("9.3  Start the app", styles["h3"]))
    story.append(code_block("npm start", styles))

    story.append(Paragraph("Expected Output", styles["h2"]))
    story.append(code_block(
        "Compiled successfully!\n\n"
        "You can now view sign-language-translator in the browser.\n\n"
        "  Local:    http://localhost:3000\n"
        "  Network:  http://192.168.x.x:3000", styles))
    story.append(Paragraph(
        "✅  The browser will automatically open http://localhost:3000",
        styles["tip"]))
    story.append(PageBreak())


def build_usage(story, styles):
    story.append(Paragraph("🎮  Step 10 — Using the App", styles["h1"]))
    story.append(divider())

    story.append(Paragraph("Tab 1 — 🤟 Translator", styles["h2"]))
    steps = [
        ["1", "Click  ▶ Start Detecting  button"],
        ["2", "Allow camera access when the browser asks"],
        ["3", "Show your hand sign clearly to the camera"],
        ["4", "The detected sign appears with a confidence bar"],
        ["5", "Signs auto-add to the Sentence Builder below"],
        ["6", "Click  🔊 Speak  to hear the full sentence"],
        ["7", "Click  ⌫ Undo  to remove the last word"],
        ["8", "Click  🗑 Clear  to start a new sentence"],
    ]
    story.append(info_table(steps, [12*mm, W-60*mm-12*mm], styles))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Tab 2 — 📖 Sign List", styles["h2"]))
    story.append(Paragraph("Browse all 40 supported signs organised by category.", styles["body"]))
    story.append(Paragraph("Use the search box to quickly find a specific sign.", styles["body"]))
    story.append(Paragraph("Signs are grouped into: Common Phrases, Expressions, Actions, Alphabet, Numbers.", styles["body"]))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Sentence Builder Modes", styles["h2"]))
    modes = [
        ["Mode",      "Description"],
        ["🔤 Words",  "Displays detected signs as individual coloured chips. Click any chip to remove it."],
        ["📝 Sentence","Joins all chips into a full readable sentence. Use Speak to hear it."],
    ]
    story.append(info_table(modes[1:], [35*mm, W-60*mm-35*mm], styles, header=modes[0]))
    story.append(PageBreak())


def build_daily_run(story, styles):
    story.append(Paragraph("🔁  Daily Running Cheatsheet", styles["h1"]))
    story.append(divider())
    story.append(Paragraph(
        "After the first-time setup, use these two commands every time you want to run the project.",
        styles["body"]))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("Terminal 1 — Start Backend", styles["h2"]))
    story.append(code_block(
        "cd Himanshu/backend\n\n"
        "# Windows:\n"
        "venv\\Scripts\\activate\n\n"
        "# Mac / Linux:\n"
        "source venv/bin/activate\n\n"
        "uvicorn app:app --port 8000", styles))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Terminal 2 — Start Frontend", styles["h2"]))
    story.append(code_block(
        "cd Himanshu/frontend\n"
        "npm start", styles))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Then open your browser at  http://localhost:3000  🎉", styles["tip"]))
    story.append(PageBreak())


def build_troubleshooting(story, styles):
    story.append(Paragraph("❌  Common Errors and Fixes", styles["h1"]))
    story.append(divider())

    errors = [
        ["Error / Problem",           "Fix"],
        ["ModuleNotFoundError",        "Run:  pip install -r requirements.txt  inside venv"],
        ["Camera not found / denied",  "Click Allow in browser camera permission popup"],
        ["WebSocket connection failed","Make sure backend is running on port 8000"],
        ["npm: command not found",     "Install Node.js from nodejs.org"],
        ["venv not activated",         "Run:  venv\\Scripts\\activate  (Windows)  or  source venv/bin/activate"],
        ["Model not loaded (demo mode)","Run train.py first to generate sign_model.h5"],
        ["Port 8000 already in use",   "Use:  uvicorn app:app --port 8001  and update frontend .env"],
        ["Low accuracy (<80%)",        "Collect more samples (200/sign) with better lighting"],
        ["App shows blank page",       "Check browser console for errors, ensure npm start ran successfully"],
    ]
    story.append(info_table(errors[1:],
        [65*mm, W-60*mm-65*mm], styles, header=errors[0]))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("💻  Minimum System Requirements", styles["h1"]))
    story.append(divider())
    reqs = [
        ["Component", "Minimum",              "Recommended"],
        ["RAM",        "8 GB",                "16 GB"],
        ["CPU",        "Intel i5 / Ryzen 5",  "Intel i7 / Ryzen 7"],
        ["GPU",        "Not required",         "NVIDIA (speeds up training)"],
        ["Storage",    "5 GB free",            "10 GB free"],
        ["Webcam",     "Any webcam",           "HD 1080p"],
        ["OS",         "Windows 10 / Ubuntu 20 / macOS 11",
                        "Windows 11 / Ubuntu 22 / macOS 13"],
    ]
    story.append(info_table(reqs[1:],
        [30*mm, 60*mm, W-60*mm-30*mm-60*mm], styles, header=reqs[0]))
    story.append(PageBreak())


def build_accuracy_tips(story, styles):
    story.append(Paragraph("📈  Improving Accuracy", styles["h1"]))
    story.append(divider())
    tips = [
        ["Tip",                          "Impact"],
        ["Collect 200+ samples per sign",           "⬆⬆⬆ High"],
        ["Vary lighting conditions",                "⬆⬆ Medium"],
        ["Use plain background",                    "⬆⬆ Medium"],
        ["Vary hand size and angle",                "⬆⬆ Medium"],
        ["Run more training epochs (200+)",         "⬆  Low–Medium"],
        ["Use GPU for training",                    "⬆  Speed only"],
        ["Add data augmentation (flip/rotate)",     "⬆⬆ Medium"],
    ]
    story.append(info_table(tips[1:], [110*mm, W-60*mm-110*mm], styles, header=tips[0]))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("📦  Recommended Dataset (Kaggle)", styles["h1"]))
    story.append(divider())
    story.append(Paragraph(
        "To boost accuracy further, use a pre-built dataset alongside your own collected data.",
        styles["body"]))
    story.append(Spacer(1, 2*mm))
    datasets = [
        ["Dataset",                        "Signs", "Format",             "Link"],
        ["Google ASL Signs (Kaggle)",       "250",   "MediaPipe landmarks","kaggle.com/competitions/asl-signs"],
        ["Sign Language MNIST",             "24",    "CSV pixel images",   "kaggle.com/datasets/datamunge/sign-language-mnist"],
        ["ASL Alphabet (Kaggle)",           "29",    "JPG images",         "kaggle.com/datasets/grassknoted/asl-alphabet"],
    ]
    story.append(info_table(datasets[1:],
        [55*mm, 15*mm, 40*mm, W-60*mm-55*mm-15*mm-40*mm],
        styles, header=datasets[0]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Download Command:", styles["h3"]))
    story.append(code_block(
        "pip install kaggle\n"
        "# Place kaggle.json in ~/.kaggle/\n\n"
        "# Best option — pre-extracted MediaPipe landmarks:\n"
        "kaggle competitions download -c asl-signs -p ./backend/data/\n\n"
        "# Easy starter:\n"
        "kaggle datasets download -d datamunge/sign-language-mnist -p ./backend/data/",
        styles))
    story.append(PageBreak())


def build_final_page(story, styles):
    story.append(Spacer(1, 20*mm))
    story.append(Paragraph("🎉  You're All Set!", ParagraphStyle("done",
        fontSize=24, fontName="Helvetica-Bold",
        textColor=GREEN, alignment=TA_CENTER, spaceAfter=6)))
    story.append(divider(GREEN, 2))
    story.append(Spacer(1, 6*mm))

    summary = [
        ["✅", "Python backend installed and running"],
        ["✅", "Training data collected via webcam"],
        ["✅", "LSTM model trained with 95%+ accuracy"],
        ["✅", "FastAPI server running on port 8000"],
        ["✅", "React frontend running on port 3000"],
        ["✅", "Real-time sign detection working"],
        ["✅", "Text-to-Speech enabled"],
        ["✅", "Sentence Builder working"],
    ]
    t = Table(summary, colWidths=[12*mm, W-60*mm-12*mm])
    t.setStyle(TableStyle([
        ("TEXTCOLOR",     (0,0), (0,-1), GREEN),
        ("TEXTCOLOR",     (1,0), (1,-1), WHITE),
        ("FONTNAME",      (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE",      (0,0), (-1,-1), 11),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 10*mm))
    story.append(divider(INDIGO_DARK))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        "👤  Himanshu Jagdish Patil  |  BTech CSE (AI &amp; ML)",
        ParagraphStyle("footer_name", fontSize=10, fontName="Helvetica-Bold",
            textColor=WHITE, alignment=TA_CENTER)))
    story.append(Paragraph(
        "📧  himanshujagdishpatil914@gmail.com",
        ParagraphStyle("footer_email", fontSize=9, fontName="Helvetica",
            textColor=SLATE_400, alignment=TA_CENTER, spaceAfter=2)))
    story.append(Paragraph(
        "🔗  github.com/himanshujagdishpatil914/Himanshu",
        ParagraphStyle("footer_gh", fontSize=9, fontName="Helvetica",
            textColor=INDIGO, alignment=TA_CENTER)))


def on_page(canvas, doc):
    """Draw header and footer on every page."""
    canvas.saveState()
    W, H = A4
    # Header bar
    canvas.setFillColor(SLATE_900)
    canvas.rect(0, H - 18*mm, W, 18*mm, fill=1, stroke=0)
    canvas.setFillColor(INDIGO)
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(20*mm, H - 12*mm, "🤟  SignAI — Real-time AI Sign Language Translator")
    canvas.setFillColor(SLATE_400)
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(W - 20*mm, H - 12*mm, "Final Year Project  |  Himanshu Jagdish Patil")
    # Footer bar
    canvas.setFillColor(SLATE_900)
    canvas.rect(0, 0, W, 14*mm, fill=1, stroke=0)
    canvas.setFillColor(SLATE_400)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(20*mm, 5*mm, "Setup Guide — Step by Step")
    canvas.drawRightString(W - 20*mm, 5*mm, f"Page {doc.page}")
    canvas.restoreState()


def main():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=30*mm, rightMargin=30*mm,
        topMargin=22*mm,  bottomMargin=18*mm,
        title="SignAI Setup Guide",
        author="Himanshu Jagdish Patil",
        subject="Step-by-step guide to run the AI Sign Language Translator",
    )

    styles = make_styles()
    story  = []

    build_cover(story, styles)
    build_overview(story, styles)
    build_prerequisites(story, styles)
    build_setup(story, styles)
    build_data_collection(story, styles)
    build_training(story, styles)
    build_backend(story, styles)
    build_frontend(story, styles)
    build_usage(story, styles)
    build_daily_run(story, styles)
    build_troubleshooting(story, styles)
    build_accuracy_tips(story, styles)
    build_final_page(story, styles)

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"[DONE] PDF saved → {OUTPUT}")


if __name__ == "__main__":
    main()
