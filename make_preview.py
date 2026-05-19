from PIL import Image, ImageDraw, ImageFont

W, H = 1400, 920
img = Image.new("RGB", (W, H), "#0f172a")
d   = ImageDraw.Draw(img)

BG_SURFACE  = "#1e293b"
BG_ELEVATED = "#273548"
BORDER      = "#334155"
TEXT_PRI    = "#f1f5f9"
TEXT_MUT    = "#94a3b8"
ACCENT      = "#6366f1"
ACCENT2     = "#818cf8"
SUCCESS     = "#22c55e"
DANGER      = "#ef4444"
PURPLE      = "#7c3aed"
CYAN        = "#06b6d4"
INDIGO_DARK = "#4338ca"

def fnt(size, bold=False):
    try:
        p = "/usr/share/fonts/truetype/dejavu/DejaVuSans{}.ttf".format("-Bold" if bold else "")
        return ImageFont.truetype(p, size)
    except:
        return ImageFont.load_default()

def txt(x, y, s, color=TEXT_PRI, size=14, bold=False, anchor="lt"):
    d.text((x, y), s, fill=color, font=fnt(size, bold), anchor=anchor)

def rect(x1,y1,x2,y2,fill=None,outline=None,r=0):
    if r: d.rounded_rectangle([x1,y1,x2,y2], radius=r, fill=fill, outline=outline)
    else: d.rectangle([x1,y1,x2,y2], fill=fill, outline=outline)

