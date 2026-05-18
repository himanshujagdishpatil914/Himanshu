# 🤟 SignAI — Real-time AI Sign Language Translator

> **Final Year Project** | AI-powered real-time sign language detection with Text-to-Speech and Sentence Builder

![Tech Stack](https://img.shields.io/badge/Stack-React%20%7C%20FastAPI%20%7C%20TensorFlow%20%7C%20MediaPipe-6366f1?style=for-the-badge)
![Signs](https://img.shields.io/badge/Signs-40%20Supported-22c55e?style=for-the-badge)
![Accuracy](https://img.shields.io/badge/Accuracy-95%25%2B-f59e0b?style=for-the-badge)

---

## 📸 Features

| Feature | Description |
|---------|-------------|
| 🎥 **Real-time Detection** | Webcam-based live sign detection via WebSocket |
| 🧠 **LSTM Model** | Stacked LSTM neural network trained on 40 signs |
| 🔊 **Text-to-Speech** | gTTS backend + browser fallback |
| 💬 **Sentence Builder** | Build full sentences from detected signs |
| 📝 **Word + Sentence Mode** | Toggle between word chips and full sentence view |
| 📖 **Sign Dictionary** | Browse all 40 supported signs with search |
| 📊 **Confidence Meter** | Real-time confidence bar + Top-5 predictions |
| 🌙 **Dark UI** | Modern glassmorphism dark theme |

---

## 🗂️ Project Structure

```
sign-language-translator/
├── backend/
│   ├── app.py                    # FastAPI server (WS + TTS + REST)
│   ├── requirements.txt          # Python dependencies
│   ├── data/
│   │   ├── sign_model.h5         # Trained model (generated)
│   │   ├── label_encoder.npy     # Sign labels (generated)
│   │   ├── signs.json            # Sign list
│   │   └── keypoints/            # Training data (generated)
│   └── model/
│       ├── collect_data.py       # Data collection via webcam
│       └── train.py              # Model training (LSTM)
└── frontend/
    ├── public/index.html
    └── src/
        ├── App.jsx
        ├── index.js
        ├── styles/App.css
        └── components/
            ├── Camera.jsx         # Webcam + WebSocket client
            ├── SignDisplay.jsx    # Current sign + confidence
            ├── SentenceBuilder.jsx # Word chips + TTS + modes
            ├── SignList.jsx       # Sign dictionary
            ├── Header.jsx
            └── StatusBar.jsx
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Webcam

---

### Step 1 — Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### Step 2 — Collect Training Data

```bash
cd backend/model
python collect_data.py
```

**Controls:**
- `ENTER` — Record one 30-frame sample
- `N` — Next sign
- `P` — Previous sign
- `Q` — Quit

> Collect **200 samples per sign** for best accuracy. Vary lighting and hand positions!

---

### Step 3 — Train the Model

```bash
cd backend/model
python train.py
```

This will:
- Load all collected keypoint sequences
- Train a **3-layer LSTM** with BatchNorm + Dropout
- Save `backend/data/sign_model.h5` and `backend/data/label_encoder.npy`
- Print test accuracy and classification report

> Expected accuracy: **93–98%** with 200 samples/sign

---

### Step 4 — Start Backend

```bash
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

API will be live at `http://localhost:8000`

---

### Step 5 — Start Frontend

```bash
cd frontend
cp .env.example .env
npm install
npm start
```

App will open at `http://localhost:3000`

---

## 🧠 How the AI Works

```
Webcam Frame (640×480)
       ↓
MediaPipe Hands
  → 21 landmarks (x, y, z)
  → 63-dim keypoint vector
       ↓
Sliding window (30 frames)
       ↓
┌──────────────────────────┐
│  LSTM (128) + BN + Drop  │
│  LSTM (256) + BN + Drop  │
│  LSTM (128) + BN + Drop  │
│  Dense (256) → ReLU      │
│  Dense (128) → ReLU      │
│  Dense (40)  → Softmax   │
└──────────────────────────┘
       ↓
Predicted Sign + Confidence
       ↓
Sentence Builder + TTS
```

---

## 🤟 Supported Signs (40 Total)

| Category | Signs |
|----------|-------|
| **Common Phrases** | hello, yes, no, thankyou, please, sorry, help, good, bad, stop |
| **Expressions** | iloveyou, goodmorning, goodnight, howareyou, fine |
| **Actions** | eat, drink, sleep, come, go |
| **Alphabet** | A, B, C, D, E, F, G, H, I, J |
| **Numbers** | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 |

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `WS` | `/ws/predict` | Real-time frame prediction |
| `POST` | `/api/tts` | Convert text to speech (MP3) |
| `GET` | `/api/signs` | List all supported signs |
| `GET` | `/api/health` | Server health check |

### TTS Request Body
```json
{
  "text": "hello thank you",
  "lang": "en",
  "slow": false
}
```

---

## 📈 Improving Accuracy

| Tip | Impact |
|-----|--------|
| Collect 200+ samples per sign | ⬆⬆⬆ |
| Vary lighting conditions | ⬆⬆ |
| Use consistent background | ⬆⬆ |
| Vary hand size/angle | ⬆⬆ |
| Run more epochs (200+) | ⬆ |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Hand Detection | MediaPipe Hands |
| ML Framework | TensorFlow / Keras |
| Model Type | Stacked LSTM |
| Backend | FastAPI + WebSockets |
| TTS | gTTS (Google TTS) |
| Frontend | React 18 |
| Animations | Framer Motion |
| Camera | react-webcam |
| Styling | Custom CSS (Dark theme) |

---

## 👨‍💻 Author

**Himanshu Jagdish Patil**  
Final Year Project — AI Sign Language Translator

---

## 📄 License

MIT License — Free to use for academic and personal projects.
