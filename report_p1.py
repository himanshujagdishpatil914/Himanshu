"""
SignAI Project Report — Part 1
Styles, Helpers, Cover Page, Certificate, Acknowledgement, Abstract
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak,
    KeepTogether, Image
)
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String
from reportlab.graphics import renderPDF
import math

W, H = A4
PAGE_W = W - 50*mm   # usable width

# ─── COLOURS ──────────────────────────────────────────────────────────────────
NAVY    = colors.HexColor("#1a237e")
BLUE    = colors.HexColor("#1565c0")
LBLUE   = colors.HexColor("#1976d2")
CYAN    = colors.HexColor("#0288d1")
TEAL    = colors.HexColor("#00695c")
GRAY_DK = colors.HexColor("#212121")
GRAY    = colors.HexColor("#424242")
GRAY_LT = colors.HexColor("#757575")
GRAY_BG = colors.HexColor("#f5f5f5")
GRAY_LN = colors.HexColor("#e0e0e0")
WHITE   = colors.white
BLACK   = colors.black
RED     = colors.HexColor("#c62828")
GREEN   = colors.HexColor("#2e7d32")
AMBER   = colors.HexColor("#e65100")
PURPLE  = colors.HexColor("#6a1b9a")

# ─── STYLES ───────────────────────────────────────────────────────────────────
def make_styles():
    def S(name, **kw):
        return ParagraphStyle(name, **kw)

    return {
        # Cover
        "cov_inst":   S("cov_inst",   fontSize=13, fontName="Helvetica-Bold",
                         textColor=NAVY,  alignment=TA_CENTER, spaceAfter=4, leading=18),
        "cov_dept":   S("cov_dept",   fontSize=11, fontName="Helvetica",
                         textColor=GRAY,  alignment=TA_CENTER, spaceAfter=2, leading=16),
        "cov_title":  S("cov_title",  fontSize=22, fontName="Helvetica-Bold",
                         textColor=NAVY,  alignment=TA_CENTER, spaceAfter=8, leading=30),
        "cov_sub":    S("cov_sub",    fontSize=12, fontName="Helvetica",
                         textColor=GRAY,  alignment=TA_CENTER, spaceAfter=4, leading=18),
        "cov_label":  S("cov_label",  fontSize=11, fontName="Helvetica-Bold",
                         textColor=GRAY_DK, alignment=TA_CENTER, spaceAfter=2),
        "cov_value":  S("cov_value",  fontSize=11, fontName="Helvetica",
                         textColor=GRAY,    alignment=TA_CENTER, spaceAfter=2),
        # Chapter headings
        "ch_num":     S("ch_num",     fontSize=13, fontName="Helvetica-Bold",
                         textColor=BLUE,  spaceBefore=6, spaceAfter=2),
        "ch_title":   S("ch_title",   fontSize=18, fontName="Helvetica-Bold",
                         textColor=NAVY,  spaceBefore=2, spaceAfter=10, leading=24),
        "h2":         S("h2",         fontSize=13, fontName="Helvetica-Bold",
                         textColor=BLUE,  spaceBefore=12, spaceAfter=4),
        "h3":         S("h3",         fontSize=11, fontName="Helvetica-Bold",
                         textColor=LBLUE, spaceBefore=8,  spaceAfter=3),
        # Body
        "body":       S("body",       fontSize=11, fontName="Helvetica",
                         textColor=GRAY_DK, leading=18, spaceAfter=6,
                         alignment=TA_JUSTIFY),
        "body_c":     S("body_c",     fontSize=11, fontName="Helvetica",
                         textColor=GRAY_DK, leading=18, spaceAfter=6,
                         alignment=TA_CENTER),
        "bullet":     S("bullet",     fontSize=11, fontName="Helvetica",
                         textColor=GRAY_DK, leading=17, spaceAfter=3,
                         leftIndent=16, firstLineIndent=0),
        "bullet2":    S("bullet2",    fontSize=10.5, fontName="Helvetica",
                         textColor=GRAY,    leading=16, spaceAfter=2,
                         leftIndent=32),
        # Caption
        "caption":    S("caption",    fontSize=9.5, fontName="Helvetica",
                         textColor=GRAY_LT, alignment=TA_CENTER,
                         spaceBefore=2, spaceAfter=8),
        # Code
        "code":       S("code",       fontSize=8.5, fontName="Courier",
                         textColor=colors.HexColor("#1b5e20"),
                         backColor=colors.HexColor("#f1f8e9"),
                         leading=12, leftIndent=8, spaceAfter=6),
        # TOC
        "toc1":       S("toc1",       fontSize=11, fontName="Helvetica-Bold",
                         textColor=NAVY,   spaceBefore=6, spaceAfter=2),
        "toc2":       S("toc2",       fontSize=10.5, fontName="Helvetica",
                         textColor=GRAY,   spaceBefore=2, spaceAfter=1,
                         leftIndent=16),
        # Abstract
        "abs_body":   S("abs_body",   fontSize=11, fontName="Helvetica",
                         textColor=GRAY_DK, leading=19, spaceAfter=6,
                         alignment=TA_JUSTIFY),
        # Section label
        "pg_label":   S("pg_label",   fontSize=20, fontName="Helvetica-Bold",
                         textColor=NAVY, alignment=TA_CENTER,
                         spaceBefore=20, spaceAfter=10),
    }

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def rule(color=BLUE, thickness=1.2):
    return HRFlowable(width="100%", thickness=thickness,
                      color=color, spaceAfter=6, spaceBefore=4)

def thin_rule():
    return HRFlowable(width="100%", thickness=0.5,
                      color=GRAY_LN, spaceAfter=4, spaceBefore=4)

def sp(h=6):
    return Spacer(1, h)

def info_table(data, col_widths, header_bg=NAVY, stripe=GRAY_BG):
    """Generic styled table. data[0] = header row."""
    ts = [
        ("BACKGROUND",    (0,0), (-1,0),  header_bg),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,0),  10),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",      (0,1), (-1,-1), 9.5),
        ("TEXTCOLOR",     (0,1), (-1,-1), GRAY_DK),
        ("GRID",          (0,0), (-1,-1), 0.5, GRAY_LN),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, stripe]),
    ]
    rows = []
    for r in data:
        rows.append([
            Paragraph(str(c), ParagraphStyle("tc",
                fontSize=9.5, fontName="Helvetica",
                textColor=GRAY_DK if i>0 else WHITE,
                alignment=TA_CENTER, leading=13))
            for i, c in enumerate(r)
        ])
    # fix header style
    rows[0] = [
        Paragraph(str(c), ParagraphStyle("th",
            fontSize=10, fontName="Helvetica-Bold",
            textColor=WHITE, alignment=TA_CENTER, leading=14))
        for c in data[0]
    ]
    t = Table(rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle(ts))
    return t

def left_table(data, col_widths, header_bg=NAVY, stripe=GRAY_BG):
    """Table with left-aligned text."""
    ts = [
        ("BACKGROUND",    (0,0), (-1,0),  header_bg),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,0),  10),
        ("ALIGN",         (0,0), (-1,-1), "LEFT"),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",      (0,1), (-1,-1), 9.5),
        ("TEXTCOLOR",     (0,1), (-1,-1), GRAY_DK),
        ("GRID",          (0,0), (-1,-1), 0.5, GRAY_LN),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, stripe]),
    ]
    rows = []
    for r in data:
        rows.append([
            Paragraph(str(c), ParagraphStyle("tc",
                fontSize=9.5, fontName="Helvetica",
                textColor=GRAY_DK, alignment=TA_LEFT, leading=14))
            for c in r
        ])
    rows[0] = [
        Paragraph(str(c), ParagraphStyle("th",
            fontSize=10, fontName="Helvetica-Bold",
            textColor=WHITE, alignment=TA_LEFT, leading=14))
        for c in data[0]
    ]
    t = Table(rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle(ts))
    return t

def arch_box(drawing, x, y, w, h, label, sublabel="",
             fill=LBLUE, text_col=WHITE, font_size=9):
    """Draw a box with label inside a Drawing."""
    drawing.add(Rect(x, y, w, h, fillColor=fill,
                     strokeColor=NAVY, strokeWidth=1))
    drawing.add(String(x + w/2, y + h/2 + (5 if sublabel else 1),
                       label, fontSize=font_size,
                       fontName="Helvetica-Bold",
                       fillColor=text_col, textAnchor="middle"))
    if sublabel:
        drawing.add(String(x + w/2, y + h/2 - 9,
                           sublabel, fontSize=7.5,
                           fontName="Helvetica",
                           fillColor=text_col, textAnchor="middle"))

def arrow(drawing, x1, y1, x2, y2, label=""):
    drawing.add(Line(x1, y1, x2, y2,
                     strokeColor=GRAY, strokeWidth=1.2))
    # arrowhead
    ang = math.atan2(y2-y1, x2-x1)
    sz  = 6
    for da in (0.4, -0.4):
        ax = x2 - sz*math.cos(ang+da)
        ay = y2 - sz*math.sin(ang+da)
        drawing.add(Line(x2, y2, ax, ay,
                         strokeColor=GRAY, strokeWidth=1.2))
    if label:
        mx = (x1+x2)/2
        my = (y1+y2)/2 + 4
        drawing.add(String(mx, my, label, fontSize=7.5,
                           fontName="Helvetica", fillColor=GRAY_LT,
                           textAnchor="middle"))

# ─── PAGE CALLBACKS ───────────────────────────────────────────────────────────
class PageDraw:
    def __init__(self):
        self.chapter = ""

    def __call__(self, canvas, doc):
        canvas.saveState()
        # Header line
        canvas.setStrokeColor(NAVY)
        canvas.setLineWidth(1.5)
        canvas.line(25*mm, H-20*mm, W-25*mm, H-20*mm)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(NAVY)
        canvas.drawString(25*mm, H-17*mm, "SignAI — AI Sign Language Translator")
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(GRAY_LT)
        canvas.drawRightString(W-25*mm, H-17*mm,
                               "Final Year Project Report  |  Himanshu Jagdish Patil")
        # Footer
        canvas.setStrokeColor(GRAY_LN)
        canvas.setLineWidth(0.8)
        canvas.line(25*mm, 18*mm, W-25*mm, 18*mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(GRAY_LT)
        canvas.drawString(25*mm, 13*mm, "Department of Computer Science & Engineering (AI & ML)")
        canvas.setFillColor(NAVY)
        canvas.setFont("Helvetica-Bold", 9)
        canvas.drawCentredString(W/2, 13*mm, str(doc.page))
        canvas.restoreState()

page_draw = PageDraw()

def first_page(canvas, doc):
    pass  # cover/cert pages – no header/footer

# ─── COVER PAGE ───────────────────────────────────────────────────────────────
def build_cover(styles):
    story = []
    story.append(sp(10))

    # Institution name box
    d = Drawing(PAGE_W, 60)
    d.add(Rect(0, 0, PAGE_W, 60, fillColor=NAVY, strokeColor=NAVY))
    d.add(String(PAGE_W/2, 38, "SHRI XYZ INSTITUTE OF TECHNOLOGY",
                 fontSize=15, fontName="Helvetica-Bold",
                 fillColor=WHITE, textAnchor="middle"))
    d.add(String(PAGE_W/2, 20, "Department of Computer Science & Engineering (AI & ML)",
                 fontSize=10.5, fontName="Helvetica",
                 fillColor=colors.HexColor("#bbdefb"), textAnchor="middle"))
    d.add(String(PAGE_W/2, 7, "Affiliated to XYZ University | NAAC Accredited",
                 fontSize=9, fontName="Helvetica",
                 fillColor=colors.HexColor("#90caf9"), textAnchor="middle"))
    story.append(d)
    story.append(sp(18))

    # Badge row
    d2 = Drawing(PAGE_W, 22)
    for i, (label, x) in enumerate([
        ("B.Tech — AI & ML", 0),
        ("Academic Year 2024-25", PAGE_W/3),
        ("Final Year Project", PAGE_W*2/3),
    ]):
        d2.add(Rect(x+2, 0, PAGE_W/3-6, 22,
                    fillColor=colors.HexColor("#e3f2fd"), strokeColor=LBLUE))
        d2.add(String(x+2+(PAGE_W/3-6)/2, 8, label,
                      fontSize=9, fontName="Helvetica-Bold",
                      fillColor=NAVY, textAnchor="middle"))
    story.append(d2)
    story.append(sp(22))

    # Title block
    d3 = Drawing(PAGE_W, 90)
    d3.add(Rect(0, 0, PAGE_W, 90,
                fillColor=colors.HexColor("#e8f4fd"),
                strokeColor=BLUE, strokeWidth=1.5))
    d3.add(Rect(0, 72, PAGE_W, 4, fillColor=BLUE, strokeColor=BLUE))
    d3.add(Rect(0, 0,  PAGE_W, 4, fillColor=BLUE, strokeColor=BLUE))
    d3.add(String(PAGE_W/2, 58,
                  "SignAI: Real-Time AI-Powered Sign Language",
                  fontSize=17, fontName="Helvetica-Bold",
                  fillColor=NAVY, textAnchor="middle"))
    d3.add(String(PAGE_W/2, 36,
                  "Translator with Text-to-Speech and",
                  fontSize=17, fontName="Helvetica-Bold",
                  fillColor=NAVY, textAnchor="middle"))
    d3.add(String(PAGE_W/2, 14,
                  "Sentence Builder",
                  fontSize=17, fontName="Helvetica-Bold",
                  fillColor=NAVY, textAnchor="middle"))
    story.append(d3)
    story.append(sp(20))

    # Submitted by
    d4 = Drawing(PAGE_W, 110)
    d4.add(Rect(0, 0, PAGE_W, 110,
                fillColor=WHITE, strokeColor=GRAY_LN))
    d4.add(String(PAGE_W/2, 92,
                  "Submitted By",
                  fontSize=10, fontName="Helvetica-Bold",
                  fillColor=GRAY_LT, textAnchor="middle"))
    d4.add(String(PAGE_W/2, 73,
                  "Himanshu Jagdish Patil",
                  fontSize=14, fontName="Helvetica-Bold",
                  fillColor=NAVY, textAnchor="middle"))
    d4.add(String(PAGE_W/2, 55,
                  "Roll No.: CS2024001  |  Batch: 2021–2025",
                  fontSize=10, fontName="Helvetica",
                  fillColor=GRAY, textAnchor="middle"))
    d4.add(String(PAGE_W/2, 37,
                  "Under the Guidance of:",
                  fontSize=9.5, fontName="Helvetica",
                  fillColor=GRAY_LT, textAnchor="middle"))
    d4.add(String(PAGE_W/2, 20,
                  "Prof. [Guide Name]  |  Assistant Professor, CSE Department",
                  fontSize=10, fontName="Helvetica-Bold",
                  fillColor=GRAY_DK, textAnchor="middle"))
    d4.add(String(PAGE_W/2, 5,
                  "Co-Guide: Prof. [Co-Guide Name]",
                  fontSize=9.5, fontName="Helvetica",
                  fillColor=GRAY, textAnchor="middle"))
    story.append(d4)
    story.append(sp(18))

    # Bottom info bar
    d5 = Drawing(PAGE_W, 36)
    d5.add(Rect(0, 0, PAGE_W, 36, fillColor=NAVY, strokeColor=NAVY))
    d5.add(String(PAGE_W/2, 22,
                  "Submitted in partial fulfillment of the requirements for the degree of",
                  fontSize=9, fontName="Helvetica",
                  fillColor=colors.HexColor("#bbdefb"), textAnchor="middle"))
    d5.add(String(PAGE_W/2, 7,
                  "Bachelor of Technology in Computer Science & Engineering (AI & ML)",
                  fontSize=10, fontName="Helvetica-Bold",
                  fillColor=WHITE, textAnchor="middle"))
    story.append(d5)
    story.append(PageBreak())
    return story

# ─── CERTIFICATE PAGE ─────────────────────────────────────────────────────────
def build_certificate(styles):
    story = []
    story.append(sp(15))
    story.append(Paragraph("CERTIFICATE", styles["pg_label"]))
    story.append(rule(NAVY, 2))
    story.append(sp(20))

    txt = [
        ("This is to certify that the project entitled"),
        (""),
        ("<b>\"SignAI: Real-Time AI-Powered Sign Language Translator with Text-to-Speech and Sentence Builder\"</b>"),
        (""),
        ("has been successfully completed by"),
        (""),
        ("<b>Himanshu Jagdish Patil</b>  (Roll No.: CS2024001)"),
        (""),
        ("in partial fulfillment of the requirements for the award of the degree of"),
        ("<b>Bachelor of Technology in Computer Science & Engineering (AI & ML)</b>"),
        ("from <b>Shri XYZ Institute of Technology</b>, affiliated to <b>XYZ University</b>,"),
        ("during the academic year <b>2024–2025</b>."),
        (""),
        ("The work embodied in this project report is original and has not been submitted"),
        ("to any other university or institution for the award of any degree or diploma."),
    ]
    for t in txt:
        story.append(Paragraph(t, styles["body_c"]))

    story.append(sp(30))

    sig_data = [
        ["Project Guide", "Co-Guide", "Head of Department"],
        ["Prof. [Guide Name]", "Prof. [Co-Guide Name]", "Prof. [HOD Name]"],
        ["Assistant Professor", "Assistant Professor", "Professor & HOD"],
        ["CSE Department", "CSE Department", "CSE Department"],
        ["Date: ___________", "Date: ___________", "Date: ___________"],
    ]
    cw = PAGE_W / 3
    rows = [[Paragraph(c, ParagraphStyle("sc", fontSize=10,
             fontName="Helvetica-Bold" if i==0 else "Helvetica",
             textColor=NAVY if i==0 else GRAY_DK,
             alignment=TA_CENTER, leading=15))
             for c in r]
            for i, r in enumerate(sig_data)]
    t = Table(rows, colWidths=[cw]*3)
    t.setStyle(TableStyle([
        ("ALIGN",  (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LINEABOVE", (0,0), (-1,0), 2, NAVY),
        ("LINEBELOW", (0,-1), (-1,-1), 0.5, GRAY_LN),
    ]))
    story.append(t)

    story.append(sp(30))
    story.append(thin_rule())
    story.append(Paragraph(
        "Examiner 1: ________________________  "
        "Examiner 2: ________________________  "
        "Date of Viva: ____________",
        ParagraphStyle("ex", fontSize=10, fontName="Helvetica",
                       textColor=GRAY, alignment=TA_CENTER)))
    story.append(PageBreak())
    return story

# ─── ACKNOWLEDGEMENT ──────────────────────────────────────────────────────────
def build_acknowledgement(styles):
    story = []
    story.append(sp(15))
    story.append(Paragraph("ACKNOWLEDGEMENT", styles["pg_label"]))
    story.append(rule(NAVY, 2))
    story.append(sp(12))

    paras = [
        "I express my sincere gratitude and heartfelt thanks to all those who guided and supported me throughout the course of this project.",
        "I am deeply grateful to my project guide, <b>Prof. [Guide Name]</b>, Assistant Professor, Department of Computer Science & Engineering, for their invaluable guidance, constant encouragement, and constructive suggestions throughout the development of this project. Their insightful feedback helped shape this work into its final form.",
        "I extend my sincere thanks to <b>Prof. [Co-Guide Name]</b> for their co-guidance and technical inputs that greatly improved the quality of this work.",
        "I am also thankful to <b>Prof. [HOD Name]</b>, Head of the Department of CSE, for providing the necessary facilities and a conducive research environment. The infrastructure and computational resources provided by the department were instrumental in the successful completion of this project.",
        "I would like to acknowledge the contributions of the open-source community, particularly the developers of <b>TensorFlow</b>, <b>MediaPipe</b>, <b>FastAPI</b>, and <b>React.js</b> — the foundational technologies upon which SignAI is built. The Kaggle community and Google Research for providing high-quality ASL datasets used in training the model.",
        "I extend my gratitude to my family for their unconditional support, patience, and encouragement throughout my academic journey. Their belief in me has been my greatest motivation.",
        "Lastly, I thank my friends and batchmates for the collaborative spirit, knowledge sharing, and the many productive discussions that enriched this work.",
    ]
    for p in paras:
        story.append(Paragraph(p, styles["abs_body"]))
        story.append(sp(6))

    story.append(sp(30))
    story.append(Paragraph(
        "<b>Himanshu Jagdish Patil</b><br/>"
        "B.Tech CSE (AI &amp; ML), Batch 2021–2025<br/>"
        "Roll No.: CS2024001<br/>"
        "himanshujagdishpatil914@gmail.com",
        ParagraphStyle("auth", fontSize=11, fontName="Helvetica",
                       textColor=GRAY_DK, alignment=TA_RIGHT,
                       leading=18)))
    story.append(PageBreak())
    return story

# ─── ABSTRACT ─────────────────────────────────────────────────────────────────
def build_abstract(styles):
    story = []
    story.append(sp(15))
    story.append(Paragraph("ABSTRACT", styles["pg_label"]))
    story.append(rule(NAVY, 2))
    story.append(sp(12))

    abs_text = [
        "Sign language is the primary mode of communication for millions of deaf and hearing-impaired individuals worldwide. Despite its widespread use, the vast majority of the hearing population cannot understand sign language, creating a significant communication barrier. This project presents <b>SignAI</b>, a real-time Artificial Intelligence-based sign language translator that bridges this communication gap using computer vision and deep learning technologies.",
        "SignAI is capable of detecting and classifying <b>40 distinct sign language gestures</b> in real time through a standard webcam. The system leverages <b>Google MediaPipe</b> for accurate hand landmark extraction, capturing 21 keypoints per hand (126 keypoints total for both hands) per frame, which are fed into a <b>Stacked Long Short-Term Memory (LSTM)</b> neural network architecture for temporal sequence classification. The trained model achieves a classification accuracy of <b>95% or above</b> with sufficient training data.",
        "The system supports <b>both single-hand and dual-hand sign detection</b>, making it robust for a wide range of ASL (American Sign Language) signs including alphabets, numbers, common phrases, expressions, and action words. A sliding window of 30 frames is used for prediction, ensuring smooth real-time performance at 15 frames per second.",
        "The project includes a <b>full-stack web application</b> built with React.js (frontend) and FastAPI (backend), connected via WebSockets for low-latency real-time communication. Key features include: (1) live camera feed with hand skeleton visualization, (2) animated sign detection display with confidence scores and top-5 predictions, (3) a Sentence Builder with Word Mode and Sentence Mode, (4) Text-to-Speech output using Google TTS, and (5) a searchable Sign Dictionary.",
        "The system was evaluated on a custom-collected dataset and the Google ASL Signs Kaggle dataset. Experimental results demonstrate high accuracy, low latency, and robust performance across varying lighting conditions and hand orientations. This project has significant potential as an assistive technology tool for inclusive communication.",
    ]
    for p in abs_text:
        story.append(Paragraph(p, styles["abs_body"]))
        story.append(sp(6))

    story.append(sp(14))
    story.append(rule(GRAY_LN))

    # Keywords box
    kw_box = Drawing(PAGE_W, 32)
    kw_box.add(Rect(0, 0, PAGE_W, 32,
                    fillColor=colors.HexColor("#e8f4fd"),
                    strokeColor=LBLUE, strokeWidth=1))
    kw_box.add(String(10, 18,
                      "Keywords:",
                      fontSize=10, fontName="Helvetica-Bold",
                      fillColor=NAVY))
    kw_box.add(String(75, 18,
                      "Sign Language Recognition, LSTM, MediaPipe, Hand Landmarks, "
                      "Real-Time Detection,",
                      fontSize=9.5, fontName="Helvetica", fillColor=GRAY_DK))
    kw_box.add(String(75, 6,
                      "Deep Learning, FastAPI, React.js, Text-to-Speech, "
                      "Assistive Technology, Computer Vision",
                      fontSize=9.5, fontName="Helvetica", fillColor=GRAY_DK))
    story.append(kw_box)
    story.append(PageBreak())
    return story
