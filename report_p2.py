"""
SignAI Project Report — Part 2
Table of Contents, List of Figures, List of Tables, Chapter 1 Introduction
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

W, H = A4
PAGE_W = W - 50*mm

NAVY  = colors.HexColor("#1a237e")
BLUE  = colors.HexColor("#1565c0")
LBLUE = colors.HexColor("#1976d2")
GRAY_DK = colors.HexColor("#212121")
GRAY    = colors.HexColor("#424242")
GRAY_LT = colors.HexColor("#757575")
GRAY_BG = colors.HexColor("#f5f5f5")
GRAY_LN = colors.HexColor("#e0e0e0")
WHITE   = colors.white
GREEN   = colors.HexColor("#2e7d32")
TEAL    = colors.HexColor("#00695c")
AMBER   = colors.HexColor("#e65100")


# ─── TABLE OF CONTENTS ────────────────────────────────────────────────────────
def build_toc(styles):
    story = []
    story.append(Spacer(1, 15))
    story.append(Paragraph("TABLE OF CONTENTS", styles["pg_label"]))

    from report_p1 import rule, thin_rule, sp
    story.append(rule(NAVY, 2))
    story.append(sp(10))

    toc_entries = [
        ("", "Certificate", "ii"),
        ("", "Acknowledgement", "iii"),
        ("", "Abstract", "iv"),
        ("", "Table of Contents", "v"),
        ("", "List of Figures", "vi"),
        ("", "List of Tables", "vii"),
        ("1", "Introduction", "1"),
        ("1.1", "Background and Motivation", "1"),
        ("1.2", "Problem Statement", "2"),
        ("1.3", "Objectives of the Project", "3"),
        ("1.4", "Scope of the Project", "4"),
        ("1.5", "Organisation of the Report", "4"),
        ("2", "Literature Review", "5"),
        ("2.1", "Overview of Sign Language Recognition Systems", "5"),
        ("2.2", "Traditional Image-Based Approaches", "6"),
        ("2.3", "Deep Learning Based Approaches", "7"),
        ("2.4", "MediaPipe and Landmark-Based Methods", "8"),
        ("2.5", "Recurrent Neural Networks for Gesture Recognition", "9"),
        ("2.6", "Summary and Research Gap", "10"),
        ("3", "System Design and Architecture", "11"),
        ("3.1", "Overall System Architecture", "11"),
        ("3.2", "Data Collection Module", "13"),
        ("3.3", "Hand Landmark Extraction", "14"),
        ("3.4", "LSTM Model Architecture", "15"),
        ("3.5", "Backend API Design", "17"),
        ("3.6", "Frontend Design", "18"),
        ("3.7", "Technology Stack", "19"),
        ("4", "Implementation", "20"),
        ("4.1", "Development Environment Setup", "20"),
        ("4.2", "Data Collection Implementation", "21"),
        ("4.3", "Model Training Implementation", "24"),
        ("4.4", "Backend Implementation", "28"),
        ("4.5", "Frontend Implementation", "32"),
        ("4.6", "Integration and Deployment", "36"),
        ("5", "Results and Discussion", "38"),
        ("5.1", "Dataset Summary", "38"),
        ("5.2", "Training Results and Accuracy", "39"),
        ("5.3", "Per-Class Classification Report", "41"),
        ("5.4", "System Performance Metrics", "43"),
        ("5.5", "UI Screenshots and Observations", "44"),
        ("5.6", "Comparison with Existing Systems", "45"),
        ("5.7", "Limitations", "46"),
        ("6", "Conclusion and Future Work", "47"),
        ("6.1", "Conclusion", "47"),
        ("6.2", "Future Enhancements", "48"),
        ("", "References", "50"),
    ]

    rows = []
    for num, title, pg in toc_entries:
        is_chapter = num.isdigit() and len(num) == 1
        is_front   = num == ""

        if is_chapter:
            label = f"Chapter {num}  —  {title}"
            fn = "Helvetica-Bold"
            fc = NAVY
            fs = 11
            indent = 0
        elif is_front:
            label = title
            fn = "Helvetica-Bold" if title in ("References",) else "Helvetica"
            fc = NAVY if title in ("References",) else GRAY
            fs = 10.5
            indent = 0
        else:
            label = f"  {num}  {title}"
            fn = "Helvetica"
            fc = GRAY_DK
            fs = 10
            indent = 10

        style_l = ParagraphStyle("tl", fontSize=fs, fontName=fn,
                                 textColor=fc, leftIndent=indent,
                                 leading=15)
        style_r = ParagraphStyle("tr", fontSize=fs, fontName=fn,
                                 textColor=fc, alignment=TA_RIGHT,
                                 leading=15)
        rows.append([
            Paragraph(label, style_l),
            Paragraph("." * 60, ParagraphStyle("dots", fontSize=8,
                      fontName="Helvetica", textColor=GRAY_LN, leading=15)),
            Paragraph(pg, style_r),
        ])
        if is_chapter:
            rows[-1][1] = Paragraph("", style_l)   # no dots for chapters

    t = Table(rows, colWidths=[PAGE_W*0.65, PAGE_W*0.2, PAGE_W*0.15])
    t.setStyle(TableStyle([
        ("ALIGN",  (0,0), (-1,-1), "LEFT"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
    ]))
    story.append(t)
    story.append(PageBreak())
    return story


# ─── LIST OF FIGURES ──────────────────────────────────────────────────────────
def build_lof(styles):
    from report_p1 import rule, sp
    story = []
    story.append(sp(15))
    story.append(Paragraph("LIST OF FIGURES", styles["pg_label"]))
    story.append(rule(NAVY, 2))
    story.append(sp(10))

    figs = [
        ("Fig 1.1", "Deaf and hard-of-hearing population worldwide", "2"),
        ("Fig 1.2", "Communication barrier between deaf and hearing populations", "3"),
        ("Fig 2.1", "Taxonomy of sign language recognition approaches", "6"),
        ("Fig 2.2", "CNN-based hand gesture recognition pipeline", "7"),
        ("Fig 2.3", "MediaPipe hand landmark model — 21 keypoints", "8"),
        ("Fig 2.4", "LSTM cell architecture and memory gates", "9"),
        ("Fig 3.1", "Overall SignAI system architecture", "11"),
        ("Fig 3.2", "End-to-end data flow pipeline", "12"),
        ("Fig 3.3", "Hand landmark extraction workflow", "14"),
        ("Fig 3.4", "Dual-hand keypoint extraction — 126 features", "14"),
        ("Fig 3.5", "Stacked LSTM model architecture", "15"),
        ("Fig 3.6", "LSTM input window — 30 frames × 126 keypoints", "16"),
        ("Fig 3.7", "FastAPI backend architecture and endpoints", "17"),
        ("Fig 3.8", "React frontend component hierarchy", "18"),
        ("Fig 4.1", "Data collection script — webcam feed with HUD", "22"),
        ("Fig 4.2", "Hand skeleton with MediaPipe landmarks during collection", "23"),
        ("Fig 4.3", "Training loss and accuracy curves", "26"),
        ("Fig 4.4", "Model summary — layer-by-layer parameters", "27"),
        ("Fig 4.5", "WebSocket real-time communication flow", "29"),
        ("Fig 4.6", "SignAI frontend — Translator tab", "33"),
        ("Fig 4.7", "SignAI frontend — Sentence Builder", "34"),
        ("Fig 4.8", "SignAI frontend — Sign List tab", "35"),
        ("Fig 5.1", "Training accuracy vs. validation accuracy per epoch", "39"),
        ("Fig 5.2", "Training loss vs. validation loss per epoch", "40"),
        ("Fig 5.3", "Confusion matrix — top-10 signs", "42"),
        ("Fig 5.4", "Real-time detection confidence scores", "44"),
        ("Fig 5.5", "Text-to-speech output flow", "45"),
    ]

    rows = []
    for fig_num, caption, pg in figs:
        rows.append([
            Paragraph(fig_num, ParagraphStyle("fn", fontSize=10,
                      fontName="Helvetica-Bold", textColor=BLUE, leading=14)),
            Paragraph(caption, ParagraphStyle("fc", fontSize=10,
                      fontName="Helvetica", textColor=GRAY_DK, leading=14)),
            Paragraph(pg, ParagraphStyle("fp", fontSize=10,
                      fontName="Helvetica", textColor=GRAY, alignment=TA_RIGHT,
                      leading=14)),
        ])

    t = Table(rows, colWidths=[PAGE_W*0.15, PAGE_W*0.72, PAGE_W*0.13])
    t.setStyle(TableStyle([
        ("ALIGN",  (0,0), (0,-1), "LEFT"),
        ("ALIGN",  (2,0), (2,-1), "RIGHT"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("LINEBELOW", (0,0), (-1,-1), 0.3, GRAY_LN),
    ]))
    story.append(t)
    story.append(PageBreak())
    return story


# ─── LIST OF TABLES ───────────────────────────────────────────────────────────
def build_lot(styles):
    from report_p1 import rule, sp
    story = []
    story.append(sp(15))
    story.append(Paragraph("LIST OF TABLES", styles["pg_label"]))
    story.append(rule(NAVY, 2))
    story.append(sp(10))

    tables = [
        ("Table 1.1", "Comparison of sign language types worldwide", "2"),
        ("Table 2.1", "Summary of related works in sign language recognition", "5"),
        ("Table 2.2", "Comparison of deep learning models for gesture recognition", "7"),
        ("Table 3.1", "Technology stack summary", "19"),
        ("Table 3.2", "LSTM model hyperparameters", "16"),
        ("Table 3.3", "API endpoint specifications", "17"),
        ("Table 4.1", "Supported signs — 40 categories", "21"),
        ("Table 4.2", "Dataset statistics — samples per category", "25"),
        ("Table 4.3", "Training configuration and hyperparameters", "25"),
        ("Table 4.4", "Python library dependencies", "20"),
        ("Table 4.5", "Node.js package dependencies", "20"),
        ("Table 5.1", "Dataset summary — total samples", "38"),
        ("Table 5.2", "Model performance metrics summary", "39"),
        ("Table 5.3", "Per-class precision, recall, F1-score", "41"),
        ("Table 5.4", "System latency measurements", "43"),
        ("Table 5.5", "Comparison with existing sign language systems", "45"),
        ("Table 5.6", "Confusion matrix — selected sign pairs", "42"),
    ]

    rows = []
    for tbl_num, caption, pg in tables:
        rows.append([
            Paragraph(tbl_num, ParagraphStyle("tn", fontSize=10,
                      fontName="Helvetica-Bold", textColor=BLUE, leading=14)),
            Paragraph(caption, ParagraphStyle("tc2", fontSize=10,
                      fontName="Helvetica", textColor=GRAY_DK, leading=14)),
            Paragraph(pg, ParagraphStyle("tp", fontSize=10,
                      fontName="Helvetica", textColor=GRAY,
                      alignment=TA_RIGHT, leading=14)),
        ])

    t = Table(rows, colWidths=[PAGE_W*0.18, PAGE_W*0.69, PAGE_W*0.13])
    t.setStyle(TableStyle([
        ("ALIGN",  (0,0), (0,-1), "LEFT"),
        ("ALIGN",  (2,0), (2,-1), "RIGHT"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("LINEBELOW", (0,0), (-1,-1), 0.3, GRAY_LN),
    ]))
    story.append(t)
    story.append(PageBreak())
    return story


# ─── CHAPTER 1: INTRODUCTION ──────────────────────────────────────────────────
def build_ch1(styles):
    from report_p1 import rule, thin_rule, sp, info_table, left_table

    story = []

    # Chapter heading
    d = Drawing(PAGE_W, 52)
    d.add(Rect(0, 0, PAGE_W, 52, fillColor=NAVY, strokeColor=NAVY))
    d.add(String(16, 32, "CHAPTER 1", fontSize=12,
                 fontName="Helvetica-Bold",
                 fillColor=colors.HexColor("#90caf9"), textAnchor="start"))
    d.add(String(16, 11, "Introduction",
                 fontSize=20, fontName="Helvetica-Bold",
                 fillColor=WHITE, textAnchor="start"))
    story.append(d)
    story.append(sp(14))

    # 1.1
    story.append(Paragraph("1.1  Background and Motivation", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "Communication is a fundamental human right. For the more than <b>466 million people worldwide</b> "
        "who suffer from disabling hearing loss (WHO, 2023), sign language serves as the primary and most "
        "natural means of communication. Sign language is a complete, complex, and expressive language that "
        "employs a system of hand gestures, body posture, and facial expressions to convey meaning.",
        styles["body"]))
    story.append(Paragraph(
        "Despite its significance, sign language remains inaccessible to the vast majority of the "
        "hearing population. This creates a profound communication barrier that affects education, "
        "healthcare, employment, and social inclusion for deaf and hard-of-hearing (DHH) individuals. "
        "Trained sign language interpreters are scarce and expensive, and their availability is "
        "particularly limited in developing countries.",
        styles["body"]))
    story.append(Paragraph(
        "Advances in <b>Artificial Intelligence (AI)</b>, particularly in <b>Computer Vision</b> and "
        "<b>Deep Learning</b>, have opened new possibilities for automatic sign language recognition. "
        "Modern hand-tracking libraries such as Google's <b>MediaPipe</b> can extract precise 3D hand "
        "landmarks in real time, while sequential deep learning models like <b>Long Short-Term Memory "
        "(LSTM)</b> networks excel at capturing the temporal dynamics of sign gestures.",
        styles["body"]))
    story.append(Paragraph(
        "This project, <b>SignAI</b>, is motivated by the need to create an accessible, low-cost, "
        "real-time sign language translation tool that does not require specialized hardware, works on "
        "a standard webcam, and can be deployed as a web application accessible from any modern browser.",
        styles["body"]))

    story.append(sp(10))

    # Statistics table
    story.append(Paragraph("Table 1.1 — Comparison of Sign Language Types Worldwide",
                            styles["caption"]))
    tbl_data = [
        ["Sign Language", "Country / Region", "Approx. Users", "Standardised?", "ISO Code"],
        ["American Sign Language (ASL)", "USA, Canada", "500,000+", "Yes", "ase"],
        ["British Sign Language (BSL)",  "United Kingdom", "150,000+", "Yes", "bfi"],
        ["Indian Sign Language (ISL)",   "India",          "2,000,000+", "Partial", "ins"],
        ["Auslan",                        "Australia",     "16,000+", "Yes", "asf"],
        ["Chinese Sign Language (CSL)",  "China",          "20,000,000+", "Yes", "csl"],
        ["French Sign Language (LSF)",   "France",         "100,000+", "Yes", "fsl"],
        ["International Sign (IS)",      "Global",         "Varies", "Partial", "ils"],
    ]
    story.append(info_table(tbl_data,
        [PAGE_W*0.30, PAGE_W*0.22, PAGE_W*0.17, PAGE_W*0.15, PAGE_W*0.16]))
    story.append(sp(10))

    # 1.2
    story.append(Paragraph("1.2  Problem Statement", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The primary challenge in sign language communication is the lack of an effective, real-time, "
        "and accessible translation tool. Existing solutions suffer from one or more of the following "
        "limitations:",
        styles["body"]))

    problems = [
        ("❶ Hardware Dependency",
         "Many systems require specialised gloves or depth sensors (e.g., Microsoft Kinect, Leap Motion), "
         "making them expensive and impractical for everyday use."),
        ("❷ Limited Sign Vocabulary",
         "Most systems are restricted to recognising only a small set of signs (typically fewer than 26 "
         "alphabets), which is insufficient for real-world communication."),
        ("❸ Lack of Temporal Modelling",
         "Static image-based CNN approaches fail to capture the temporal nature of many signs that involve "
         "hand movement over time."),
        ("❹ No Two-Way Communication",
         "Existing systems typically translate sign to text but do not include text-to-speech or sentence "
         "construction capabilities."),
        ("❺ Poor Real-Time Performance",
         "Many research systems operate offline on pre-recorded video clips rather than providing live, "
         "streaming predictions through a user-friendly web interface."),
    ]
    for title, desc in problems:
        story.append(KeepTogether([
            Paragraph(f"<b>{title}:</b>  {desc}", styles["bullet"]),
            sp(4),
        ]))

    story.append(sp(6))
    story.append(Paragraph(
        "This project addresses all of the above limitations by building a complete end-to-end system "
        "that works on any standard webcam, supports 40 signs with temporal LSTM modelling, outputs both "
        "text and speech, and runs as a real-time web application.",
        styles["body"]))

    story.append(sp(10))

    # 1.3
    story.append(Paragraph("1.3  Objectives of the Project", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The following are the primary objectives of the SignAI project:", styles["body"]))

    objectives = [
        "To design and implement a real-time sign language recognition system using a standard webcam without any specialised hardware.",
        "To extract and utilise 3D hand landmark keypoints from both hands (126 features per frame) using Google MediaPipe for robust gesture representation.",
        "To build and train a deep learning model (Stacked LSTM) capable of classifying a minimum of 40 sign language gestures with an accuracy of 95% or above.",
        "To develop a FastAPI-based backend server with WebSocket support for real-time, low-latency prediction streaming to the frontend.",
        "To create a modern, responsive React.js frontend that displays live camera feed, detected signs, confidence scores, and top-5 predictions.",
        "To implement a Sentence Builder module that accumulates detected signs into full sentences in real time.",
        "To integrate Text-to-Speech (TTS) output using Google TTS (gTTS) to make the system fully accessible to hearing users.",
        "To evaluate the system comprehensively on custom-collected and publicly available datasets and report accuracy, precision, recall, and F1-score.",
    ]
    for i, obj in enumerate(objectives, 1):
        story.append(Paragraph(f"<b>{i}.</b>  {obj}", styles["bullet"]))
        story.append(sp(3))

    story.append(sp(10))

    # 1.4
    story.append(Paragraph("1.4  Scope of the Project", styles["h2"]))
    story.append(rule())

    scope_data = [
        ["Aspect", "In Scope", "Out of Scope"],
        ["Sign Type",       "ASL static + dynamic signs",         "Indian / Chinese sign language"],
        ["Vocabulary",      "40 signs (phrases, alpha, numbers)",  "Full sentence grammar parsing"],
        ["Input",           "Webcam video (real-time)",            "Pre-recorded video files"],
        ["Output",          "Text + Speech + Sentence Builder",    "Sign language generation"],
        ["Platform",        "Web browser (React.js)",              "Mobile / AR/VR platforms"],
        ["Hardware",        "Standard RGB webcam",                 "Depth cameras, data gloves"],
        ["Users",           "Hearing users / learners",            "Clinical diagnostic systems"],
    ]
    story.append(info_table(scope_data,
        [PAGE_W*0.20, PAGE_W*0.42, PAGE_W*0.38]))
    story.append(sp(6))

    # 1.5
    story.append(Paragraph("1.5  Organisation of the Report", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The remainder of this report is organised into the following chapters:", styles["body"]))

    org = [
        ("Chapter 2 — Literature Review",
         "A comprehensive survey of existing work in sign language recognition, covering "
         "traditional image-based methods, CNN approaches, RNN/LSTM-based temporal models, "
         "and MediaPipe-based landmark methods."),
        ("Chapter 3 — System Design and Architecture",
         "Detailed description of the overall system architecture, data flow, LSTM model design, "
         "backend API design, and frontend component architecture."),
        ("Chapter 4 — Implementation",
         "Step-by-step implementation details covering data collection, model training, "
         "backend server, and frontend development with code snippets."),
        ("Chapter 5 — Results and Discussion",
         "Experimental results including training/validation accuracy curves, per-class "
         "classification report, confusion matrix, system performance metrics, and comparison "
         "with existing systems."),
        ("Chapter 6 — Conclusion and Future Work",
         "Summary of project achievements, limitations, and proposed directions for future "
         "enhancement including ISL support, mobile deployment, and real-time translation."),
    ]
    for title, desc in org:
        story.append(Paragraph(f"<b>{title}:</b>  {desc}", styles["bullet"]))
        story.append(sp(5))

    story.append(PageBreak())
    return story
