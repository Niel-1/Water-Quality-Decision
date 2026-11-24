"""
Generator Presentasi Final Project Teknologi Logika Fuzzy (Kelompok 1)
Format: 15 Slide Widescreen 16:9 (.pptx) siap edit di PowerPoint, Google Slides, dan Canva.
Palet warna 100% mengikuti palet & aura gradien Canva pengguna (#EEF2F3, #FFFFFF, #4735F3 -> #61DD99).
Tanpa stock image: seluruh visual menggunakan diagram asli, tabel native, dan tangkapan layar GUI Streamlit.
"""

import io
from functools import lru_cache
from pathlib import Path
import numpy as np
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / "docs" / "figures"
OUT_PPTX = ROOT / "docs" / "Presentasi_Final_Project_TLF_Kelompok_1.pptx"

# Palet Warna Exact Canva (PPT Proposal Bisnis Presentasi Gradien Modern Biru Hijau)
C_BG = RGBColor(0xEE, 0xF2, 0xF3)           # #EEF2F3 - Canva Airy Canvas
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)        # #FFFFFF - Crisp Card Surface
C_BORDER = RGBColor(0xD2, 0xDF, 0xEC)       # #D2DFEC - Cool Ice-Blue Card Border
C_PRIMARY = RGBColor(0x47, 0x35, 0xF3)      # #4735F3 - Canva Electric Blue-Indigo (Stop 0)
C_BLUE_MID = RGBColor(0x4E, 0x7A, 0xE8)     # #4E7AE8 - Mid Gradient Sky-Cobalt
C_PRIMARY_DARK = RGBColor(0x31, 0x24, 0xB8) # #3124B8 - Deep Cobalt for soft-pill text
C_PRIMARY_SOFT = RGBColor(0xEC, 0xEE, 0xFF) # #ECEEFF - Luminous Soft Indigo Tint
C_MINT = RGBColor(0x4E, 0x7A, 0xE8)         # Mid-gradient cobalt-aqua for crisp table headers
C_MINT_PURE = RGBColor(0x61, 0xDD, 0x99)    # #61DD99 - Exact Canva SVG Gradient Stop 1
C_MINT_LIGHT = RGBColor(0x61, 0xDD, 0x99)   # #61DD99 - Canva Bright Mint
C_MINT_TEXT = RGBColor(0x16, 0x9B, 0x6A)    # #169B6A - High-contrast mint for readable text on white
C_MINT_SOFT = RGBColor(0xE6, 0xFA, 0xF0)    # #E6FAF0 - Soft Mint Tint
C_INK = RGBColor(0x18, 0x1E, 0x34)          # #181E34 - Soft Deep Navy Ink
C_BODY = RGBColor(0x36, 0x41, 0x58)         # #364158 - Slate Navy Body Text
C_MUTED = RGBColor(0x5E, 0x6C, 0x86)        # #5E6C86 - Secondary / Captions
C_ROW_ALT = RGBColor(0xF5, 0xF8, 0xFD)      # #F5F8FD - Cool Airy Table Zebra Row
C_CORAL = RGBColor(0xD9, 0x46, 0x6F)        # #D9466F - Harmonized Rose for Poor / Error
C_CORAL_SOFT = RGBColor(0xFD, 0xEE, 0xF2)   # #FDEEF2 - Soft Rose Tint

FONT_HEAD = "Poppins"
FONT_BODY = "Poppins"

TOTAL_SLIDES = 15


@lru_cache(maxsize=4)
def _make_aura_bg_bytes(variant: str = "content") -> bytes:
    """Generate smooth 16:9 Canva-style airy #EEF2F3 canvas with luminous #4735F3 -> #61DD99 corner auras."""
    W, H = 1600, 900
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    xn = xx / float(W)
    yn = yy / float(H)

    # Base #EEF2F3
    r = np.full((H, W), 238.0, dtype=np.float32)
    g = np.full((H, W), 242.0, dtype=np.float32)
    b = np.full((H, W), 243.0, dtype=np.float32)

    if variant == "cover":
        blobs = [
            # Top-right electric blue + mint luminous aura
            (0.92, 0.04, 0.28, 0.30, (71, 53, 243), 0.42),
            (0.76, 0.06, 0.26, 0.28, (97, 221, 153), 0.36),
            # Bottom-left electric blue + mint luminous aura
            (0.05, 0.96, 0.28, 0.30, (71, 53, 243), 0.42),
            (0.24, 0.96, 0.26, 0.26, (97, 221, 153), 0.34),
            # Subtle top-left mint mist
            (0.04, 0.06, 0.22, 0.24, (97, 221, 153), 0.16),
        ]
    else:
        blobs = [
            # Top-right glowing blue-mint aura matching Canva Page 2 exactly
            (0.92, 0.00, 0.24, 0.22, (71, 53, 243), 0.40),
            (0.76, 0.02, 0.20, 0.18, (97, 221, 153), 0.30),
            (0.84, 0.08, 0.22, 0.18, (88, 123, 240), 0.22),
            # Bottom-left glowing blue-mint aura matching Canva Page 2 exactly
            (0.03, 0.98, 0.22, 0.22, (71, 53, 243), 0.42),
            (0.18, 0.99, 0.20, 0.16, (97, 221, 153), 0.28),
            (0.10, 0.92, 0.18, 0.16, (88, 123, 240), 0.20),
        ]

    for cx, cy, sx, sy, (cr, cg, cb), alpha_max in blobs:
        dist2 = ((xn - cx) / sx) ** 2 + ((yn - cy) / sy) ** 2
        w = alpha_max * np.exp(-0.5 * dist2)
        r = r * (1.0 - w) + cr * w
        g = g * (1.0 - w) + cg * w
        b = b * (1.0 - w) + cb * w

    arr = np.clip(np.dstack([r, g, b]), 0, 255).astype(np.uint8)
    buf = io.BytesIO()
    Image.fromarray(arr, mode="RGB").save(buf, format="JPEG", quality=92, optimize=True)
    return buf.getvalue()


def _apply_gradient(shp, c_start=C_PRIMARY, c_end=C_MINT_PURE, angle=0.0):
    """Apply native PowerPoint/Canva 2-stop linear gradient fill (#4735F3 -> #61DD99)."""
    fill = shp.fill
    fill.gradient()
    fill.gradient_angle = angle
    stops = fill.gradient_stops
    stops[0].position = 0.0
    stops[0].color.rgb = c_start
    stops[1].position = 1.0
    stops[1].color.rgb = c_end


def _new_slide(prs: Presentation, variant: str = "content"):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = C_BG
    # Place smooth Canva blue-mint aura background behind all slide elements
    slide.shapes.add_picture(
        io.BytesIO(_make_aura_bg_bytes(variant)),
        Inches(0.0),
        Inches(0.0),
        width=Inches(13.333),
        height=Inches(7.5),
    )
    return slide


def _add_rect(slide, x, y, w, h, fill_rgb, border_rgb=None, border_pt=0.75, rounded=False, grad_angle=None):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shp = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
    if rounded:
        try:
            shp.adjustments[0] = 0.07
        except Exception:
            pass
    if grad_angle is not None:
        _apply_gradient(shp, C_PRIMARY, C_MINT_PURE, angle=grad_angle)
    elif fill_rgb is not None:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill_rgb
    else:
        shp.fill.background()
    if border_rgb is not None:
        shp.line.color.rgb = border_rgb
        shp.line.width = Pt(border_pt)
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def _add_pill(
    slide,
    x,
    y,
    w,
    h,
    text,
    bg_rgb,
    fg_rgb,
    font_size=10,
    bold=True,
    gradient=False,
    border_rgb=None,
    border_pt=1.0,
    align=PP_ALIGN.CENTER,
):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    try:
        shp.adjustments[0] = 0.5
    except Exception:
        pass
    if gradient:
        _apply_gradient(shp, C_PRIMARY, C_MINT_PURE, angle=0.0)
    elif bg_rgb is not None:
        shp.fill.solid()
        shp.fill.fore_color.rgb = bg_rgb
    else:
        shp.fill.background()
    if border_rgb is not None:
        shp.line.color.rgb = border_rgb
        shp.line.width = Pt(border_pt)
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    tf = shp.text_frame
    tf.word_wrap = False
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.14)
    tf.margin_right = Inches(0.14)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.name = FONT_HEAD
    r.font.size = Pt(font_size)
    r.font.bold = bold
    r.font.color.rgb = fg_rgb
    return shp


def _add_text(
    slide,
    x,
    y,
    w,
    h,
    text,
    size=12,
    bold=False,
    italic=False,
    color=C_BODY,
    align=PP_ALIGN.LEFT,
    font=FONT_BODY,
    line_spacing=1.18,
    valign=MSO_ANCHOR.TOP,
):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = valign
    tf.margin_left = Inches(0.02)
    tf.margin_right = Inches(0.02)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    lines = text.split("\n")
    for idx, line in enumerate(lines):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        if idx > 0:
            p.space_before = Pt(3)
        r = p.add_run()
        r.text = line
        r.font.name = font
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = color
    return tb