def pill(x1,y1,x2,y2,fill,label,lc=TEXT_PRI,fs=12,bold=False):
    d.rounded_rectangle([x1,y1,x2,y2], radius=20, fill=fill)
    d.text(((x1+x2)//2,(y1+y2)//2), label, fill=lc, font=fnt(fs,bold), anchor="mm")

def btn(x,y,w,h,label,bg=BG_ELEVATED,fg=TEXT_PRI,fs=12):
    d.rounded_rectangle([x,y,x+w,y+h], radius=9, fill=bg, outline=BORDER)
    d.text(((x+x+w)//2,(y+y+h)//2), label, fill=fg, font=fnt(fs,True), anchor="mm")

def hbar(x,y,bw,bh,pct,col=SUCCESS):
    d.rounded_rectangle([x,y,x+bw,y+bh], radius=4, fill=BG_ELEVATED)
    fw = max(4, int(bw*pct/100))
    d.rounded_rectangle([x,y,x+fw,y+bh], radius=4, fill=col)

PAD = 30

# ── HEADER ────────────────────────────────────────────────────────────────────
txt(PAD, 20, "SignAI", color=ACCENT2, size=28, bold=True)
txt(PAD, 56, "Real-time Sign Language Translator", color=TEXT_MUT, size=11)
d.rounded_rectangle([W-200,22,W-110,48], radius=13, fill=BG_ELEVATED, outline=BORDER)
txt(W-155, 35, "40 Signs", color=TEXT_MUT, size=11, bold=True, anchor="mm")
d.rounded_rectangle([W-102,22,W-PAD,48], radius=13, fill=ACCENT)
txt(W-66, 35, "AI Powered", color="#fff", size=11, bold=True, anchor="mm")
d.line([(PAD,70),(W-PAD,70)], fill=BORDER, width=1)

# ── STATUS BAR ────────────────────────────────────────────────────────────────
rect(PAD,78,W-PAD,108, fill=BG_SURFACE, outline=BORDER, r=10)
d.ellipse([PAD+16,90,PAD+26,100], fill=SUCCESS)
txt(PAD+34, 94, "Connected", color=SUCCESS, size=11, bold=True, anchor="lm")
d.ellipse([PAD+170,90,PAD+180,100], fill=SUCCESS)
txt(PAD+188, 94, "Hand Detected", color=SUCCESS, size=11, bold=True, anchor="lm")
txt(W-PAD-180, 94, "WebSocket: Active  |  15 fps  |  Model Loaded", color=TEXT_MUT, size=10, anchor="lm")

# ── TAB NAV ───────────────────────────────────────────────────────────────────
d.rounded_rectangle([PAD,116,PAD+160,144], radius=9, fill=ACCENT)
txt(PAD+80,130,"Translator", color="#fff", size=12, bold=True, anchor="mm")
d.rounded_rectangle([PAD+170,116,PAD+316,144], radius=9, fill=BG_SURFACE, outline=BORDER)
txt(PAD+243,130,"Sign List", color=TEXT_MUT, size=12, bold=True, anchor="mm")

# ═══════════════════════════════════════════════════════════════════════════════
# LEFT PANEL — Camera
# ═══════════════════════════════════════════════════════════════════════════════
LX1, LX2 = PAD, 670
PY = 156
rect(LX1,PY,LX2,H-28, fill=BG_SURFACE, outline=BORDER, r=16)
txt(LX1+18, PY+14, "Live Camera Feed", color=TEXT_PRI, size=13, bold=True)

# Camera box
CY1, CY2 = PY+46, PY+46+390
for i in range(CY2-CY1):
    t = i/(CY2-CY1)
    r2 = int(10 + 22*t); g2 = int(10 + 33*t); b2 = int(15 + 62*t)
    d.line([(LX1+14,CY1+i),(LX2-14,CY1+i)], fill=(r2,g2,b2))
rect(LX1+14,CY1,LX2-14,CY2, outline=BORDER, r=12)

# Hand skeleton
cx = (LX1+LX2)//2 - 10
cy = (CY1+CY2)//2 + 10
S  = 1.25
lm = {
    0:(0,85),1:(-28,58),2:(-48,32),3:(-60,12),4:(-70,-8),
    5:(-22,12),6:(-24,-20),7:(-26,-50),8:(-28,-76),
    9:(0,10),10:(2,-22),11:(4,-52),12:(6,-80),
    13:(22,14),14:(24,-16),15:(26,-46),16:(28,-70),
    17:(40,20),18:(42,-2),19:(44,-26),20:(46,-48),
}
conns=[(0,1),(1,2),(2,3),(3,4),(0,5),(5,6),(6,7),(7,8),(0,9),(9,10),(10,11),(11,12),
       (0,13),(13,14),(14,15),(15,16),(0,17),(17,18),(18,19),(19,20),(5,9),(9,13),(13,17)]
def lp(i): return (cx+int(lm[i][0]*S), cy+int(lm[i][1]*S))
for a,b in conns: d.line([lp(a),lp(b)], fill="#15803d", width=2)
tips={4,8,12,16,20}
for i in lm:
    r3=5 if i in tips else 3
    px,py2=lp(i)
    d.ellipse([px-r3,py2-r3,px+r3,py2+r3], fill=SUCCESS if i in tips else "#4ade80")

# LIVE badge
d.rounded_rectangle([LX2-90,CY1+10,LX2-18,CY1+34], radius=10, fill=DANGER)
txt(LX2-54, CY1+22, "LIVE", color="#fff", size=10, bold=True, anchor="mm")
d.ellipse([LX2-84,CY1+17,LX2-74,CY1+27], fill="#fff")

# Buttons
btn(LX1+16, CY2+12, 130, 36, "Stop Detecting", bg="#450a0a", fg=DANGER)
btn(LX1+156,CY2+12, 110, 36, "Mirror",         bg=BG_ELEVATED, fg=TEXT_PRI)
txt(LX1+18, CY2+58, "Detecting in real-time — hold your sign steady", color=TEXT_MUT, size=10)

# Confidence mini display inside camera
d.rounded_rectangle([LX1+14,CY2-46,LX2-14,CY2-2], radius=0, fill="rgba(15,23,42,180)")
d.rounded_rectangle([LX1+14,CY2-46,LX2-14,CY2-2], radius=0, fill=(15,23,42,180))
# simple bar at bottom
rect(LX1+14,CY2-46,LX2-14,CY2-2, fill=(15,23,42), r=0)
txt(LX1+22, CY2-40, "Detected:", color=TEXT_MUT, size=10)
txt(LX1+100,CY2-40, "hello", color=SUCCESS, size=11, bold=True)
hbar(LX1+22, CY2-22, 360, 8, 96.2, col=SUCCESS)
txt(LX2-50, CY2-22, "96.2%", color=SUCCESS, size=10, bold=True)

# ═══════════════════════════════════════════════════════════════════════════════
# RIGHT PANEL — Results
# ═══════════════════════════════════════════════════════════════════════════════
RX1, RX2 = 690, W-PAD
rect(RX1,PY,RX2,H-28, fill=BG_SURFACE, outline=BORDER, r=16)

# ── Detected Sign card ────────────────────────────────────────────────────────
txt(RX1+18, PY+14, "Detected Sign", color=TEXT_PRI, size=13, bold=True)
d.rounded_rectangle([RX1+16,PY+44,RX2-16,PY+200], radius=14, fill="#1e1b4b", outline=INDIGO_DARK)

# Big sign word — layered for glow
for off,col in [(3,"#312e81"),(2,"#4338ca"),(1,"#7c3aed"),(0,"#c084fc")]:
    d.text(((RX1+RX2)//2+off, PY+128+off), "hello",
           fill=col, font=fnt(58,True), anchor="mm")

# Confidence
hbar(RX1+28, PY+168, RX2-88, 14, 96.2, col=SUCCESS)
txt(RX2-76, PY+168, "96.2%", color=SUCCESS, size=13, bold=True)

# Top-5
d.line([(RX1+16,PY+204),(RX2-16,PY+204)], fill=BORDER, width=1)
txt(RX1+18, PY+212, "Top Predictions", color=TEXT_MUT, size=10, bold=True)

top5 = [("hello",96.2,SUCCESS),("good",2.1,ACCENT),("yes",0.9,ACCENT),
        ("please",0.5,ACCENT),("fine",0.3,ACCENT)]
for i,(lb,pr,col) in enumerate(top5):
    ty = PY+232+i*22
    txt(RX1+22, ty+1, f"#{i+1}", color=TEXT_MUT, size=10, anchor="lm")
    txt(RX1+50, ty+1, lb, color=TEXT_PRI, size=10, bold=(i==0), anchor="lm")
    bx = RX1+145
    bw = 190
    d.rounded_rectangle([bx,ty-4,bx+bw,ty+6], radius=3, fill=BG_ELEVATED)
    fw = max(3, int(bw*pr/100))
    d.rounded_rectangle([bx,ty-4,bx+fw,ty+6], radius=3, fill=col)
    txt(bx+bw+8, ty+1, f"{pr}%", color=TEXT_MUT, size=9, anchor="lm")

# ── Sentence Builder ──────────────────────────────────────────────────────────
SBY = PY+350
d.line([(RX1+16,SBY-10),(RX2-16,SBY-10)], fill=BORDER, width=1)
txt(RX1+18, SBY, "Sentence Builder", color=TEXT_PRI, size=13, bold=True)

# Mode toggle
d.rounded_rectangle([RX2-220,SBY-2,RX2-120,SBY+26], radius=8, fill=BG_ELEVATED, outline=BORDER)
txt(RX2-170,SBY+12,"Words",color=TEXT_MUT,size=10,bold=True,anchor="mm")
d.rounded_rectangle([RX2-112,SBY-2,RX2-16,SBY+26], radius=8, fill=ACCENT)
txt(RX2-64,SBY+12,"Sentence",color="#fff",size=10,bold=True,anchor="mm")

# Chips area
CHP_Y = SBY+34
d.rounded_rectangle([RX1+16,CHP_Y,RX2-16,CHP_Y+58], radius=10, fill=BG_ELEVATED, outline=BORDER)
chips=[("hello",ACCENT),("howareyou",PURPLE),("iloveyou","#2563eb"),("thankyou",CYAN),("good","#059669")]
cpx = RX1+28
for lb,col in chips:
    cw=int(fnt(11,True).getlength(lb))+26
    d.rounded_rectangle([cpx,CHP_Y+10,cpx+cw,CHP_Y+44], radius=20, fill=col)
    txt((cpx+cpx+cw)//2, CHP_Y+27, lb, color="#fff", size=11, bold=True, anchor="mm")
    cpx+=cw+8

# Full sentence
STY=CHP_Y+66
d.rounded_rectangle([RX1+16,STY,RX2-16,STY+40], radius=10, fill=BG_ELEVATED)
d.rectangle([RX1+16,STY,RX1+22,STY+40], fill=ACCENT)
txt(RX1+32,STY+20,"hello  howareyou  iloveyou  thankyou  good", color=TEXT_PRI, size=11, anchor="lm")

# Action buttons row
BTY=STY+50
btn(RX1+16,    BTY,168,36,"Speak",    bg=ACCENT,    fg="#fff")
btn(RX1+192,   BTY, 88,36,"Copy",     bg=BG_ELEVATED,fg=TEXT_PRI)
btn(RX1+288,   BTY, 88,36,"Undo",     bg=BG_ELEVATED,fg=TEXT_PRI)
btn(RX1+384,   BTY, 88,36,"Clear",    bg="#450a0a",  fg=DANGER)

# Quick Add
QY2=BTY+48
txt(RX1+18,QY2,"Quick Add:", color=TEXT_MUT, size=10)
qwords=["hello","yes","no","please","thankyou","sorry","help","good","iloveyou","stop"]
qx2=RX1+18; qy3=QY2+18
for w in qwords:
    qw=int(fnt(10).getlength(w))+20
    d.rounded_rectangle([qx2,qy3,qx2+qw,qy3+26], radius=13, fill=BG_ELEVATED, outline=BORDER)
    txt((qx2+qx2+qw)//2,qy3+13,w,color=TEXT_MUT,size=10,anchor="mm")
    qx2+=qw+6
    if qx2 > RX2-80: qx2=RX1+18; qy3+=32

# ── Footer bar ────────────────────────────────────────────────────────────────
d.rounded_rectangle([W//2-280,H-22,W//2+280,H-4], radius=6, fill=BG_ELEVATED, outline=BORDER)
txt(W//2,H-13,"SignAI  |  AI Sign Language Translator  |  Final Year Project  |  Himanshu Jagdish Patil",
    color=TEXT_MUT, size=9, anchor="mm")

img.save("/projects/sandbox/Himanshu/frontend_screenshot.png","PNG")
print("Done!")
