"""
SignAI Project Report — Master Build Script
Assembles all 6 parts into a single professional PDF.
Output: SignAI_Project_Report.pdf
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Spacer, PageBreak
from reportlab.lib import colors

# ── Import all parts ──────────────────────────────────────────────────────────
from report_p1 import (
    make_styles, page_draw, first_page,
    build_cover, build_certificate, build_acknowledgement, build_abstract,
)
from report_p2 import build_toc, build_lof, build_lot, build_ch1
from report_p3 import build_ch2, build_ch2_extra
from report_p4 import build_ch3, build_ch3_extra
from report_p5 import build_ch4, build_ch4_extra
from report_p6 import build_ch5, build_ch5_extra, build_ch6, build_references, build_appendix

W, H   = A4
OUTPUT = os.path.join(os.path.dirname(__file__), "SignAI_Project_Report.pdf")


def build():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=25*mm, rightMargin=25*mm,
        topMargin=24*mm,  bottomMargin=22*mm,
        title="SignAI: Real-Time AI Sign Language Translator — Project Report",
        author="Himanshu Jagdish Patil",
        subject="B.Tech Final Year Project Report — CSE (AI & ML)",
        creator="SignAI Report Builder",
    )

    styles = make_styles()
    story  = []

    # ── Front matter (no header/footer) ──────────────────────────────────────
    story += build_cover(styles)            # Page 1
    story += build_certificate(styles)      # Page 2
    story += build_acknowledgement(styles)  # Page 3
    story += build_abstract(styles)         # Page 4

    # ── Prelims ───────────────────────────────────────────────────────────────
    story += build_toc(styles)              # Page 5
    story += build_lof(styles)              # Page 6
    story += build_lot(styles)              # Page 7

    # ── Chapters ──────────────────────────────────────────────────────────────
    story += build_ch1(styles)   # Chapter 1 — Introduction
    story += build_ch2(styles)   # Chapter 2 — Literature Review
    story += build_ch2_extra(styles)  # Chapter 2 continued
    story += build_ch3(styles)   # Chapter 3 — System Design
    story += build_ch3_extra(styles)  # Chapter 3 continued
    story += build_ch4(styles)   # Chapter 4 — Implementation
    story += build_ch4_extra(styles)  # Chapter 4 continued
    story += build_ch5(styles)   # Chapter 5 — Results
    story += build_ch5_extra(styles)  # Chapter 5 continued
    story += build_ch6(styles)   # Chapter 6 — Conclusion

    # ── Back matter ───────────────────────────────────────────────────────────
    story += build_references(styles)
    story += build_appendix(styles)

    print(f"[BUILD] Total flowables: {len(story)}")
    print(f"[BUILD] Building PDF → {OUTPUT}")

    doc.build(
        story,
        onFirstPage=first_page,   # cover: no header/footer
        onLaterPages=page_draw,   # all other pages: header + footer + page number
    )

    size_kb = os.path.getsize(OUTPUT) // 1024
    print(f"[DONE]  PDF saved → {OUTPUT}  ({size_kb} KB)")


if __name__ == "__main__":
    build()
