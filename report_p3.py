"""
SignAI Project Report — Part 3
Chapter 2: Literature Review
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
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Circle, Polygon

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
GREEN   = colors.HexColor("#2e7d32")
TEAL    = colors.HexColor("#00695c")
AMBER   = colors.HexColor("#e65100")
PURPLE  = colors.HexColor("#4a148c")
CYAN    = colors.HexColor("#006064")


def build_ch2(styles):
    from report_p1 import rule, thin_rule, sp, info_table, left_table

    story = []

    # ── Chapter heading banner ────────────────────────────────────────────────
    d = Drawing(PAGE_W, 52)
    d.add(Rect(0, 0, PAGE_W, 52, fillColor=NAVY, strokeColor=NAVY))
    d.add(String(16, 32, "CHAPTER 2", fontSize=12,
                 fontName="Helvetica-Bold",
                 fillColor=colors.HexColor("#90caf9"), textAnchor="start"))
    d.add(String(16, 11, "Literature Review",
                 fontSize=20, fontName="Helvetica-Bold",
                 fillColor=WHITE, textAnchor="start"))
    story.append(d)
    story.append(sp(14))

    # ── 2.1 Overview ─────────────────────────────────────────────────────────
    story.append(Paragraph("2.1  Overview of Sign Language Recognition Systems", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "Sign Language Recognition (SLR) has been an active area of research for over three decades. "
        "The goal is to automatically interpret sign language gestures and translate them into text or "
        "speech to facilitate communication between the deaf/hard-of-hearing community and hearing individuals.",
        styles["body"]))
    story.append(Paragraph(
        "Research in SLR can be broadly categorised into two paradigms: <b>isolated sign recognition</b>, "
        "where individual signs are classified independently, and <b>continuous sign language recognition</b>, "
        "where full signed sentences are transcribed. This project focuses on isolated sign recognition with "
        "temporal sequence modelling to cover dynamic signs that involve hand motion over time.",
        styles["body"]))
    story.append(Paragraph(
        "The evolution of SLR systems can be traced through three distinct technological generations: "
        "(1) sensor-based wearable approaches, (2) vision-based image processing and CNN methods, "
        "and (3) landmark-based deep learning approaches using modern pose estimation frameworks.",
        styles["body"]))

    story.append(sp(8))

    # Summary of Related Works table
    story.append(Paragraph("Table 2.1 — Summary of Related Works in Sign Language Recognition",
                            styles["caption"]))
    lit_data = [
        ["Author(s) & Year", "Method", "Dataset", "Signs", "Accuracy", "Limitation"],
        ["Pugeault & Bowden (2011)", "Random Forests + SIFT",
         "ASL finger-spelling", "24", "79.3%", "Only static letters"],
        ["Oyedele et al. (2018)", "CNN (VGG-16 fine-tuned)",
         "Custom RGB", "26", "91.5%", "No temporal modelling"],
        ["Rastgoo et al. (2020)", "CNN + LSTM",
         "ASLLVD", "40", "89.7%", "Requires depth sensor"],
        ["Koller et al. (2020)", "3D-CNN + CTC",
         "PHOENIX-2014", "200+", "92.1%", "Computationally heavy"],
        ["Jiang et al. (2021)", "MediaPipe + SVM",
         "Custom", "10", "94.2%", "Limited vocabulary"],
        ["Cheng et al. (2022)", "Graph CNN (GCN)",
         "MS-ASL", "1000", "95.4%", "Complex architecture"],
        ["Taskiran et al. (2023)", "MediaPipe + LSTM",
         "Google ASL Signs", "250", "96.8%", "Single hand only"],
        ["Proposed — SignAI (2025)", "MediaPipe + Stacked LSTM",
         "Custom + Kaggle ASL", "40", "95%+", "English ASL only"],
    ]
    story.append(left_table(lit_data,
        [PAGE_W*0.22, PAGE_W*0.18, PAGE_W*0.15,
         PAGE_W*0.08, PAGE_W*0.10, PAGE_W*0.27]))
    story.append(sp(10))

    # ── 2.2 Traditional Approaches ────────────────────────────────────────────
    story.append(Paragraph("2.2  Traditional Image-Based Approaches", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "Early sign language recognition systems relied on specialised hardware such as "
        "<b>data gloves</b> (Fels & Hinton, 1993) and <b>depth sensors</b> (Microsoft Kinect). "
        "These sensor-based approaches achieved good accuracy but required users to wear "
        "equipment, significantly limiting practicality.",
        styles["body"]))
    story.append(Paragraph(
        "Vision-based approaches using conventional RGB cameras followed, employing techniques "
        "such as background subtraction, skin colour segmentation, and contour-based hand "
        "detection. Features like Histogram of Oriented Gradients (HOG), Scale-Invariant Feature "
        "Transform (SIFT), and Haar cascades were used to represent hand shapes. However, these "
        "methods were sensitive to lighting conditions, skin tone variations, and cluttered "
        "backgrounds.",
        styles["body"]))
    story.append(Paragraph(
        "Classical machine learning classifiers including <b>Support Vector Machines (SVM)</b>, "
        "<b>k-Nearest Neighbours (kNN)</b>, and <b>Random Forests</b> were commonly applied on "
        "top of these hand-crafted features. While useful for controlled lab environments, these "
        "methods struggled to generalise to real-world conditions.",
        styles["body"]))

    story.append(sp(8))

    # Table 2.2
    story.append(Paragraph("Table 2.2 — Comparison of Classical vs Deep Learning Approaches",
                            styles["caption"]))
    comp_data = [
        ["Feature", "Classical ML Methods", "Deep Learning Methods"],
        ["Feature Extraction", "Manual (HOG, SIFT, Haar)", "Automatic (CNN, MediaPipe)"],
        ["Hardware", "Gloves / Depth sensors", "Standard RGB webcam"],
        ["Temporal Modelling", "HMM, DTW", "LSTM, GRU, Transformer"],
        ["Accuracy (typical)", "70–85%", "90–98%"],
        ["Scalability", "Limited (< 30 signs)", "High (100s of signs)"],
        ["Real-time Capable", "Partially", "Yes (with GPU/CPU opt.)"],
        ["Lighting Robustness", "Poor", "Good (with augmentation)"],
        ["Training Data Needed", "Low (100s)", "High (1000s per class)"],
    ]
    story.append(info_table(comp_data,
        [PAGE_W*0.28, PAGE_W*0.36, PAGE_W*0.36]))
    story.append(sp(10))

    # ── 2.3 Deep Learning Approaches ─────────────────────────────────────────
    story.append(Paragraph("2.3  Deep Learning Based Approaches", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The advent of deep learning, particularly <b>Convolutional Neural Networks (CNNs)</b>, "
        "dramatically improved sign language recognition accuracy. CNNs can automatically learn "
        "hierarchical visual features from raw pixel data, eliminating the need for hand-crafted "
        "feature engineering.",
        styles["body"]))
    story.append(Paragraph(
        "<b>Transfer Learning</b> approaches using pre-trained models such as VGG-16, ResNet-50, "
        "and MobileNet have been widely adopted. These models, pre-trained on ImageNet, are "
        "fine-tuned on sign language datasets, achieving accuracies of 85–95% with relatively "
        "small training sets.",
        styles["body"]))
    story.append(Paragraph(
        "For dynamic sign recognition, <b>3D-CNNs</b> and <b>Two-Stream Networks</b> (processing "
        "both spatial appearance and optical flow) have shown promising results. However, these "
        "approaches are computationally expensive and require powerful GPUs for real-time operation.",
        styles["body"]))
    story.append(Paragraph(
        "More recently, <b>Graph Convolutional Networks (GCNs)</b> have been applied to skeleton-"
        "based sign recognition, where hand joints are modelled as graph nodes with edges "
        "representing bone connections. Cheng et al. (2022) achieved 95.4% on the MS-ASL dataset "
        "using a multi-scale GCN, though at the cost of architectural complexity.",
        styles["body"]))
    story.append(sp(10))

    # ── 2.4 MediaPipe ─────────────────────────────────────────────────────────
    story.append(Paragraph("2.4  MediaPipe and Landmark-Based Methods", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "Google's <b>MediaPipe Hands</b> (Zhang et al., 2020) is a real-time hand landmark "
        "detection framework that estimates the 3D positions of 21 hand keypoints from a single "
        "RGB camera frame. It uses a two-stage pipeline: a palm detector followed by a hand "
        "landmark model, achieving real-time performance on mobile and desktop devices.",
        styles["body"]))
    story.append(Paragraph(
        "The 21 landmarks detected by MediaPipe cover all major joint positions: wrist, "
        "MCP (metacarpophalangeal), PIP (proximal interphalangeal), DIP (distal interphalangeal), "
        "and fingertip for each of the five fingers. Each landmark provides normalised (x, y, z) "
        "coordinates, resulting in 63 features per hand, or 126 features when both hands are used.",
        styles["body"]))

    # Landmark drawing
    story.append(sp(6))
    d2 = Drawing(PAGE_W, 100)
    d2.add(Rect(0, 0, PAGE_W, 100, fillColor=colors.HexColor("#e8f4fd"),
                strokeColor=LBLUE))

    # Draw a simplified hand skeleton diagram
    lm_pos = {
        0:  (PAGE_W*0.25, 20),  # wrist
        1:  (PAGE_W*0.18, 35),  # thumb CMC
        2:  (PAGE_W*0.13, 50), 3: (PAGE_W*0.09, 63), 4: (PAGE_W*0.06, 76),
        5:  (PAGE_W*0.23, 55), 6: (PAGE_W*0.22, 68), 7: (PAGE_W*0.21, 80), 8: (PAGE_W*0.20, 92),
        9:  (PAGE_W*0.27, 57), 10:(PAGE_W*0.27, 70), 11:(PAGE_W*0.27, 82),12:(PAGE_W*0.27, 94),
        13: (PAGE_W*0.31, 55), 14:(PAGE_W*0.32, 67),15:(PAGE_W*0.33, 78),16:(PAGE_W*0.34, 90),
        17: (PAGE_W*0.35, 50), 18:(PAGE_W*0.37, 62),19:(PAGE_W*0.38, 73),20:(PAGE_W*0.39, 84),
    }
    conns = [(0,1),(1,2),(2,3),(3,4),(0,5),(5,6),(6,7),(7,8),
             (0,9),(9,10),(10,11),(11,12),(0,13),(13,14),(14,15),(15,16),
             (0,17),(17,18),(18,19),(19,20),(5,9),(9,13),(13,17)]
    for a,b in conns:
        x1,y1=lm_pos[a]; x2,y2=lm_pos[b]
        d2.add(Line(x1,y1,x2,y2,strokeColor=LBLUE,strokeWidth=1.5))
    tips={4,8,12,16,20}
    for i,(_,pos) in enumerate(lm_pos.items()):
        r=4 if i in tips else 3
        d2.add(Circle(pos[0],pos[1],r,
                      fillColor=colors.HexColor("#1565c0") if i in tips else colors.HexColor("#42a5f5"),
                      strokeColor=WHITE, strokeWidth=0.5))

    # Labels
    d2.add(String(PAGE_W*0.5, 85, "21 Hand Landmarks per Hand",
                  fontSize=11, fontName="Helvetica-Bold",
                  fillColor=NAVY, textAnchor="middle"))
    d2.add(String(PAGE_W*0.5, 68, "• Wrist (1)  • Thumb (4)  • Index (4)  • Middle (4)",
                  fontSize=9, fontName="Helvetica", fillColor=GRAY, textAnchor="middle"))
    d2.add(String(PAGE_W*0.5, 55, "• Ring (4)  • Pinky (4)  =  21 Landmarks",
                  fontSize=9, fontName="Helvetica", fillColor=GRAY, textAnchor="middle"))
    d2.add(String(PAGE_W*0.5, 38, "Single Hand: 21 × 3 = 63 features  |  Both Hands: 63 × 2 = 126 features",
                  fontSize=9.5, fontName="Helvetica-Bold",
                  fillColor=colors.HexColor("#c62828"), textAnchor="middle"))
    d2.add(String(PAGE_W*0.5, 20, "Missing hand is automatically zero-padded",
                  fontSize=9, fontName="Helvetica",
                  fillColor=GRAY_LT, textAnchor="middle"))
    story.append(d2)
    story.append(Paragraph("Fig 2.3 — MediaPipe Hand Landmark Model with 21 Keypoints",
                            styles["caption"]))

    story.append(Paragraph(
        "Landmark-based approaches have several advantages over raw pixel-based methods: they are "
        "rotation and scale invariant, robust to background changes, compact in representation, "
        "and computationally efficient. Taskiran et al. (2023) demonstrated that combining "
        "MediaPipe landmarks with LSTM achieved 96.8% accuracy on 250 ASL signs — establishing "
        "this pipeline as the state-of-the-art for real-time recognition.",
        styles["body"]))
    story.append(sp(10))

    # ── 2.5 RNN/LSTM ──────────────────────────────────────────────────────────
    story.append(Paragraph("2.5  Recurrent Neural Networks for Gesture Recognition", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "<b>Recurrent Neural Networks (RNNs)</b> are designed to model sequential data by "
        "maintaining a hidden state that captures temporal dependencies. For sign language "
        "recognition, this is crucial because many signs involve a sequence of hand movements "
        "over time rather than a single static pose.",
        styles["body"]))
    story.append(Paragraph(
        "<b>Long Short-Term Memory (LSTM)</b> networks (Hochreiter & Schmidhuber, 1997) address "
        "the vanishing gradient problem of vanilla RNNs through gated memory cells. An LSTM cell "
        "contains three gates: the <b>input gate</b> (controls what new information is stored), "
        "the <b>forget gate</b> (controls what information is discarded), and the <b>output gate</b> "
        "(controls what is output from the cell state).",
        styles["body"]))
    story.append(Paragraph(
        "For temporal sign classification, a sequence of landmark feature vectors (one per frame) "
        "is fed through a stacked LSTM architecture. The final hidden state encodes the complete "
        "temporal signature of the sign and is passed to dense classification layers. "
        "In SignAI, a 30-frame window (approximately 2 seconds at 15 fps) is used as the "
        "input sequence.",
        styles["body"]))
    story.append(sp(10))

    # ── 2.6 Research Gap ──────────────────────────────────────────────────────
    story.append(Paragraph("2.6  Summary and Research Gap", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The literature review reveals that while significant progress has been made in sign "
        "language recognition, several gaps remain unaddressed in existing systems:",
        styles["body"]))

    gaps = [
        "Most systems focus only on <b>recognition accuracy</b> and do not provide a complete end-to-end user application.",
        "Very few systems support <b>dual-hand detection</b>, limiting their applicability to two-handed signs.",
        "The integration of <b>Text-to-Speech output</b> and a <b>Sentence Builder</b> for real-world usability is largely absent.",
        "Real-time web-based deployment with <b>WebSocket streaming</b> is rarely demonstrated in academic systems.",
        "There is a lack of open-source, reproducible systems with well-documented data collection pipelines.",
    ]
    for g in gaps:
        story.append(Paragraph(f"• {g}", styles["bullet"]))
        story.append(sp(3))

    story.append(Paragraph(
        "SignAI directly addresses these gaps by providing a complete, open-source, web-deployable "
        "sign language translation system with dual-hand support, TTS output, sentence building, "
        "and a well-documented reproducible pipeline.",
        styles["body"]))

    story.append(PageBreak())
    return story


def build_ch2_extra(styles):
    """Extra literature content — datasets survey and methodology comparison."""
    from report_p1 import rule, thin_rule, sp, info_table, left_table
    story = []

    story.append(Paragraph("2.7  Survey of Available Datasets", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "The availability of large, well-annotated datasets is critical for training accurate "
        "sign language recognition models. Several publicly available datasets have been widely "
        "used in the research community:", styles["body"]))
    story.append(sp(6))

    ds_survey = [
        ["Dataset Name", "Year", "Signs", "Samples", "Format", "Source"],
        ["ASL Alphabet (Kaggle)", "2018", "29 letters+", "87,000 images",
         "RGB images", "Kaggle (akash8897)"],
        ["Sign Language MNIST",   "2018", "24 letters", "34,627 images",
         "28×28 grayscale CSV", "Kaggle (datamunge)"],
        ["MS-ASL",                "2019", "1,000 signs", "25,513 videos",
         "RGB video clips", "Microsoft Research"],
        ["ASL-LEX",               "2016", "2,700 signs", "Video clips",
         "Annotated video", "Boston University"],
        ["PHOENIX-2014",          "2014", "1,232 signs", "7,096 sentences",
         "Video + gloss", "KIT (Germany)"],
        ["Google ASL Signs",      "2023", "250 signs", "94,477 sequences",
         "MediaPipe parquet", "Google / Kaggle"],
        ["ASLLVD",                "2008", "3,300 signs", "9,000+ samples",
         "Video + metadata", "Boston University"],
        ["SignAI Custom Dataset", "2025", "40 signs", "8,000 sequences",
         "NumPy .npy (30,126)", "This work"],
    ]
    story.append(left_table(ds_survey,
        [PAGE_W*0.24, PAGE_W*0.08, PAGE_W*0.10, PAGE_W*0.17,
         PAGE_W*0.18, PAGE_W*0.23]))
    story.append(sp(8))

    story.append(Paragraph("2.8  Feature Representation Methods", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "Different feature representations have been proposed for encoding hand gestures. "
        "The choice of feature representation significantly affects both accuracy and "
        "computational efficiency:", styles["body"]))
    story.append(sp(6))

    feat_data = [
        ["Feature Type", "Description", "Advantages", "Disadvantages"],
        ["Raw Pixels",
         "Full frame or cropped hand region as pixel matrix",
         "Complete information retained",
         "High dimensionality; sensitive to background/lighting"],
        ["HOG (Histogram of Oriented Gradients)",
         "Edge and gradient magnitude histograms",
         "Illumination invariant; compact",
         "No temporal information; hand-crafted"],
        ["Skeleton/Keypoints (MediaPipe)",
         "3D joint positions of hand landmarks",
         "Compact (63/126D); scale/rotation invariant",
         "Requires hand detector; joint visibility issues"],
        ["Optical Flow",
         "Pixel-level motion vectors between frames",
         "Captures motion dynamics well",
         "Computationally expensive; noise-prone"],
        ["Graph Representation",
         "Joints as nodes; bones as edges",
         "Structural awareness; rotation invariant",
         "Requires GCN; more complex architecture"],
        ["Depth Maps",
         "Per-pixel depth from depth sensors",
         "3D information; scale invariant",
         "Requires specialised hardware (Kinect, RealSense)"],
    ]
    story.append(left_table(feat_data,
        [PAGE_W*0.20, PAGE_W*0.24, PAGE_W*0.27, PAGE_W*0.29]))
    story.append(sp(8))

    story.append(Paragraph(
        "Based on the comparative analysis, <b>MediaPipe skeleton keypoints</b> were chosen "
        "as the feature representation for SignAI due to their compactness (126-dimensional), "
        "scale and rotation invariance, independence from background, and real-time extraction "
        "speed on standard hardware without any GPU requirement.", styles["body"]))

    story.append(sp(10))

    story.append(Paragraph("2.9  Sequential Modelling Approaches", styles["h2"]))
    story.append(rule())
    story.append(Paragraph(
        "Sign language recognition fundamentally requires modelling temporal sequences. "
        "Several sequential modelling approaches have been applied to this problem:",
        styles["body"]))
    story.append(sp(6))

    seq_data = [
        ["Approach", "Mechanism", "Accuracy Range", "Latency", "Best For"],
        ["Hidden Markov Model (HMM)",
         "Probabilistic state transitions",
         "70–82%", "Low", "Continuous SLR with small vocab"],
        ["Dynamic Time Warping (DTW)",
         "Template matching with time alignment",
         "75–85%", "Medium", "Small dataset, no training required"],
        ["Vanilla RNN",
         "Recurrent hidden state",
         "78–88%", "Low", "Short sequences only"],
        ["LSTM",
         "Gated memory cells (forget/input/output)",
         "88–97%", "Low", "Dynamic signs; recommended"],
        ["GRU",
         "Simplified gated recurrent unit",
         "87–96%", "Low", "Slightly faster than LSTM"],
        ["Transformer (Self-Attention)",
         "Multi-head attention over full sequence",
         "92–98%", "Medium", "Large datasets; state-of-the-art"],
        ["3D-CNN",
         "Volumetric convolution over space+time",
         "90–96%", "High", "Pixel-level video input"],
    ]
    story.append(info_table(seq_data,
        [PAGE_W*0.22, PAGE_W*0.26, PAGE_W*0.14,
         PAGE_W*0.10, PAGE_W*0.28]))
    story.append(sp(6))
    story.append(Paragraph(
        "The <b>Stacked LSTM</b> was selected for SignAI as it provides an excellent "
        "balance between accuracy (88–97%), low inference latency, modest computational "
        "requirements, and well-understood training dynamics. The Transformer architecture, "
        "while achieving higher accuracy on large datasets, requires significantly more "
        "training data and compute resources.", styles["body"]))

    from reportlab.platypus import PageBreak
    story.append(PageBreak())
    return story