def _add_bullets(slide, x, y, w, h, items, size=11.5, color=C_BODY, space_after=6, line_spacing=1.18):
    """items: list of (bold_prefix, body_text)"""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.02)
    tf.margin_right = Inches(0.02)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    for idx, (prefix, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.space_after = Pt(space_after)
        p.line_spacing = line_spacing
        r0 = p.add_run()
        r0.text = "●  "
        r0.font.name = FONT_HEAD
        r0.font.size = Pt(max(7.5, size - 2.0))
        r0.font.bold = True
        r0.font.color.rgb = C_MINT_TEXT
        if prefix:
            r1 = p.add_run()
            r1.text = prefix
            r1.font.name = FONT_HEAD
            r1.font.size = Pt(size)
            r1.font.bold = True
            r1.font.color.rgb = C_INK
        r2 = p.add_run()
        r2.text = body
        r2.font.name = FONT_BODY
        r2.font.size = Pt(size)
        r2.font.color.rgb = color
    return tb


def _add_image_fit(slide, img_path: Path, x, y, max_w, max_h):
    with Image.open(img_path) as im:
        iw, ih = im.size
    ratio = iw / ih
    box_ratio = max_w / max_h
    if ratio >= box_ratio:
        w = max_w
        h = w / ratio
    else:
        h = max_h
        w = h * ratio
    cx = x + (max_w - w) / 2.0
    cy = y + (max_h - h) / 2.0
    return slide.shapes.add_picture(str(img_path), Inches(cx), Inches(cy), width=Inches(w), height=Inches(h))


def _add_table(
    slide,
    x,
    y,
    w,
    h,
    headers,
    rows,
    col_widths,
    font_size=10,
    header_bg=C_PRIMARY,
    aligns=None,
    row_bg_fn=None,
    highlight_col=None,
    margin_lr=0.04,
):
    n_rows = len(rows) + 1
    n_cols = len(headers)
    tbl_shape = slide.shapes.add_table(n_rows, n_cols, Inches(x), Inches(y), Inches(w), Inches(h))
    tbl = tbl_shape.table
    for ci, cw in enumerate(col_widths):
        tbl.columns[ci].width = Inches(cw)

    # Header
    for ci, text in enumerate(headers):
        cell = tbl.cell(0, ci)
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_bg
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = Inches(margin_lr)
        cell.margin_right = Inches(margin_lr)
        cell.margin_top = Inches(0.03)
        cell.margin_bottom = Inches(0.03)
        p = cell.text_frame.paragraphs[0]
        p.alignment = aligns[ci] if aligns else PP_ALIGN.CENTER
        r = p.add_run()
        r.text = str(text)
        r.font.name = FONT_HEAD
        r.font.size = Pt(font_size)
        r.font.bold = True
        r.font.color.rgb = C_WHITE

    # Body rows
    for ri, row in enumerate(rows):
        default_bg = C_WHITE if ri % 2 == 0 else C_ROW_ALT
        for ci, val in enumerate(row):
            cell = tbl.cell(ri + 1, ci)
            bg_c = row_bg_fn(ri, ci, val) if row_bg_fn else default_bg
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_c
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = Inches(margin_lr)
            cell.margin_right = Inches(margin_lr)
            cell.margin_top = Inches(0.025)
            cell.margin_bottom = Inches(0.025)
            p = cell.text_frame.paragraphs[0]
            p.alignment = aligns[ci] if aligns else PP_ALIGN.CENTER
            r = p.add_run()
            r.text = str(val)
            r.font.name = FONT_BODY
            r.font.size = Pt(font_size)
            is_bold = (ci == 0) or (highlight_col is not None and ci == highlight_col)
            r.font.bold = is_bold
            if bg_c == C_MINT_SOFT:
                r.font.color.rgb = C_MINT_TEXT
            elif bg_c == C_CORAL_SOFT:
                r.font.color.rgb = C_CORAL
            elif bg_c == C_PRIMARY_SOFT:
                r.font.color.rgb = C_PRIMARY_DARK
            else:
                r.font.color.rgb = C_INK if is_bold else C_BODY
    return tbl_shape


def _add_chrome(slide, page_num: int, section_tag: str, title: str, subtitle: str = ""):
    """Exact Canva signature capsule top bar, electric-blue title, and PAGE | XX gradient pill footer."""
    # Top signature Canva capsule bar (white pill with #4735F3 border + gradient right cap)
    _add_pill(
        slide,
        0.55,
        0.18,
        12.23,
        0.34,
        "KELOMPOK 1  ·  INFORMATIKA UNIVERSITAS UDAYANA",
        C_WHITE,
        C_PRIMARY,
        font_size=9.2,
        bold=True,
        border_rgb=C_PRIMARY,
        border_pt=1.0,
        align=PP_ALIGN.LEFT,
    )
    _add_pill(
        slide,
        9.85,
        0.18,
        2.93,
        0.34,
        section_tag.upper(),
        None,
        C_WHITE,
        font_size=9.0,
        bold=True,
        gradient=True,
    )

    # Main slide title in Canva Electric Blue (#4735F3) + clean slate subtitle
    _add_text(slide, 0.55, 0.58, 12.23, 0.48, title, size=23, bold=True, color=C_PRIMARY, font=FONT_HEAD)
    if subtitle:
        _add_text(slide, 0.55, 1.05, 12.23, 0.34, subtitle, size=11.0, color=C_BODY)

    # Subtle gradient hairline divider below header
    div_y = 1.42 if subtitle else 1.14
    _add_rect(slide, 0.55, div_y, 12.23, 0.022, None, grad_angle=0.0)

    # Footer: Canva-style bottom-left outline pill & bottom-right PAGE | XX split pill
    _add_pill(
        slide,
        0.55,
        7.04,
        3.15,
        0.30,
        "WATER-QUALITY-DECISION",
        C_WHITE,
        C_PRIMARY,
        font_size=8.6,
        bold=True,
        border_rgb=C_BLUE_MID,
        border_pt=0.9,
    )
    _add_text(
        slide,
        3.85,
        7.08,
        6.5,
        0.24,
        "Fuzzy Mamdani (27 Rules) + KNN 4D  ·  github.com/dhikrtika/Water-Quality-Decision",
        size=8.4,
        color=C_MUTED,
    )
    _add_pill(
        slide,
        11.20,
        7.04,
        1.58,
        0.30,
        "PAGE",
        C_WHITE,
        C_PRIMARY,
        font_size=8.6,
        bold=True,
        border_rgb=C_PRIMARY,
        border_pt=0.9,
        align=PP_ALIGN.LEFT,
    )
    _add_pill(
        slide,
        12.06,
        7.04,
        0.72,
        0.30,
        f"{page_num:02d}",
        None,
        C_WHITE,
        font_size=9.0,
        bold=True,
        gradient=True,
    )


def _add_card(slide, x, y, w, h, title=None, accent_rgb=None, fill_rgb=C_WHITE):
    _add_rect(slide, x, y, w, h, fill_rgb, border_rgb=C_BORDER, border_pt=0.85, rounded=True)
    if accent_rgb is not None:
        # Use Canva's signature vertical blue-to-mint gradient stripe on cards
        _add_rect(slide, x + 0.14, y + 0.13, 0.075, h - 0.26, None, grad_angle=90.0)
    if title:
        tx = x + (0.30 if accent_rgb else 0.18)
        tw = w - (0.44 if accent_rgb else 0.36)
        _add_text(slide, tx, y + 0.12, tw, 0.34, title, size=12.8, bold=True, color=C_PRIMARY, font=FONT_HEAD)


def _add_kpi_tile(slide, x, y, w, h, label, value, caption, accent=C_PRIMARY, soft=C_PRIMARY_SOFT):
    _add_rect(slide, x, y, w, h, C_WHITE, border_rgb=C_BORDER, border_pt=0.85, rounded=True)
    if accent == C_CORAL:
        _add_rect(slide, x, y, w, 0.08, C_CORAL)
    else:
        _add_rect(slide, x, y, w, 0.08, None, grad_angle=0.0)
    _add_text(slide, x + 0.16, y + 0.14, w - 0.32, 0.24, label.upper(), size=8.8, bold=True, color=C_MUTED)
    val_color = C_MINT_TEXT if accent in (C_MINT, C_MINT_PURE) else accent
    _add_text(slide, x + 0.16, y + 0.38, w - 0.32, 0.46, value, size=22.5, bold=True, color=val_color, font=FONT_HEAD)
    _add_text(slide, x + 0.16, y + 0.86, w - 0.32, 0.28, caption, size=9.3, color=C_BODY)


def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # =========================================================================
    # SLIDE 01: COVER (Exact Canva Aura + #4735F3 -> #61DD99 Gradient Identity)
    # =========================================================================
    s1 = _new_slide(prs, variant="cover")

    # Top Canva capsule header on Cover
    _add_pill(
        s1,
        0.65,
        0.38,
        8.25,
        0.38,
        "KELOMPOK 1  ·  INFORMATIKA FMIPA UNIVERSITAS UDAYANA",
        C_WHITE,
        C_PRIMARY,
        font_size=9.5,
        bold=True,
        border_rgb=C_PRIMARY,
        border_pt=1.0,
        align=PP_ALIGN.LEFT,
    )
    _add_pill(
        s1,
        6.25,
        0.38,
        2.65,
        0.38,
        "FINAL PROJECT TLF 2026",
        None,
        C_WHITE,
        font_size=9.2,
        bold=True,
        gradient=True,
    )

    # Left panel: Logo + Gradient Pill + Electric Blue Hero Title + Description
    logo_path = FIG_DIR / "logo_unud.png"
    if logo_path.exists():
        _add_image_fit(s1, logo_path, 0.65, 1.02, 0.86, 0.86)
    _add_pill(
        s1,
        1.68,
        1.24,
        4.15,
        0.40,
        "FUZZY MAMDANI (27 RULES) + KNN 4D",
        None,
        C_WHITE,
        font_size=10,
        bold=True,
        gradient=True,
    )

    _add_text(
        s1,
        0.65,
        2.06,
        8.4,
        1.95,
        "WATER QUALITY\nDECISION SUPPORT\nSYSTEM",
        size=42,
        bold=True,
        color=C_PRIMARY,
        font=FONT_HEAD,
        line_spacing=1.02,
    )
    _add_text(
        s1,
        0.65,
        4.22,
        8.25,
        1.10,
        "Sistem pendukung keputusan berbasis Fuzzy Mamdani (kurva segitiga simetris, 27 basis aturan, defuzzifikasi Centroid analitik) yang diintegrasikan dengan Fuzzy-Enhanced K-Nearest Neighbors untuk klasifikasi kelayakan air minum (Potable vs Not Potable).",
        size=12.6,
        color=C_BODY,
        line_spacing=1.28,
    )

    # Bottom team card on left panel
    _add_rect(s1, 0.65, 5.62, 8.25, 1.15, C_WHITE, border_rgb=C_BLUE_MID, border_pt=1.0, rounded=True)
    _add_rect(s1, 0.65, 5.62, 8.25, 0.08, None, grad_angle=0.0)
    _add_text(s1, 0.90, 5.80, 4.5, 0.26, "ANGGOTA KELOMPOK 1  ·  INFORMATIKA UNUD", size=9.8, bold=True, color=C_PRIMARY)
    _add_text(
        s1,
        0.90,
        6.10,
        7.8,
        0.54,
        "Nathanael Adrian W. (013)  ·  I Wayan Arya Adi G. (019)  ·  Komang Dhika Artika N. (055)\nKadek Phatra Adisuta T. (076)  ·  I Putu Maichail Ganio W. (123)",
        size=10.2,
        color=C_INK,
        line_spacing=1.28,
    )

    # Right luminous gradient card (#4735F3 -> #61DD99, zero stock image!)
    _add_rect(s1, 9.25, 0.38, 3.55, 6.74, None, rounded=True, grad_angle=135.0)
    _add_text(s1, 9.56, 0.64, 2.95, 0.30, "RINGKASAN CAPAIAN", size=10.5, bold=True, color=C_WHITE)
    _add_rect(s1, 9.56, 0.96, 2.95, 0.04, C_WHITE)

    cover_stats = [
        ("600 Sampel", "Dataset Kaggle bersih & seimbang\n(300 Potable : 300 Not Potable)"),
        ("27 Rules Mamdani", "Kurva segitiga simetris (sum mu = 1)\nCentroid analitik eksak (diff 0.0000)"),
        ("97.50% Akurasi", "Model B (4D, K=11), unggul +4.17%\ndari baseline KNN 3D (93.33%)"),
        ("100% Match", "Implementasi Python/NumPy scratch\nidentik 100% terhadap scikit-learn"),
    ]
    cy = 1.18
    for val, desc in cover_stats:
        _add_text(s1, 9.56, cy, 2.95, 0.36, val, size=19, bold=True, color=C_WHITE, font=FONT_HEAD)
        _add_text(s1, 9.56, cy + 0.36, 2.95, 0.48, desc, size=9.4, color=RGBColor(0xF0, 0xFB, 0xF7), line_spacing=1.18)
        cy += 0.96

    _add_rect(s1, 9.52, 5.10, 3.00, 1.76, C_WHITE, border_rgb=C_BORDER, border_pt=0.6, rounded=True)
    _add_text(s1, 9.72, 5.22, 2.65, 0.26, "DELIVERABLES PROYEK", size=9.6, bold=True, color=C_PRIMARY)
    _add_text(
        s1,
        9.72,
        5.50,
        2.65,
        1.26,
        "●  Core Engine Scratch (Python)\n●  Streamlit GUI 6 Halaman\n●  5/5 Unit Test (pytest)\n●  Laporan & Analisis Lengkap\n●  Repo: Water-Quality-Decision",
        size=9.5,
        bold=True,
        color=C_INK,
        line_spacing=1.26,
    )

    # =========================================================================
    # SLIDE 02: PROFIL TIM KELOMPOK 1 & PEMBAGIAN TUGAS
    # =========================================================================
    s2 = _new_slide(prs)
    _add_chrome(
        s2,
        2,
        "Tim Pengembang",
        "Profil Anggota Kelompok 1 & Pembagian Tanggung Jawab",
        "Seluruh modul dikerjakan secara kolaboratif dan terdokumentasi sinkron antara kode program, GUI Streamlit, dan laporan.",
    )

    team_headers = ["No", "Nama Lengkap", "NIM", "Peran & Tanggung Jawab (GUI)", "Kontribusi Konkret & Artefak"]
    team_rows = [
        [
            "1",
            "Nathanael Adrian Wattimena",
            "2408561013",
            "Ketua Kelompok, Analisis Masalah & Laporan (BAB I-II)",
            "Koordinasi tim, studi literatur standar WHO & Permenkes RI, penyusunan BAB I-II dan penyuntingan akhir laporan.",
        ],
        [
            "2",
            "I Wayan Arya Adi Guna",
            "2408561019",
            "Data Cleaning, Preprocessing & Eksplorasi Dataset",
            "Pembersihan dataset Kaggle 3.276 -> 600 sampel seimbang, 5 sampel referensi (S1-S5), EDA (src/prepare_dataset.py).",
        ],
        [
            "3",
            "Komang Dhika Artika Nurdi",
            "2408561055",
            "Implementasi Fuzzy Mamdani & Perhitungan Manual",
            "Kurva segitiga simetris, 27 rule base, inferensi MIN-MAX, Centroid analitik, verifikasi manual S4 & Q* (src/fuzzy_mamdani.py).",
        ],
        [
            "4",
            "Kadek Phatra Adisuta Timonuli",
            "2408561076",
            "Implementasi KNN, Integrasi & Evaluasi Model",
            "Min-Max & Z-Score scratch, KNN 4D, eksperimen Model A vs Model B lintas K, validasi 100% scikit-learn (src/knn_model.py).",
        ],
        [
            "5",
            "I Putu Maichail Ganio Wijaya",
            "2408561123",
            "Streamlit UI, Visualisasi Chart & Dokumentasi",
            "Antarmuka Streamlit 6 halaman modular (app.py, src/ui/), visualisasi Plotly, grafik Matplotlib 200 DPI, panduan sistem.",
        ],
    ]
    _add_table(
        s2,
        0.55,
        1.62,
        12.23,
        3.85,
        team_headers,
        team_rows,
        col_widths=[0.50, 2.55, 1.30, 3.25, 4.63],
        font_size=10,
        aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT],
    )

    # Bottom 3 summary context cards
    _add_card(s2, 0.55, 5.72, 3.92, 1.15, "Mata Kuliah & Institusi", accent_rgb=C_PRIMARY)
    _add_text(
        s2,
        0.85,
        6.10,
        3.48,
        0.65,
        "Teknologi Logika Fuzzy (TLF)\nProgram Studi Informatika, FMIPA\nUniversitas Udayana · Semester Genap 2026",
        size=10,
        color=C_BODY,
        line_spacing=1.22,
    )

    _add_card(s2, 4.70, 5.72, 3.92, 1.15, "Dosen Pengampu", accent_rgb=C_MINT)
    _add_text(
        s2,
        5.00,
        6.10,
        3.48,
        0.65,
        "I Made Widiartha, S.Si., M.Kom.\nDr. I Gusti Ngurah Anom Cahyadi Putra, S.T., M.Cs.",
        size=10,
        color=C_BODY,
        line_spacing=1.30,
    )

    _add_card(s2, 8.86, 5.72, 3.92, 1.15, "Repositori & Reproducibility", accent_rgb=C_PRIMARY)
    _add_text(
        s2,
        9.16,
        6.10,
        3.48,
        0.65,
        "GitHub: dhikrtika/Water-Quality-Decision\nUnit Tests: 5/5 Passed (pytest)\nApp Entry: streamlit run app.py",
        size=10,
        color=C_BODY,
        line_spacing=1.22,
    )

    # =========================================================================
    # SLIDE 03: LATAR BELAKANG, STANDAR AIR MINUM & RUMUSAN MASALAH
    # =========================================================================
    s3 = _new_slide(prs)
    _add_chrome(
        s3,
        3,
        "BAB I · Pendahuluan",
        "Latar Belakang, Standar Kualitas Air & Rumusan Masalah",
        "Mengapa penilaian kelayakan air minum membutuhkan pendekatan Fuzzy Mamdani yang dipadukan dengan klasifikasi KNN.",
    )

    # Left column: 3 Problem Cards
    _add_text(s3, 0.55, 1.56, 6.2, 0.30, "PERMASALAHAN UTAMA DI LAPANGAN", size=10.5, bold=True, color=C_PRIMARY)

    probs = [
        (
            "1. Kelemahan Batas Kaku (Crisp Threshold)",
            "Aturan konvensional memutus kelayakan secara biner (misal pH 6.49 langsung gagal, pH 6.50 langsung lolos). Sampel borderline di sekitar ambang baku mutu sering salah diklasifikasikan.",
            C_PRIMARY,
        ),
        (
            "2. Interaksi Non-Linear Antar Parameter Air",
            "Kualitas air minum tidak ditentukan satu variabel tunggal. Air ber-pH netral tetap berisiko jika Hardness atau Turbidity tinggi, sehingga perlu penalaran berbasis aturan (rule-based inference).",
            C_MINT,
        ),
        (
            "3. Kebutuhan Transparansi (White-Box) & Akurasi",
            "Model machine learning murni sulit menjelaskan alasan skor kualitas air secara linguistik. Sebaliknya, sistem fuzzy saja belum memanfaatkan pola kemiripan tetangga data aktual.",
            C_PRIMARY,
        ),
    ]
    py = 1.92
    for title_p, desc_p, acc in probs:
        _add_card(s3, 0.55, py, 6.15, 1.50, title_p, accent_rgb=acc)
        _add_text(s3, 0.86, py + 0.50, 5.65, 0.90, desc_p, size=10.5, color=C_BODY, line_spacing=1.25)
        py += 1.66

    # Right column: WHO / Permenkes Table + Research Objectives
    _add_text(s3, 6.98, 1.56, 5.8, 0.30, "ACUAN BAKU MUTU AIR MINUM (WHO & PERMENKES RI)", size=10.5, bold=True, color=C_MINT)

    std_headers = ["Parameter", "Satuan", "Baku Mutu Ideal", "Dampak Jika Melampaui"]
    std_rows = [
        ["pH (X1)", "Skala 0-14", "6.5 - 8.5 (Netral)", "Korosif (asam) atau rasa pahit/kerak (basa)."],
        ["Hardness (X2)", "mg/L CaCO3", "<= 500 (Lunak < 150)", "Endapan mineral & penurunan kualitas rasa air."],
        ["Turbidity (X3)", "NTU", "<= 5.0 (Jernih < 3.5)", "Indikasi partikel tersuspensi & risiko mikroba."],
    ]
    _add_table(
        s3,
        6.98,
        1.92,
        5.80,
        2.15,
        std_headers,
        std_rows,
        col_widths=[1.25, 1.05, 1.45, 2.05],
        font_size=9.5,
        header_bg=C_MINT,
        aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT],
    )

    _add_card(s3, 6.98, 4.30, 5.80, 2.46, "Tujuan & Pendekatan Solusi Kelompok 1", accent_rgb=C_PRIMARY, fill_rgb=C_WHITE)
    _add_bullets(
        s3,
        7.28,
        4.76,
        5.32,
        1.88,
        [
            ("Tahap 1 (Fuzzy Mamdani): ", "Menghasilkan skor kualitas air kontinu fuzzy_quality_score [0, 100] melalui 27 aturan lengkap & Centroid analitik."),
            ("Tahap 2 (Fuzzy-Enhanced KNN): ", "Menjadikan skor Mamdani sebagai fitur ke-4 untuk klasifikasi Potable vs Not Potable dengan evaluasi leakage-free."),
            ("Verifikasi & GUI: ", "Membuktikan kecocokan 0.0000 dengan perhitungan manual, 100% match scikit-learn, serta menyajikan GUI Streamlit 6 halaman."),
        ],
        size=10.2,
        space_after=7,
    )

    # =========================================================================
    # SLIDE 04: DATASET KAGGLE & PIPELINE PREPROCESSING
    # =========================================================================
    s4 = _new_slide(prs)
    _add_chrome(
        s4,
        4,
        "BAB III · Data & Preprocessing",
        "Dataset Kaggle Water Potability & Strategi Preprocessing",
        "Sumber: Kaggle adityakadiwal/water-potability (3.276 baris mentah, 10 kolom) dibersihkan menjadi 600 sampel seimbang.",
    )

    # Top 4-step pipeline boxes
    steps = [
        ("STEP 01", "Raw Kaggle CSV", "3.276 baris, 10 kolom.\nTerdapat missing values pada ph (491) & fitur lain.", C_PRIMARY),
        ("STEP 02", "Data Cleaning", "Drop missing values & validasi domain fisik:\npH [0,14], Hard [60,300], Turb [1,6].", C_MINT),
        ("STEP 03", "Balanced 600 Rows", "Sampling seimbang 300 Potable & 300 Not Potable\nuntuk mencegah bias kelas mayoritas.", C_PRIMARY),
        ("STEP 04", "Leakage-Free 80:20", "Stratified split: 480 Train (240:240) &\n120 Test (60:60). Scaler fit hanya pada Train.", C_MINT),
    ]
    sx = 0.55
    for idx, (tag, stitle, sdesc, acc) in enumerate(steps):
        _add_rect(s4, sx, 1.60, 2.86, 1.52, C_WHITE, border_rgb=C_BORDER, border_pt=0.85, rounded=True)
        _add_rect(s4, sx, 1.60, 2.86, 0.08, None, grad_angle=0.0)
        _add_text(s4, sx + 0.14, 1.74, 1.2, 0.22, tag, size=8.5, bold=True, color=C_PRIMARY)
        _add_text(s4, sx + 0.14, 1.96, 2.58, 0.28, stitle, size=12, bold=True, color=C_INK, font=FONT_HEAD)
        _add_text(s4, sx + 0.14, 2.28, 2.58, 0.76, sdesc, size=9.4, color=C_BODY, line_spacing=1.20)
        if idx < 3:
            _add_text(s4, sx + 2.87, 2.15, 0.25, 0.35, "→", size=16, bold=True, color=C_PRIMARY, align=PP_ALIGN.CENTER)
        sx += 3.12

    # Bottom Left: Descriptive Statistics Table
    _add_text(s4, 0.55, 3.35, 6.9, 0.28, "STATISTIK DESKRIPTIF DATASET BERSIH (N = 600 SAMPEL)", size=10.5, bold=True, color=C_PRIMARY)
    stat_headers = ["Fitur / Variabel", "Min", "Mean", "Std Dev", "Max", "Peran di Sistem"]
    stat_rows = [
        ["ph (X1)", "1.4318", "7.1165", "1.7151", "13.3499", "Input Mamdani & KNN"],
        ["Hardness (X2)", "73.4922", "195.2735", "34.0901", "286.5680", "Input Mamdani & KNN"],
        ["Turbidity (X3)", "1.8444", "3.9713", "0.7570", "5.9568", "Input Mamdani & KNN"],
        ["fuzzy_quality_score (Y)", "20.3883", "46.3661", "4.8023", "60.0580", "Output Mamdani -> Fitur 4"],
        ["Solids (ppm)", "1372.09", "22237.82", "8482.93", "55334.70", "Konteks Eksplorasi"],
        ["Chloramines (ppm)", "2.4586", "7.2088", "1.6174", "13.1270", "Konteks Eksplorasi"],
        ["Conductivity (uS/cm)", "201.62", "424.45", "79.67", "753.34", "Konteks Eksplorasi"],
    ]
    _add_table(
        s4,
        0.55,
        3.68,
        6.95,
        3.12,
        stat_headers,
        stat_rows,
        col_widths=[1.68, 0.78, 0.84, 0.78, 0.87, 2.00],
        font_size=9.0,
        aligns=[PP_ALIGN.LEFT, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT, PP_ALIGN.LEFT],
        row_bg_fn=lambda r, c, v: C_MINT_SOFT if r == 3 else (C_WHITE if r % 2 == 0 else C_ROW_ALT),
    )

    # Bottom Right: Rationale Card
    _add_card(s4, 8.05, 3.68, 4.73, 3.12, "Mengapa 3 Fitur Inti + 1 Fitur Fuzzy?", accent_rgb=C_MINT)
    _add_bullets(
        s4,
        8.35,
        4.14,
        4.25,
        2.55,
        [
            ("Menghindari Rule Explosion: ", "3 input x 3 himpunan menghasilkan tepat 27 aturan yang lengkap, logis, dan mudah diaudit manual."),
            ("Relevansi Fisik-Kimia: ", "pH, Hardness, dan Turbidity merupakan indikator utama paling sensitif pada standar WHO & Permenkes."),
            ("5 Sampel Manual (S1-S5): ", "Disiapkan pula manual_calc_sample.csv dengan rentang terstruktur (pH 3.5-10.5) untuk verifikasi analitik."),
        ],
        size=10.2,
        space_after=8,
    )

    # =========================================================================
    # SLIDE 05: ARSITEKTUR SISTEM (TWO-STAGE PIPELINE)
    # =========================================================================
    s5 = _new_slide(prs)
    _add_chrome(
        s5,
        5,
        "BAB III · Arsitektur Sistem",
        "Arsitektur Two-Stage Pipeline: Fuzzy Mamdani + KNN",
        "Integrasi berbasis feature engineering: skor kualitas dari mesin Fuzzy Mamdani memperkaya ruang fitur klasifikasi KNN.",
    )

    # Left: Architecture diagram image inside white card
    _add_rect(s5, 0.55, 1.58, 7.60, 5.26, C_WHITE, border_rgb=C_BORDER, border_pt=0.9, rounded=True)
    _add_image_fit(s5, FIG_DIR / "gambar_3_2_arsitektur_sistem.png", 0.68, 1.70, 7.34, 4.72)
    _add_text(
        s5,
        0.72,
        6.48,
        7.25,
        0.28,
        "Gambar 3.2: Diagram arsitektur pipeline sistem pendukung keputusan Fuzzy Mamdani dan KNN (Model A vs Model B).",
        size=9,
        italic=True,
        color=C_MUTED,
        align=PP_ALIGN.CENTER,
    )

    # Right: Detailed Stage Breakdown
    _add_card(s5, 8.38, 1.58, 4.40, 1.65, "Stage 01: Fuzzy Mamdani Engine", accent_rgb=C_PRIMARY)
    _add_text(
        s5,
        8.68,
        2.02,
        3.92,
        1.12,
        "Memetakan 3 input crisp [pH, Hardness, Turbidity] melalui fuzzifikasi segitiga simetris, evaluasi 27 rule (AND=MIN), agregasi MAX, dan Centroid analitik menjadi fitur kontinu fuzzy_quality_score dalam rentang [0, 100].",
        size=10,
        color=C_BODY,
        line_spacing=1.22,
    )

    _add_card(s5, 8.38, 3.38, 4.40, 1.72, "Stage 02: Model A (3D) vs Model B (4D)", accent_rgb=C_MINT)
    _add_text(
        s5,
        8.68,
        3.82,
        3.92,
        1.18,
        "Model A (Baseline): KNN dengan 3 fitur fisik [pH, Hardness, Turbidity].\nModel B (Fuzzy-Enhanced): KNN dengan 4 fitur [pH, Hardness, Turbidity, fuzzy_quality_score].\nNormalisasi Min-Max di-fit eksklusif pada 480 data latih (anti data leakage).",
        size=10,
        color=C_BODY,
        line_spacing=1.22,
    )

    _add_card(s5, 8.38, 5.25, 4.40, 1.59, "Implementasi 100% From-Scratch", accent_rgb=C_PRIMARY, fill_rgb=C_PRIMARY_SOFT)
    _add_text(
        s5,
        8.68,
        5.68,
        3.92,
        1.06,
        "Seluruh fungsi fuzzy (src/fuzzy_mamdani.py) dan KNN (src/knn_model.py) ditulis murni menggunakan Python & NumPy tanpa library fuzzy eksternal. Validasi silang terhadap scikit-learn mencapai 100% kecocokan.",
        size=10,
        color=C_PRIMARY_DARK,
        line_spacing=1.22,
    )

    # =========================================================================
    # SLIDE 06: DESAIN FUNGSI KEANGGOTAAN (SEGITIGA SIMETRIS)
    # =========================================================================
    s6 = _new_slide(prs)
    _add_chrome(
        s6,
        6,
        "BAB III · Fuzzy Mamdani",
        "Desain Fungsi Keanggotaan Segitiga Simetris (a, b, c)",
        "Setiap variabel dipartisi menjadi 3 himpunan fuzzy segitiga simetris dengan sifat sum(mu) = 1 di seluruh domain.",
    )

    # Left: Membership function curves image
    _add_rect(s6, 0.55, 1.58, 6.75, 5.26, C_WHITE, border_rgb=C_BORDER, border_pt=0.9, rounded=True)
    _add_image_fit(s6, FIG_DIR / "gambar_3_1_membership_functions.png", 0.66, 1.68, 6.53, 4.74)
    _add_text(
        s6,
        0.68,
        6.48,
        6.50,
        0.28,
        "Gambar 3.1: Kurva fungsi keanggotaan segitiga simetris untuk 3 input (X1, X2, X3) dan 1 output (Y).",
        size=9,
        italic=True,
        color=C_MUTED,
        align=PP_ALIGN.CENTER,
    )

    # Right: Parameter Table + Mathematical Properties
    _add_text(s6, 7.50, 1.56, 5.3, 0.28, "TABEL PARAMETER KURVA SEGITIGA (a, b, c)", size=10.5, bold=True, color=C_PRIMARY)
    mf_headers = ["Variabel & Domain", "Himpunan", "Parameter (a, b, c)"]
    mf_rows = [
        ["pH (X1) [0, 14]", "Acidic / Neutral / Alkaline", "(0,0,7)  |  (0,7,14)  |  (7,14,14)"],
        ["Hardness (X2) [60, 300]", "Soft / Moderate / Hard", "(60,60,180) | (60,180,300) | (180,300,300)"],
        ["Turbidity (X3) [1, 6]", "Clear / Moderate / Turbid", "(1,1,3.5)  |  (1,3.5,6)  |  (3.5,6,6)"],
        ["Quality Score (Y) [0, 100]", "Poor / Moderate / Good", "(0,0,50)  |  (0,50,100)  |  (50,100,100)"],
    ]
    _add_table(
        s6,
        7.50,
        1.88,
        5.28,
        2.35,
        mf_headers,
        mf_rows,
        col_widths=[1.62, 1.62, 2.04],
        font_size=8.8,
        aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER],
        row_bg_fn=lambda r, c, v: C_MINT_SOFT if r == 3 else (C_WHITE if r % 2 == 0 else C_ROW_ALT),
    )

    _add_card(s6, 7.50, 4.42, 5.28, 2.42, "Persamaan & Keunggulan Partisi Simetris", accent_rgb=C_MINT)
    _add_text(
        s6,
        7.80,
        4.84,
        4.80,
        0.52,
        "mu(x; a, b, c) = max(0, min((x - a)/(b - a), (c - x)/(c - b)))\nShoulder: kiri a=b (mu=1, x<=a) | kanan b=c (mu=1, x>=c)",
        size=9.3,
        bold=True,
        color=C_PRIMARY_DARK,
        line_spacing=1.22,
    )
    _add_bullets(
        s6,
        7.80,
        5.44,
        4.80,
        1.32,
        [
            ("Zero Dead-Zone: ", "Untuk setiap nilai x dalam domain, selalu berlaku sum(mu(x)) = 1.0000 sehingga minimal 1 aturan selalu aktif."),
            ("Transisi Halus: ", "Input tepat di titik potong (misal pH = 3.5) memiliki mu = 0.50 di dua himpunan berdampingan."),
        ],
        size=9.8,
        space_after=5,
    )

    # =========================================================================
    # SLIDE 07: BASIS ATURAN LENGKAP (27 RULE BASE MAMDANI)
    # =========================================================================
    s7 = _new_slide(prs)
    _add_chrome(
        s7,
        7,
        "BAB III · Basis Aturan",
        "Basis Aturan Lengkap Fuzzy Mamdani (27 Rules: R01 - R27)",
        "Kombinasi lengkap 3 x 3 x 3 himpunan input dengan operator AND = MIN, Implikasi MIN, dan Agregasi MAX.",
    )

    # Left & Middle: Split 27 rules into 2 clean side-by-side tables (R01-R14 and R15-R27)
    r_headers = ["ID", "pH (X1)", "Hardness", "Turbidity", "Output (Y)"]
    rules_left = [
        ["R01", "Acidic", "Soft", "Clear", "Moderate"],
        ["R02", "Acidic", "Soft", "Moderate", "Moderate"],
        ["R03", "Acidic", "Soft", "Turbid", "Poor"],
        ["R04", "Acidic", "Moderate", "Clear", "Moderate"],
        ["R05", "Acidic", "Moderate", "Moderate", "Poor"],
        ["R06", "Acidic", "Moderate", "Turbid", "Poor"],
        ["R07", "Acidic", "Hard", "Clear", "Poor"],
        ["R08", "Acidic", "Hard", "Moderate", "Poor"],
        ["R09", "Acidic", "Hard", "Turbid", "Poor"],
        ["R10", "Neutral", "Soft", "Clear", "Good"],
        ["R11", "Neutral", "Soft", "Moderate", "Good"],
        ["R12", "Neutral", "Soft", "Turbid", "Moderate"],
        ["R13", "Neutral", "Moderate", "Clear", "Good"],
        ["R14", "Neutral", "Moderate", "Moderate", "Moderate"],
    ]
    rules_right = [
        ["R15", "Neutral", "Moderate", "Turbid", "Poor"],
        ["R16", "Neutral", "Hard", "Clear", "Moderate"],
        ["R17", "Neutral", "Hard", "Moderate", "Poor"],
        ["R18", "Neutral", "Hard", "Turbid", "Poor"],
        ["R19", "Alkaline", "Soft", "Clear", "Moderate"],
        ["R20", "Alkaline", "Soft", "Moderate", "Moderate"],
        ["R21", "Alkaline", "Soft", "Turbid", "Poor"],
        ["R22", "Alkaline", "Moderate", "Clear", "Moderate"],
        ["R23", "Alkaline", "Moderate", "Moderate", "Poor"],
        ["R24", "Alkaline", "Moderate", "Turbid", "Poor"],
        ["R25", "Alkaline", "Hard", "Clear", "Poor"],
        ["R26", "Alkaline", "Hard", "Moderate", "Poor"],
        ["R27", "Alkaline", "Hard", "Turbid", "Poor"],
        ["Σ 27", "3 x 3 x 3", "27 Rules", "Complete", "3G · 9M · 15P"],
    ]

    def rule_bg(r, c, val):
        if val == "Good":
            return C_MINT_SOFT
        if val == "Moderate" and c == 4:
            return C_PRIMARY_SOFT
        if val == "Poor":
            return C_CORAL_SOFT
        if val == "Σ 27" or val == "3G · 9M · 15P":
            return C_PRIMARY_SOFT
        return C_WHITE if r % 2 == 0 else C_ROW_ALT

    _add_table(
        s7,
        0.55,
        1.58,
        3.45,
        5.25,
        r_headers,
        rules_left,
        [0.46, 0.71, 0.76, 0.74, 0.78],
        font_size=8.0,
        row_bg_fn=rule_bg,
        margin_lr=0.02,
    )
    _add_table(
        s7,
        4.52,
        1.58,
        3.45,
        5.25,
        r_headers,
        rules_right,
        [0.46, 0.71, 0.76, 0.74, 0.78],
        font_size=8.0,
        row_bg_fn=rule_bg,
        margin_lr=0.02,
    )

    # Right column: Rule Distribution + Inference Formulas
    _add_card(s7, 8.55, 1.58, 4.23, 2.38, "Distribusi 27 Konsekuen", accent_rgb=C_MINT)
    _add_pill(s7, 8.83, 2.06, 3.68, 0.42, "GOOD : 3 Rules (R10, R11, R13)", C_MINT_SOFT, RGBColor(0x0F, 0x6A, 0x49), font_size=9.6)
    _add_pill(s7, 8.83, 2.60, 3.68, 0.42, "MODERATE : 9 Rules (Borderline)", C_PRIMARY_SOFT, C_PRIMARY_DARK, font_size=9.6)
    _add_pill(s7, 8.83, 3.14, 3.68, 0.42, "POOR : 15 Rules (Risiko Tinggi)", C_CORAL_SOFT, C_CORAL, font_size=9.6)
    _add_text(s7, 8.83, 3.62, 3.68, 0.28, "Konservatif sesuai prinsip keamanan air minum.", size=9.0, italic=True, color=C_MUTED)

    _add_card(s7, 8.55, 4.14, 4.23, 2.69, "Mekanisme Inferensi Mamdani", accent_rgb=C_PRIMARY)
    _add_bullets(
        s7,
        8.83,
        4.58,
        3.75,
        2.16,
        [
            ("Firing Strength (AND=MIN): ", "alpha_k = min(mu_pH, mu_Hardness, mu_Turbidity) untuk k = 1..27."),
            ("Implikasi (Clipping MIN): ", "Memotong kurva output pada tinggi alpha_k."),
            ("Agregasi (Union MAX): ", "mu_agg(z) = max(min(alpha_k, mu_out_k(z))) menghasilkan amplop komposisi akhir."),
            ("Logika Domain: ", "Status Good hanya muncul saat pH Neutral serta tidak ada kondisi Hard atau Turbid."),
        ],
        size=9.6,
        space_after=5,
    )

    # =========================================================================
    # SLIDE 08: FLOWCHART ALGORITMA & DEFUZZIFIKASI CENTROID ANALITIK
    # =========================================================================
    s8 = _new_slide(prs)
    _add_chrome(
        s8,
        8,
        "BAB III · Algoritma & Matematika",
        "Flowchart Komputasi End-to-End & Centroid Analitik",
        "Mengapa sistem memakai integrasi Centroid analitik eksak dibandingkan aproksimasi grid diskrit.",
    )

    # Left: Flowchart diagram
    _add_rect(s8, 0.55, 1.58, 6.75, 5.26, C_WHITE, border_rgb=C_BORDER, border_pt=0.9, rounded=True)
    _add_image_fit(s8, FIG_DIR / "gambar_3_3_flowchart_algoritma.png", 0.66, 1.68, 6.53, 4.74)
    _add_text(
        s8,
        0.68,
        6.48,
        6.50,
        0.28,
        "Gambar 3.3: Flowchart komputasi end-to-end dari preprocessing, Mamdani Centroid, hingga evaluasi KNN.",
        size=9,
        italic=True,
        color=C_MUTED,
        align=PP_ALIGN.CENTER,
    )

    # Right: Mathematical formulas cards
    _add_card(s8, 7.52, 1.58, 5.26, 2.55, "1. Defuzzifikasi Centroid Analitik (Piecewise Exact)", accent_rgb=C_PRIMARY)
    _add_text(
        s8,
        7.82,
        2.00,
        4.78,
        0.72,
        "z* = Integral(0..100) [ z * mu_agg(z) dz ] / Integral(0..100) [ mu_agg(z) dz ]\n    = Sum( M_i ) / Sum( A_i )   untuk setiap segmen linear mu(z) = m*z + c",
        size=9.8,
        bold=True,
        color=C_PRIMARY_DARK,
        line_spacing=1.25,
    )
    _add_bullets(
        s8,
        7.82,
        2.78,
        4.78,
        1.25,
        [
            ("Luas Segmen: ", "A_i = [0.5*m*z^2 + c*z] dari z_a ke z_b."),
            ("Momen Segmen: ", "M_i = [(m/3)*z^3 + 0.5*c*z^2] dari z_a ke z_b."),
            ("Akurasi Eksak: ", "0.0000 selisih terhadap hitungan manual, bebas error diskritisasi (grid 1001 titik berselisih ~0.0103)."),
        ],
        size=9.7,
        space_after=4,
    )

    _add_card(s8, 7.52, 4.30, 5.26, 2.54, "2. Normalisasi Min-Max & KNN 4-Dimensi", accent_rgb=C_MINT)
    _add_text(
        s8,
        7.82,
        4.72,
        4.78,
        0.78,
        "Min-Max (Fit on Train):   x'_ij = (x_ij - min_train_j) / (max_train_j - min_train_j)\nEuclidean Distance 4D:   d(x_q, x_i) = sqrt( Sum_{j=1..4} (x'_qj - x'_ij)^2 )",
        size=9.8,
        bold=True,
        color=RGBColor(0x0F, 0x6A, 0x49),
        line_spacing=1.28,
    )
    _add_bullets(
        s8,
        7.82,
        5.56,
        4.78,
        1.20,
        [
            ("Ruang Fitur Model B: ", "[pH', Hardness', Turbidity', fuzzy_quality_score'] ternormalisasi pada [0, 1]."),
            ("Majority Voting & Tie-Breaker: ", "Kelas dipilih berdasarkan suara terbanyak K tetangga terdekat (tie diputus jarak rata-rata terdekat)."),
        ],
        size=9.7,
        space_after=4,
    )

    # =========================================================================
    # SLIDE 09: VERIFIKASI PERHITUNGAN MANUAL KASUS 1 (SAMPEL S4)
    # =========================================================================
    s9 = _new_slide(prs)
    _add_chrome(
        s9,
        9,
        "BAB III & IV · Verifikasi Manual",
        "Verifikasi Perhitungan Manual Kasus 1: Sampel Referensi S4",
        "Sampel S4 (WQP-M04): pH = 7.00, Hardness = 120.0 mg/L, Turbidity = 2.25 NTU (Kelas Aktual: Potable).",
    )

    # Top-Left: Step 1 Fuzzification
    _add_card(s9, 0.55, 1.58, 6.05, 1.98, "Tahap 1: Fuzzifikasi Input S4", accent_rgb=C_PRIMARY)
    fuz_headers = ["Variabel", "Input x", "Derajat Keanggotaan (mu)"]
    fuz_rows = [
        ["pH (X1)", "7.00", "Acidic = 0.0000  |  Neutral = 1.0000  |  Alkaline = 0.0000"],
        ["Hardness (X2)", "120.0", "Soft = 0.5000  |  Moderate = 0.5000  |  Hard = 0.0000"],
        ["Turbidity (X3)", "2.25", "Clear = 0.5000  |  Moderate = 0.5000  |  Turbid = 0.0000"],
    ]
    _add_table(
        s9,
        0.80,
        2.04,
        5.20,
        1.36,
        fuz_headers,
        fuz_rows,
        col_widths=[1.05, 0.65, 3.50],
        font_size=8.6,
        aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT],
    )

    # Bottom-Left: Step 2 Active Rules & Aggregation
    _add_card(s9, 0.55, 3.74, 6.05, 3.10, "Tahap 2: 4 Rule Aktif (MIN) & Agregasi (MAX)", accent_rgb=C_MINT)
    s4_r_headers = ["Rule", "Anteseden (X1, X2, X3)", "mu1, mu2, mu3", "alpha", "Konsekuen"]
    s4_r_rows = [
        ["R10", "(Neutral, Soft, Clear)", "1.0, 0.5, 0.5", "0.5000", "Good"],
        ["R11", "(Neutral, Soft, Moderate)", "1.0, 0.5, 0.5", "0.5000", "Good"],
        ["R13", "(Neutral, Moderate, Clear)", "1.0, 0.5, 0.5", "0.5000", "Good"],
        ["R14", "(Neutral, Moderate, Mod.)", "1.0, 0.5, 0.5", "0.5000", "Moderate"],
    ]
    _add_table(
        s9,
        0.80,
        4.20,
        5.20,
        1.82,
        s4_r_headers,
        s4_r_rows,
        col_widths=[0.50, 1.80, 1.04, 0.76, 1.10],
        font_size=8.6,
        header_bg=C_MINT,
        aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER],
        row_bg_fn=lambda r, c, v: C_MINT_SOFT if v == "Good" else (C_PRIMARY_SOFT if v == "Moderate" else (C_WHITE if r % 2 == 0 else C_ROW_ALT)),
    )
    _add_text(
        s9,
        0.80,
        6.14,
        5.65,
        0.58,
        "Agregasi MAX: Poor = 0.0000 | Moderate = 0.5000 | Good = 0.5000\nKurva terpotong mendatar di tinggi 0.50 mulai z = 25 hingga z = 100.",
        size=9.4,
        bold=True,
        color=C_INK,
        line_spacing=1.22,
    )

    # Right: Step 3 Piecewise Integral Table + Big Verification Card
    _add_card(s9, 6.82, 1.58, 5.96, 3.35, "Tahap 3: Integrasi Luas (A) & Momen (M) Analitik", accent_rgb=C_PRIMARY)
    int_headers = ["Segmen", "Interval z", "Persamaan mu(z)", "Luas A_i", "Momen M_i"]
    int_rows = [
        ["Segmen 1", "[0.00, 25.00]", "mu(z) = 0.0200 z", "6.2500", "104.1667"],
        ["Segmen 2", "[25.00, 100.00]", "mu(z) = 0.5000", "37.5000", "2343.7500"],
        ["TOTAL", "[0.00, 100.00]", "Sum A_i & Sum M_i", "43.7500", "2447.9167"],
    ]
    _add_table(
        s9,
        7.08,
        2.06,
        5.15,
        1.65,
        int_headers,
        int_rows,
        col_widths=[0.88, 1.10, 1.32, 0.85, 1.00],
        font_size=9.0,
        aligns=[PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT],
        row_bg_fn=lambda r, c, v: C_PRIMARY_SOFT if r == 2 else (C_WHITE if r % 2 == 0 else C_ROW_ALT),
    )
    _add_text(
        s9,
        7.08,
        3.86,
        5.52,
        0.95,
        "Perhitungan Eksak:\nA1 = 0.5 * 25 * 0.50 = 6.2500    |    M1 = (0.02 / 3) * 25^3 = 104.1667\nA2 = (100 - 25) * 0.50 = 37.5000  |  M2 = 0.25 * (100^2 - 25^2) = 2343.7500",
        size=9.5,
        color=C_BODY,
        line_spacing=1.28,
    )

    # Verification Hero Banner on Bottom Right (Canva #4735F3 -> #61DD99 gradient)
    _add_rect(s9, 6.82, 5.12, 5.96, 1.72, None, rounded=True, grad_angle=0.0)
    _add_text(s9, 7.12, 5.28, 5.4, 0.26, "HASIL AKHIR DEFUZZIFIKASI & VERIFIKASI SISTEM", size=9.5, bold=True, color=C_WHITE)
    _add_text(s9, 7.12, 5.58, 5.4, 0.56, "z* (S4) = 2447.9167 / 43.7500 = 55.9524", size=20, bold=True, color=C_WHITE, font=FONT_HEAD)
    _add_text(
        s9,
        7.12,
        6.20,
        5.4,
        0.48,
        "Output Program = 55.9524  |  Selisih = 0.0000 (100% VALID)",
        size=10.5,
        bold=True,
        color=RGBColor(0xF0, 0xFB, 0xF7),
    )

    # =========================================================================
    # SLIDE 10: VERIFIKASI END-TO-END KASUS 2 (KASUS UJI BARU Q*)
    # =========================================================================
    s10 = _new_slide(prs)
    _add_chrome(
        s10,
        10,
        "BAB III & IV · End-to-End Trace",
        "Verifikasi End-to-End Kasus 2: Kasus Uji Baru Q*",
        "Trace lengkap Fuzzy Mamdani -> Min-Max 4D -> Euclidean Distance -> KNN Majority Voting (K = 3) pada Q* = (5.25, 150.0, 2.25).",
    )

    # Left: Fuzzy Mamdani on Q* (3 segments -> 54.1667)
    _add_card(s10, 0.55, 1.58, 5.65, 5.26, "Tahap 1: Fuzzy Mamdani pada Q* (5.25, 150.0, 2.25)", accent_rgb=C_PRIMARY)
    _add_bullets(
        s10,
        0.84,
        2.02,
        5.18,
        1.42,
        [
            ("Fuzzifikasi: ", "pH (Acidic=0.25, Neutral=0.75); Hardness (Soft=0.25, Moderate=0.75); Turbidity (Clear=0.50, Moderate=0.50)."),
            ("8 Rule Aktif: ", "R01, R02, R04, R05 (alpha=0.25); R10, R11 (alpha=0.25); R13, R14 (alpha=0.50)."),
            ("Agregasi MAX: ", "Poor = 0.2500  |  Moderate = 0.5000  |  Good = 0.5000."),
        ],
        size=9.7,
        space_after=5,
    )

    q_seg_headers = ["Segmen", "Interval z", "mu(z)", "A_i", "M_i"]
    q_seg_rows = [
        ["Seg 1", "[0.0, 12.5]", "0.2500", "3.1250", "19.5313"],
        ["Seg 2", "[12.5, 25.0]", "0.0200 z", "4.6875", "91.1458"],
        ["Seg 3", "[25.0, 100.0]", "0.5000", "37.5000", "2343.7500"],
        ["TOTAL", "[0.0, 100.0]", "Analitik", "45.3125", "2454.4271"],
    ]
    _add_table(
        s10,
        0.80,
        3.56,
        4.85,
        1.92,
        q_seg_headers,
        q_seg_rows,
        col_widths=[0.70, 1.08, 0.98, 0.92, 1.17],
        font_size=8.8,
        aligns=[PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT],
        row_bg_fn=lambda r, c, v: C_PRIMARY_SOFT if r == 3 else (C_WHITE if r % 2 == 0 else C_ROW_ALT),
    )

    _add_rect(s10, 0.80, 5.66, 5.20, 0.96, C_MINT_SOFT, border_rgb=C_MINT, border_pt=1.0, rounded=True)
    _add_text(s10, 0.98, 5.76, 4.88, 0.36, "z* (Q*) = 2454.4271 / 45.3125 = 54.1667", size=14.5, bold=True, color=RGBColor(0x0F, 0x6A, 0x49))
    _add_text(s10, 0.98, 6.16, 4.88, 0.34, "Vektor 4D Q* = [5.25, 150.0, 2.25, 54.1667] -> Scaled [0.250, 0.400, 0.200, 0.491]", size=9.0, bold=True, color=C_INK)

    # Right: KNN 4D Distance Table + Voting Result
    _add_card(s10, 6.42, 1.58, 6.36, 5.26, "Tahap 2: Normalisasi Min-Max 4D & Jarak Euclidean KNN", accent_rgb=C_MINT)
    _add_text(
        s10,
        6.68,
        2.02,
        5.90,
        0.46,
        "Rentang Min-Max dari 5 sampel referensi (S1-S5): pH [3.5, 10.5], Hardness [90, 240], Turbidity [1.625, 4.75], Fuzzy Score [44.0476, 64.6739].",
        size=9.5,
        color=C_BODY,
        line_spacing=1.20,
    )

    knn_headers = ["No", "Kode", "Vektor Scaled [X1', X2', X3', Y']", "Jarak d", "Kelas", "K=3?"]
    knn_rows = [
        ["1", "S4", "[0.500, 0.200, 0.200, 0.577]", "0.3317", "Potable", "YA"],
        ["2", "S3", "[0.500, 0.600, 0.600, 0.289]", "0.5507", "Not Potable", "YA"],
        ["3", "S5", "[0.500, 0.000, 0.000, 1.000]", "0.7225", "Potable", "YA"],
        ["4", "S1", "[0.000, 1.000, 1.000, 0.000]", "1.1416", "Not Potable", "-"],
        ["5", "S2", "[1.000, 1.000, 1.000, 0.000]", "1.3428", "Not Potable", "-"],
    ]
    _add_table(
        s10,
        6.68,
        2.58,
        5.55,
        2.45,
        knn_headers,
        knn_rows,
        col_widths=[0.44, 0.54, 2.20, 0.80, 0.99, 0.58],
        font_size=8.6,
        header_bg=C_MINT,
        aligns=[PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.RIGHT, PP_ALIGN.CENTER, PP_ALIGN.CENTER],
        row_bg_fn=lambda r, c, v: C_MINT_SOFT if (r in (0, 2) and c in (4, 5)) else (C_CORAL_SOFT if (r == 1 and c == 4) else (C_WHITE if r % 2 == 0 else C_ROW_ALT)),
    )

    _add_rect(s10, 6.72, 5.26, 5.88, 1.36, None, rounded=True, grad_angle=0.0)
    _add_text(s10, 6.96, 5.38, 5.4, 0.26, "KEPUTUSAN MAJORITY VOTING (K = 3 TETANGGA TERDEKAT)", size=9.2, bold=True, color=C_WHITE)
    _add_text(s10, 6.96, 5.66, 5.4, 0.44, "Prediksi Q* = POTABLE  (Vote: 2 Potable vs 1 Not Potable)", size=14.2, bold=True, color=C_WHITE, font=FONT_HEAD)
    _add_text(
        s10,
        6.96,
        6.16,
        5.4,
        0.38,
        "Tetangga terpilih: S4 (Potable, 0.3317), S3 (Not Potable, 0.5507), S5 (Potable, 0.7225). 100% cocok dengan GUI White-Box.",
        size=9.1,
        color=RGBColor(0xF0, 0xFB, 0xF7),
    )

    # =========================================================================
    # SLIDE 11: EVALUASI MODEL A VS MODEL B LINTAS NILAI K
    # =========================================================================
    s11 = _new_slide(prs)
    _add_chrome(
        s11,
        11,
        "BAB IV · Evaluasi Eksperimen",
        "Perbandingan Performa Model A (3D) vs Model B (4D) Lintas K",
        "Evaluasi leakage-free pada 120 data uji (480 train / 120 test, stratified 80:20, Min-Max fit on train) untuk K = 3, 5, 7, 9, 11.",
    )

    # Left: Chart gambar_4_1
    _add_rect(s11, 0.55, 1.58, 6.30, 5.26, C_WHITE, border_rgb=C_BORDER, border_pt=0.9, rounded=True)
    _add_image_fit(s11, FIG_DIR / "gambar_4_1_perbandingan_model_k.png", 0.66, 1.72, 6.08, 4.65)
    _add_text(
        s11,
        0.68,
        6.46,
        6.05,
        0.30,
        "Gambar 4.1: Sensitivitas akurasi & Macro-F1 Model A (Baseline 3D) vs Model B (Fuzzy-Enhanced 4D).",
        size=9,
        italic=True,
        color=C_MUTED,
        align=PP_ALIGN.CENTER,
    )

    # Right: Full Evaluation Table + Key Insight
    _add_text(s11, 7.05, 1.56, 5.7, 0.28, "TABEL HASIL EVALUASI MODEL A VS MODEL B (N_TEST = 120)", size=10.2, bold=True, color=C_PRIMARY)
    ev_headers = ["K", "Acc A", "Acc B", "Gain (B-A)", "Macro-F1 B", "Sklearn"]
    ev_rows = [
        ["K = 3", "92.50%", "95.83%", "+3.33%", "95.83%", "100%"],
        ["K = 5", "92.50%", "95.00%", "+2.50%", "95.00%", "100%"],
        ["K = 7", "93.33%", "95.83%", "+2.50%", "95.83%", "100%"],
        ["K = 9", "91.67%", "95.83%", "+4.17%", "95.83%", "100%"],
        ["K = 11", "93.33%", "97.50%", "+4.17%", "97.50%", "100%"],
    ]
    _add_table(
        s11,
        7.05,
        1.88,
        5.73,
        2.55,
        ev_headers,
        ev_rows,
        col_widths=[0.78, 0.92, 0.96, 1.05, 1.12, 0.90],
        font_size=9.5,
        aligns=[PP_ALIGN.CENTER] * 6,
        row_bg_fn=lambda r, c, v: C_MINT_SOFT if (r == 4 or c == 3) else (C_WHITE if r % 2 == 0 else C_ROW_ALT),
        highlight_col=2,
    )

    _add_card(s11, 7.05, 4.62, 5.73, 2.22, "Analisis Dampak Fitur fuzzy_quality_score", accent_rgb=C_MINT)
    _add_bullets(
        s11,
        7.35,
        5.04,
        5.26,
        1.70,
        [
            ("Keunggulan Konsisten di Semua K: ", "Model B selalu mengungguli Model A sebesar +2.50% hingga +4.17% tanpa satu pun nilai K yang mengalami penurunan."),
            ("Puncak Performa di K = 11: ", "Akurasi mencapai 97.50% dan Macro-F1 97.50% (hanya 3 kesalahan dari 120 sampel uji)."),
            ("Validasi Sklearn 100%: ", "Prediksi implementasi KNN from-scratch identik 100% dengan KNeighborsClassifier milik scikit-learn."),
        ],
        size=9.8,
        space_after=6,
    )

    # =========================================================================
    # SLIDE 12: ANALISIS CONFUSION MATRIX (K = 11) & ERROR ANALYSIS
    # =========================================================================
    s12 = _new_slide(prs)
    _add_chrome(
        s12,
        12,
        "BAB IV · Analisis Kesalahan",
        "Confusion Matrix Optimal (K = 11) & Analisis Metrik Per Kelas",
        "Penambahan fitur fuzzy_quality_score memangkas kesalahan prediksi dari 8 sampel (Model A) menjadi hanya 3 sampel (Model B).",
    )

    # Left: Confusion Matrix figure (K = 11 optimal)
    _add_rect(s12, 0.55, 1.58, 6.45, 5.26, C_WHITE, border_rgb=C_BORDER, border_pt=0.9, rounded=True)
    _add_image_fit(s12, FIG_DIR / "slide_confusion_matrix_k11.png", 0.66, 1.72, 6.23, 4.65)
    _add_text(
        s12,
        0.68,
        6.46,
        6.20,
        0.30,
        "Confusion Matrix Optimal K = 11: Model A (kiri, 93.33%) vs Model B (kanan, 97.50%) pada N = 120 data uji.",
        size=9,
        italic=True,
        color=C_MUTED,
        align=PP_ALIGN.CENTER,
    )

    # Right: Per-class metrics table + Error reduction cards
    _add_text(s12, 7.20, 1.56, 5.58, 0.28, "METRIK PER KELAS MODEL B (OPTIMAL K = 11)", size=10.2, bold=True, color=C_PRIMARY)
    pc_headers = ["Kelas", "Precision", "Recall", "F1-Score", "Support"]
    pc_rows = [
        ["Not Potable (0)", "98.31%", "96.67%", "97.48%", "60"],
        ["Potable (1)", "96.72%", "98.33%", "97.52%", "60"],
        ["Macro / Weighted", "97.51%", "97.50%", "97.50%", "120"],
    ]
    _add_table(
        s12,
        7.20,
        1.88,
        5.58,
        1.78,
        pc_headers,
        pc_rows,
        col_widths=[1.58, 1.00, 1.00, 1.00, 1.00],
        font_size=9.5,
        header_bg=C_MINT,
        aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER],
        row_bg_fn=lambda r, c, v: C_PRIMARY_SOFT if r == 2 else (C_WHITE if r % 2 == 0 else C_ROW_ALT),
    )

    # 2 side-by-side KPI comparison tiles
    _add_kpi_tile(s12, 7.20, 3.84, 2.68, 1.18, "Error Model A (3D)", "8 / 120", "2 FP + 6 FN (Recall Potable 90%)", accent=C_CORAL)
    _add_kpi_tile(s12, 10.10, 3.84, 2.68, 1.18, "Error Model B (4D)", "3 / 120", "2 FP + 1 FN (Reduksi 62.5%!)", accent=C_MINT)

    _add_card(s12, 7.20, 5.18, 5.58, 1.66, "Temuan Kunci Analisis Kesalahan", accent_rgb=C_PRIMARY)
    _add_bullets(
        s12,
        7.50,
        5.60,
        5.12,
        1.16,
        [
            ("Lonjakan Recall Potable (+8.33%): ", "False Negative turun drastis dari 6 sampel (Model A) menjadi hanya 1 sampel pada Model B."),
            ("Keamanan Tetap Terjaga: ", "False Positive tetap sangat rendah (2 dari 60 sampel Not Potable) dengan Precision Not Potable 98.31%."),
        ],
        size=9.8,
        space_after=5,
    )

    # =========================================================================
    # SLIDE 13: IMPLEMENTASI GUI STREAMLIT (HALAMAN 01 - 03)
    # =========================================================================
    s13 = _new_slide(prs)
    _add_chrome(
        s13,
        13,
        "BAB IV · Demo GUI (1/2)",
        "Antarmuka Aplikasi GUI Streamlit: Halaman 01 s.d. 03",
        "Aplikasi web interaktif modular dibangun dengan Streamlit & Plotly (app.py + src/ui/) untuk simulasi dan audit white-box.",
    )

    gui_1_3 = [
        (
            "01 · Dashboard",
            FIG_DIR / "gui_01_dashboard.png",
            "Ringkasan KPI utama (600 sampel, Avg Score 46.37, Akurasi Model B 97.50%, 100% Sklearn Match), alur Two-Stage Pipeline, distribusi kelas seimbang, dan profil Kelompok 1.",
            C_PRIMARY,
        ),
        (
            "02 · Input & Dataset",
            FIG_DIR / "gui_02_input_dataset.png",
            "Single-Sample Simulator interaktif dengan preset S1-S5 & Q*, slider parameter pH/Hardness/Turbidity, pemilihan mode KNN (5 manual vs 480 train), serta fitur Upload Custom CSV.",
            C_MINT,
        ),
        (
            "03 · Step-by-Step Process",
            FIG_DIR / "gui_03_step_by_step.png",
            "Trace white-box 4 desimal (0.0000): kurva Membership Function dengan garis input aktif, tabel 27 rule & firing strength, amplop agregasi MAX, Centroid analitik, dan jarak KNN.",
            C_PRIMARY,
        ),
    ]
    gx = 0.55
    for title_g, img_g, desc_g, acc in gui_1_3:
        _add_rect(s13, gx, 1.58, 3.92, 5.26, C_WHITE, border_rgb=C_BORDER, border_pt=0.9, rounded=True)
        _add_rect(s13, gx, 1.58, 3.92, 0.08, None, grad_angle=0.0)
        _add_pill(s13, gx + 0.16, 1.76, 2.55, 0.30, title_g, None, C_WHITE, font_size=9.2, gradient=True)
        _add_rect(s13, gx + 0.14, 2.18, 3.64, 2.42, RGBColor(0x0B, 0x10, 0x1C), border_rgb=C_BORDER, border_pt=0.5)
        _add_image_fit(s13, img_g, gx + 0.16, 2.20, 3.60, 2.38)
        _add_text(s13, gx + 0.18, 4.74, 3.56, 1.96, desc_g, size=10.1, color=C_BODY, line_spacing=1.26)
        gx += 4.15

    # =========================================================================
    # SLIDE 14: IMPLEMENTASI GUI STREAMLIT (HALAMAN 04 - 06)
    # =========================================================================
    s14 = _new_slide(prs)
    _add_chrome(
        s14,
        14,
        "BAB IV · Demo GUI (2/2)",
        "Antarmuka Aplikasi GUI Streamlit: Halaman 04 s.d. 06",
        "Mendukung klasifikasi batch seluruh dataset, laboratorium evaluasi Model A vs Model B, dan dokumentasi matematis terpadu.",
    )

    gui_4_6 = [
        (
            "04 · Classification Results",
            FIG_DIR / "gui_04_results.png",
            "Ranking kualitas air seluruh 600 sampel berdasarkan fuzzy_quality_score, filter kelas Potable / Not Potable, filter skor minimum, grafik sebaran, serta ekspor hasil ke CSV.",
            C_MINT,
        ),
        (
            "05 · Model Evaluation",
            FIG_DIR / "gui_05_evaluation.png",
            "Komparasi interaktif Model A vs Model B lintas K = 3, 5, 7, 9, 11, opsi strategi split & scaling (Min-Max / Z-Score), Confusion Matrix, metrik per kelas, dan verifikasi scikit-learn.",
            C_PRIMARY,
        ),
        (
            "06 · Docs & Guide",
            FIG_DIR / "gui_06_docs.png",
            "Referensi rumus lengkap Fuzzy Mamdani & KNN 4D yang dirender rapi, tabel lengkap 27 rule base (R01-R27), serta panduan singkat penggunaan tiap halaman aplikasi.",
            C_MINT,
        ),
    ]
    gx = 0.55
    for title_g, img_g, desc_g, acc in gui_4_6:
        _add_rect(s14, gx, 1.58, 3.92, 5.26, C_WHITE, border_rgb=C_BORDER, border_pt=0.9, rounded=True)
        _add_rect(s14, gx, 1.58, 3.92, 0.08, None, grad_angle=0.0)
        _add_pill(s14, gx + 0.16, 1.76, 2.65, 0.30, title_g, None, C_WHITE, font_size=9.2, gradient=True)
        _add_rect(s14, gx + 0.14, 2.18, 3.64, 2.42, RGBColor(0x0B, 0x10, 0x1C), border_rgb=C_BORDER, border_pt=0.5)
        _add_image_fit(s14, img_g, gx + 0.16, 2.20, 3.60, 2.38)
        _add_text(s14, gx + 0.18, 4.74, 3.56, 1.96, desc_g, size=10.1, color=C_BODY, line_spacing=1.26)
        gx += 4.15

    # =========================================================================
    # SLIDE 15: KESIMPULAN, SARAN & PENUTUP (Q&A)
    # =========================================================================
    s15 = _new_slide(prs)
    _add_chrome(
        s15,
        15,
        "BAB V · Penutup",
        "Kesimpulan, Saran Pengembangan & Sesi Tanya Jawab",
        "Ringkasan pembuktian kuantitatif, validasi sistem, serta arah pengembangan lanjutan.",
    )

    # Top 4 KPI summary tiles
    _add_kpi_tile(s15, 0.55, 1.58, 2.90, 1.18, "Akurasi Terbaik (Model B)", "97.50%", "Pada K = 11 (Macro-F1: 97.50%)", accent=C_PRIMARY)
    _add_kpi_tile(s15, 3.66, 1.58, 2.90, 1.18, "Peningkatan vs Model A", "+4.17%", "Konsisten unggul +2.50% s.d. +4.17%", accent=C_MINT)
    _add_kpi_tile(s15, 6.77, 1.58, 2.90, 1.18, "Akurasi Hitungan Manual", "0.0000", "Diff eksak S4 (55.9524) & Q* (54.1667)", accent=C_PRIMARY)
    _add_kpi_tile(s15, 9.88, 1.58, 2.90, 1.18, "Validasi & Pengujian", "100%", "Match scikit-learn · 5/5 Pytest Passed", accent=C_MINT)

    # Middle-Left: Kesimpulan
    _add_card(s15, 0.55, 2.96, 6.45, 3.88, "Kesimpulan Utama Penelitian", accent_rgb=C_PRIMARY)
    _add_bullets(
        s15,
        0.86,
        3.42,
        5.96,
        3.28,
        [
            ("Model Fuzzy Mamdani Valid & Transparan: ", "Kurva segitiga simetris (sum mu = 1), 27 aturan lengkap, dan Centroid analitik menghasilkan skor kualitas air kontinu yang cocok 100% (diff 0.0000) dengan perhitungan manual."),
            ("Fitur Fuzzy Meningkatkan Akurasi KNN: ", "Integrasi fuzzy_quality_score pada Model B (4D) meningkatkan akurasi di semua nilai K (3, 5, 7, 9, 11) dan memangkas error dari 8 menjadi 3 sampel di K = 11."),
            ("Bebas Data Leakage & Terverifikasi: ", "Normalisasi Min-Max di-fit khusus pada 480 data latih, dan seluruh implementasi from-scratch terverifikasi 100% identik terhadap scikit-learn."),
            ("GUI Interaktif Siap Demo: ", "Aplikasi Streamlit 6 halaman memudahkan simulasi manual, upload CSV, audit step-by-step white-box, dan evaluasi model secara real-time."),
        ],
        size=10.2,
        space_after=8,
    )

    # Middle-Right Top: Saran Pengembangan
    _add_card(s15, 7.22, 2.96, 5.56, 1.98, "Saran Pengembangan Lanjutan", accent_rgb=C_MINT)
    _add_bullets(
        s15,
        7.52,
        3.40,
        5.08,
        1.45,
        [
            ("Ekspansi Fitur & Optimasi Bobot: ", "Integrasi fitur tambahan (Solids, Chloramines, Conductivity) dengan pembobotan fitur (Weighted KNN) atau optimasi parameter kurva."),
            ("Integrasi Sensor IoT Real-Time: ", "Menghubungkan modul Mamdani + KNN dengan sensor pH & kekeruhan lapangan untuk pemantauan air minum berkelanjutan."),
        ],
        size=9.7,
        space_after=6,
    )

    # Middle-Right Bottom: Closing Q&A Banner (Canva #4735F3 -> #61DD99 gradient)
    _add_rect(s15, 7.22, 5.12, 5.56, 1.72, None, rounded=True, grad_angle=0.0)
    _add_text(s15, 7.50, 5.26, 5.05, 0.44, "TERIMA KASIH  ·  SESI TANYA JAWAB", size=16.5, bold=True, color=C_WHITE, font=FONT_HEAD)
    _add_text(
        s15,
        7.50,
        5.76,
        5.05,
        0.96,
        "Kelompok 1 · Program Studi Informatika · Universitas Udayana\nGitHub: github.com/dhikrtika/Water-Quality-Decision\nLive Demo Lokal:  streamlit run app.py  (http://localhost:8501)",
        size=9.8,
        color=RGBColor(0xF0, 0xFB, 0xF7),
        line_spacing=1.28,
    )

    OUT_PPTX.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT_PPTX))
    print(f"[SUCCESS] Generated 15-slide presentation: {OUT_PPTX} ({OUT_PPTX.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build_presentation()
