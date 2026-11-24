"""
Generator Presentasi Final Project Teknologi Logika Fuzzy (Kelompok 1)
Format: 20 Slide Widescreen 16:9 (.pptx) siap edit di Canva, PowerPoint, dan Google Slides.
- Struktur dibagi 5 bagian setara (1 pembatas bersih per bagian + slide materi) untuk 5 anggota tim.
- Palet warna 100% mengikuti aura & gradien asli Canva (#EEF2F3, #FFFFFF, #4735F3 -> #61DD99).
- Gaya bahasa presentasi natural & santai-rapi (tanpa narasi BAB, tanpa referensi WHO/Kemenkes).
- Tanpa stock image: seluruh visual menggunakan diagram asli, tabel native, dan screenshot GUI Streamlit.
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

# Palet Warna Exact Canva (Gradien Modern Biru Hijau)
C_BG = RGBColor(0xEE, 0xF2, 0xF3)            # #EEF2F3 - Canva Airy Canvas
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)         # #FFFFFF - Crisp Card Surface
C_BORDER = RGBColor(0xD2, 0xDF, 0xEC)        # #D2DFEC - Cool Ice-Blue Border
C_PRIMARY = RGBColor(0x47, 0x35, 0xF3)       # #4735F3 - Canva Electric Blue-Indigo (Stop 0)
C_BLUE_MID = RGBColor(0x4E, 0x7A, 0xE8)      # #4E7AE8 - Mid Gradient Sky-Cobalt
C_PRIMARY_DARK = RGBColor(0x31, 0x24, 0xB8)  # #3124B8 - Deep Cobalt text on soft tints
C_PRIMARY_SOFT = RGBColor(0xEC, 0xEE, 0xFF)  # #ECEEFF - Luminous Soft Indigo Tint
C_MINT = RGBColor(0x4E, 0x7A, 0xE8)          # Secondary header color harmonized with gradient
C_MINT_PURE = RGBColor(0x61, 0xDD, 0x99)     # #61DD99 - Exact Canva SVG Stop 1
C_MINT_TEXT = RGBColor(0x16, 0x9B, 0x6A)     # #169B6A - High-contrast mint text on white
C_MINT_SOFT = RGBColor(0xE6, 0xFA, 0xF0)     # #E6FAF0 - Soft Mint Tint
C_INK = RGBColor(0x18, 0x1E, 0x34)           # #181E34 - Soft Deep Navy Ink
C_BODY = RGBColor(0x36, 0x41, 0x58)          # #364158 - Slate Navy Body Text
C_MUTED = RGBColor(0x5E, 0x6C, 0x86)         # #5E6C86 - Secondary / Captions
C_ROW_ALT = RGBColor(0xF5, 0xF8, 0xFD)       # #F5F8FD - Cool Table Zebra Row
C_CORAL = RGBColor(0xD9, 0x46, 0x6F)         # #D9466F - Harmonized Rose for Poor / Error
C_CORAL_SOFT = RGBColor(0xFD, 0xEE, 0xF2)    # #FDEEF2 - Soft Rose Tint

FONT_HEAD = "Poppins"
FONT_BODY = "Poppins"

TOTAL_SLIDES = 20


@lru_cache(maxsize=4)
def _make_aura_bg_bytes(variant: str = "content") -> bytes:
    """Generate smooth 16:9 Canva airy #EEF2F3 canvas with luminous #4735F3 -> #61DD99 corner auras."""
    W, H = 1600, 900
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    xn = xx / float(W)
    yn = yy / float(H)

    r = np.full((H, W), 238.0, dtype=np.float32)
    g = np.full((H, W), 242.0, dtype=np.float32)
    b = np.full((H, W), 243.0, dtype=np.float32)

    if variant == "cover":
        blobs = [
            (0.92, 0.04, 0.28, 0.30, (71, 53, 243), 0.42),
            (0.76, 0.06, 0.26, 0.28, (97, 221, 153), 0.36),
            (0.05, 0.96, 0.28, 0.30, (71, 53, 243), 0.42),
            (0.24, 0.96, 0.26, 0.26, (97, 221, 153), 0.34),
            (0.04, 0.06, 0.22, 0.24, (97, 221, 153), 0.16),
        ]
    else:
        blobs = [
            (0.92, 0.00, 0.24, 0.22, (71, 53, 243), 0.40),
            (0.76, 0.02, 0.20, 0.18, (97, 221, 153), 0.30),
            (0.84, 0.08, 0.22, 0.18, (88, 123, 240), 0.22),
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
    """Apply native PowerPoint/Canva 2-stop linear gradient (#4735F3 -> #61DD99)."""
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
    margin_left=0.20,
    margin_right=0.20,
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
    if align == PP_ALIGN.LEFT:
        # Canva's PPTX importer ignores shape text_frame.margin_left on rounded rectangles,
        # so placing an explicit inner textbox guarantees crisp left/right breathing room.
        inner_x = x + margin_left
        inner_w = max(0.3, w - margin_left - margin_right)
        tb = slide.shapes.add_textbox(Inches(inner_x), Inches(y), Inches(inner_w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = False
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = Inches(0.0)
        tf.margin_right = Inches(0.0)
        tf.margin_top = Inches(0.0)
        tf.margin_bottom = Inches(0.0)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run()
        r.text = text
        r.font.name = FONT_HEAD
        r.font.size = Pt(font_size)
        r.font.bold = bold
        r.font.color.rgb = fg_rgb
    else:
        tf = shp.text_frame
        tf.word_wrap = False
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = Inches(margin_left)
        tf.margin_right = Inches(margin_right)
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
    line_spacing=1.20,
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


def _add_bullets(slide, x, y, w, h, items, size=11.0, color=C_BODY, space_after=6, line_spacing=1.20):
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
    """Canva capsule header with generous inner text padding, electric-blue title, and PAGE | XX footer."""
    # Top capsule bar with clean breathing space (matching user's Screenshot 1!)
    _add_pill(
        slide,
        0.55,
        0.18,
        12.23,
        0.36,
        "KELOMPOK 1  ·  INFORMATIKA UNIVERSITAS UDAYANA",
        C_WHITE,
        C_PRIMARY,
        font_size=9.2,
        bold=True,
        border_rgb=C_PRIMARY,
        border_pt=1.0,
        align=PP_ALIGN.LEFT,
        margin_left=0.34,
        margin_right=0.20,
    )
    _add_pill(
        slide,
        9.65,
        0.18,
        3.13,
        0.36,
        section_tag.upper(),
        None,
        C_WHITE,
        font_size=9.0,
        bold=True,
        gradient=True,
        margin_left=0.22,
        margin_right=0.22,
    )

    _add_text(slide, 0.55, 0.60, 12.23, 0.46, title, size=22.5, bold=True, color=C_PRIMARY, font=FONT_HEAD)
    if subtitle:
        _add_text(slide, 0.55, 1.06, 12.23, 0.34, subtitle, size=11.0, color=C_BODY)

    div_y = 1.43 if subtitle else 1.15
    _add_rect(slide, 0.55, div_y, 12.23, 0.022, None, grad_angle=0.0)

    # Bottom capsule footer with generous inner text padding
    _add_pill(
        slide,
        0.55,
        7.03,
        3.25,
        0.32,
        "WATER-QUALITY-DECISION",
        C_WHITE,
        C_PRIMARY,
        font_size=8.6,
        bold=True,
        border_rgb=C_BLUE_MID,
        border_pt=0.95,
        margin_left=0.24,
        margin_right=0.24,
    )
    _add_text(
        slide,
        3.96,
        7.08,
        6.5,
        0.24,
        "Fuzzy Mamdani (27 Rules) + KNN 4D  ·  github.com/dhikrtika/Water-Quality-Decision",
        size=8.4,
        color=C_MUTED,
    )
    _add_pill(
        slide,
        11.15,
        7.03,
        1.63,
        0.32,
        "PAGE",
        C_WHITE,
        C_PRIMARY,
        font_size=8.6,
        bold=True,
        border_rgb=C_PRIMARY,
        border_pt=0.95,
        align=PP_ALIGN.LEFT,
        margin_left=0.26,
        margin_right=0.12,
    )
    _add_pill(
        slide,
        12.04,
        7.03,
        0.74,
        0.32,
        f"{page_num:02d}",
        None,
        C_WHITE,
        font_size=9.0,
        bold=True,
        gradient=True,
        margin_left=0.10,
        margin_right=0.10,
    )


def _add_section_divider(
    prs: Presentation,
    page_num: int,
    part_pill: str,
    title_big: str,
    description: str,
    presenter_name: str,
    presenter_nim: str,
    top_right_tag: str = "FINAL PROJECT TLF 2026",
):
    """Clean, airy minimalist section divider modeled directly on user's Screenshot 2."""
    sl = _new_slide(prs, variant="cover")

    # Top capsule bar matching Screenshot 2 (generous left padding!)
    _add_pill(
        sl,
        0.65,
        0.42,
        8.45,
        0.40,
        "KELOMPOK 1  ·  INFORMATIKA FMIPA UNIVERSITAS UDAYANA",
        C_WHITE,
        C_PRIMARY,
        font_size=9.5,
        bold=True,
        border_rgb=C_PRIMARY,
        border_pt=1.0,
        align=PP_ALIGN.LEFT,
        margin_left=0.36,
        margin_right=0.20,
    )
    _add_pill(
        sl,
        6.35,
        0.42,
        2.75,
        0.40,
        top_right_tag.upper(),
        None,
        C_WHITE,
        font_size=9.2,
        bold=True,
        gradient=True,
        margin_left=0.22,
        margin_right=0.22,
    )

    logo_path = FIG_DIR / "logo_unud.png"
    if logo_path.exists():
        _add_image_fit(sl, logo_path, 0.65, 1.15, 0.88, 0.88)

    _add_pill(
        sl,
        1.72,
        1.36,
        4.35,
        0.42,
        part_pill.upper(),
        None,
        C_WHITE,
        font_size=10.2,
        bold=True,
        gradient=True,
        margin_left=0.28,
        margin_right=0.28,
    )

    _add_text(
        sl,
        0.65,
        2.28,
        10.5,
        1.85,
        title_big,
        size=44,
        bold=True,
        color=C_PRIMARY,
        font=FONT_HEAD,
        line_spacing=1.06,
    )
    _add_text(
        sl,
        0.65,
        4.20,
        8.6,
        1.10,
        description,
        size=14.0,
        color=C_BODY,
        line_spacing=1.35,
    )

    # Clean presenter pill at bottom left + PAGE | XX at bottom right
    _add_pill(
        sl,
        0.65,
        6.55,
        5.85,
        0.42,
        f"PRESENTER  ·  {presenter_name} ({presenter_nim})",
        C_WHITE,
        C_PRIMARY,
        font_size=9.8,
        bold=True,
        border_rgb=C_BLUE_MID,
        border_pt=1.0,
        align=PP_ALIGN.LEFT,
        margin_left=0.34,
        margin_right=0.24,
    )
    _add_pill(
        sl,
        11.05,
        6.58,
        1.63,
        0.34,
        "PAGE",
        C_WHITE,
        C_PRIMARY,
        font_size=8.8,
        bold=True,
        border_rgb=C_PRIMARY,
        border_pt=1.0,
        align=PP_ALIGN.LEFT,
        margin_left=0.26,
        margin_right=0.12,
    )
    _add_pill(
        sl,
        11.94,
        6.58,
        0.74,
        0.34,
        f"{page_num:02d}",
        None,
        C_WHITE,
        font_size=9.2,
        bold=True,
        gradient=True,
        margin_left=0.10,
        margin_right=0.10,
    )
    return sl


def _add_card(slide, x, y, w, h, title=None, accent_rgb=None, fill_rgb=C_WHITE):
    _add_rect(slide, x, y, w, h, fill_rgb, border_rgb=C_BORDER, border_pt=0.85, rounded=True)
    if accent_rgb is not None:
        _add_rect(slide, x + 0.14, y + 0.13, 0.075, h - 0.26, None, grad_angle=90.0)
    if title:
        tx = x + (0.30 if accent_rgb else 0.18)
        tw = w - (0.44 if accent_rgb else 0.36)
        _add_text(slide, tx, y + 0.12, tw, 0.34, title, size=12.6, bold=True, color=C_PRIMARY, font=FONT_HEAD)


def _add_kpi_tile(slide, x, y, w, h, label, value, caption, accent=C_PRIMARY):
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
    # SLIDE 01: COVER (Clean & Airy persis Screenshot 2!)
    # =========================================================================
    s1 = _new_slide(prs, variant="cover")

    _add_pill(
        s1,
        0.65,
        0.42,
        8.45,
        0.40,
        "KELOMPOK 1  ·  INFORMATIKA FMIPA UNIVERSITAS UDAYANA",
        C_WHITE,
        C_PRIMARY,
        font_size=9.5,
        bold=True,
        border_rgb=C_PRIMARY,
        border_pt=1.0,
        align=PP_ALIGN.LEFT,
        margin_left=0.36,
        margin_right=0.20,
    )
    _add_pill(
        s1,
        6.35,
        0.42,
        2.75,
        0.40,
        "FINAL PROJECT TLF 2026",
        None,
        C_WHITE,
        font_size=9.2,
        bold=True,
        gradient=True,
        margin_left=0.22,
        margin_right=0.22,
    )

    logo_path = FIG_DIR / "logo_unud.png"
    if logo_path.exists():
        _add_image_fit(s1, logo_path, 0.65, 1.15, 0.88, 0.88)

    _add_pill(
        s1,
        1.72,
        1.36,
        4.10,
        0.42,
        "FUZZY MAMDANI + KNN",
        None,
        C_WHITE,
        font_size=10.5,
        bold=True,
        gradient=True,
        margin_left=0.28,
        margin_right=0.28,
    )

    _add_text(
        s1,
        0.65,
        2.22,
        9.5,
        2.15,
        "WATER QUALITY\nDECISION SUPPORT\nSYSTEM",
        size=46,
        bold=True,
        color=C_PRIMARY,
        font=FONT_HEAD,
        line_spacing=1.03,
    )
    _add_text(
        s1,
        0.65,
        4.56,
        8.8,
        1.05,
        "Project sistem klasifikasi kelayakan air minum (Potable vs Not Potable) yang menggabungkan Fuzzy Mamdani dan K-Nearest Neighbors, lengkap dengan simulasi interaktif di Streamlit.",
        size=13.5,
        color=C_BODY,
        line_spacing=1.32,
    )

    _add_pill(
        s1,
        0.65,
        6.48,
        6.25,
        0.42,
        "GITHUB  ·  dhikrtika/Water-Quality-Decision",
        C_WHITE,
        C_PRIMARY,
        font_size=9.8,
        bold=True,
        border_rgb=C_BLUE_MID,
        border_pt=1.0,
        align=PP_ALIGN.LEFT,
        margin_left=0.34,
        margin_right=0.24,
    )
    _add_pill(
        s1,
        11.05,
        6.52,
        1.63,
        0.34,
        "PAGE",
        C_WHITE,
        C_PRIMARY,
        font_size=8.8,
        bold=True,
        border_rgb=C_PRIMARY,
        border_pt=1.0,
        align=PP_ALIGN.LEFT,
        margin_left=0.26,
        margin_right=0.12,
    )
    _add_pill(
        s1,
        11.94,
        6.52,
        0.74,
        0.34,
        "01",
        None,
        C_WHITE,
        font_size=9.2,
        bold=True,
        gradient=True,
        margin_left=0.10,
        margin_right=0.10,
    )

    # =========================================================================
    # SLIDE 02: TIM KELOMPOK 1 & PEMBAGIAN 5 BAGIAN PRESENTASI
    # =========================================================================
    s2 = _new_slide(prs)
    _add_chrome(
        s2,
        2,
        "Tim & Alur Presentasi",
        "Kenalan Dulu: Anggota Kelompok 1 & Pembagian Materi",
        "Biar alurnya enak diikuti, presentasi project ini kita bagi jadi 5 bagian yang setara untuk 5 anggota tim.",
    )

    team_headers = ["Bagian", "Nama Anggota", "NIM", "Fokus di Project", "Materi yang Dibawakan"]
    team_rows = [
        [
            "Bagian 1",
            "Nathanael Adrian Wattimena",
            "2408561013",
            "Ketua Kelompok, Analisis Masalah & Laporan",
            "Pendahuluan, ide masalah, dan alur besar sistem (Slide 03-05)",
        ],
        [
            "Bagian 2",
            "I Wayan Arya Adi Guna",
            "2408561019",
            "Data Cleaning, Preprocessing & Eksplorasi Dataset",
            "Dataset Kaggle, cleaning data, dan pilihan fitur (Slide 06-08)",
        ],
        [
            "Bagian 3",
            "Komang Dhika Artika Nurdi",
            "2408561055",
            "Implementasi Fuzzy Mamdani & Perhitungan Manual",
            "Kurva segitiga, 27 rule base, dan cek manual S4 (Slide 09-12)",
        ],
        [
            "Bagian 4",
            "Kadek Phatra Adisuta Timonuli",
            "2408561076",
            "Implementasi KNN, Integrasi & Evaluasi Model",
            "Trace kasus uji Q*, uji Model A vs B, & error analysis (Slide 13-16)",
        ],
        [
            "Bagian 5",
            "I Putu Maichail Ganio Wijaya",
            "2408561123",
            "Streamlit UI, Visualisasi Chart & Dokumentasi",
            "Demo 6 halaman GUI Streamlit, kesimpulan & Q&A (Slide 17-20)",
        ],
    ]
    _add_table(
        s2,
        0.55,
        1.62,
        12.23,
        3.82,
        team_headers,
        team_rows,
        col_widths=[1.05, 2.58, 1.30, 3.25, 4.05],
        font_size=9.8,
        aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT],
        row_bg_fn=lambda r, c, v: C_PRIMARY_SOFT if c == 0 else (C_WHITE if r % 2 == 0 else C_ROW_ALT),
    )

    _add_card(s2, 0.55, 5.68, 3.92, 1.15, "Mata Kuliah & Kampus", accent_rgb=C_PRIMARY)
    _add_text(
        s2,
        0.85,
        6.08,
        3.48,
        0.65,
        "Teknologi Logika Fuzzy (TLF)\nProgram Studi Informatika, FMIPA\nUniversitas Udayana · 2026",
        size=9.8,
        color=C_BODY,
        line_spacing=1.24,
    )

    _add_card(s2, 4.70, 5.68, 3.92, 1.15, "Dosen Pengampu", accent_rgb=C_MINT)
    _add_text(
        s2,
        5.00,
        6.08,
        3.48,
        0.65,
        "I Made Widiartha, S.Si., M.Kom.\nDr. I Gusti Ngurah Anom Cahyadi Putra, S.T., M.Cs.",
        size=9.8,
        color=C_BODY,
        line_spacing=1.30,
    )

    _add_card(s2, 8.86, 5.68, 3.92, 1.15, "Ringkasan Hasil Project", accent_rgb=C_PRIMARY)
    _add_text(
        s2,
        9.16,
        6.08,
        3.48,
        0.65,
        "600 sampel bersih · 27 rules Mamdani\nAkurasi Model B: 97.50% (K = 11)\nUnit test: 5/5 passed · 6 halaman GUI",
        size=9.8,
        color=C_BODY,
        line_spacing=1.24,
    )

    # =========================================================================
    # BAGIAN 01: PENDAHULUAN (Presenter 1: Nathanael Adrian Wattimena)
    # =========================================================================
    _add_section_divider(
        prs,
        page_num=3,
        part_pill="BAGIAN 01  ·  PENDAHULUAN",
        title_big="PENDAHULUAN &\nGAMBARAN SISTEM",
        description="Di bagian awal ini, kita bakal bahas masalah apa yang bikin project ini menarik untuk dibuat, ide solusi yang kita pakai, serta gambaran besar cara kerja sistemnya.",
        presenter_name="Nathanael Adrian Wattimena",
        presenter_nim="2408561013",
        top_right_tag="BAGIAN 01 / 05",
    )

    # SLIDE 04: KENAPA KITA BIKIN PROJECT INI?
    s4 = _new_slide(prs)
    _add_chrome(
        s4,
        4,
        "Bagian 01 · Pendahuluan",
        "Kenapa Cek Kelayakan Air Tidak Cukup Pakai Batas Kaku?",
        "Di data kualitas air, banyak sampel yang nilainya nanggung di daerah perbatasan (borderline).",
    )

    probs = [
        (
            "1. Aturan Kaku (Crisp) Gampang Salah di Batas",
            "Kalau cuma pakai batas saklek if-else (misal pH 6.49 langsung gagal, pH 6.50 langsung lolos), beda tipis 0.01 saja bisa mengubah keputusan secara ekstrem. Padahal di dunia nyata kualitas air berubah secara halus.",
            C_PRIMARY,
        ),
        (
            "2. Parameter Air Saling Memengaruhi",
            "Air yang pH-nya bagus belum tentu aman diminum kalau ternyata keruh (Turbidity tinggi) atau terlalu sadah (Hardness tinggi). Jadi penilaiannya perlu melihat kombinasi beberapa parameter sekaligus.",
            C_MINT,
        ),
        (
            "3. Pengen Akurat tapi Tetap Gampang Dijelaskan",
            "Model klasifikasi biasa kadang sulit dijelaskan alasannya ke pengguna. Lewat Fuzzy Mamdani, kita dapat skor kualitas air yang jelas logikanya, lalu KNN membantu membaca pola kemiripan dari data latih.",
            C_PRIMARY,
        ),
    ]
    py = 1.62
    for title_p, desc_p, acc in probs:
        _add_card(s4, 0.55, py, 6.25, 1.62, title_p, accent_rgb=acc)
        _add_text(s4, 0.86, py + 0.52, 5.75, 1.00, desc_p, size=10.3, color=C_BODY, line_spacing=1.26)
        py += 1.78

    # Right column: 3 Parameter Utama dari Dataset + Tujuan Project (Tanpa WHO/Kemenkes!)
    _add_text(s4, 7.05, 1.60, 5.7, 0.28, "3 PARAMETER UTAMA YANG KITA PAKAI DARI DATASET", size=10.0, bold=True, color=C_PRIMARY)
    param_headers = ["Parameter", "Domain di Sistem", "Kategori Fuzzy", "Peran Penilaian"]
    param_rows = [
        ["pH (X1)", "0 - 14", "Acidic / Neutral / Alkaline", "Mengukur tingkat keasaman air"],
        ["Hardness (X2)", "60 - 300 mg/L", "Soft / Moderate / Hard", "Mengukur kadar mineral terlarut"],
        ["Turbidity (X3)", "1 - 6 NTU", "Clear / Moderate / Turbid", "Mengukur tingkat kekeruhan air"],
    ]
    _add_table(
        s4,
        7.05,
        1.94,
        5.73,
        2.12,
        param_headers,
        param_rows,
        col_widths=[1.22, 1.15, 1.68, 1.68],
        font_size=9.0,
        header_bg=C_BLUE_MID,
        aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT],
    )

    _add_card(s4, 7.05, 4.28, 5.73, 2.52, "Target yang Mau Kita Buktikan di Project Ini", accent_rgb=C_PRIMARY)
    _add_bullets(
        s4,
        7.35,
        4.74,
        5.25,
        1.95,
        [
            ("Skor Kualitas dari Fuzzy Mamdani: ", "Mengubah 3 angka input jadi skor kualitas air 0-100 lewat 27 aturan yang transparan."),
            ("Uji Fitur Tambahan di KNN: ", "Bandingin KNN biasa 3 fitur (Model A) vs KNN 4 fitur + skor fuzzy (Model B) untuk lihat apakah akurasinya naik."),
            ("Aplikasi Siap Pakai: ", "Bikin GUI Streamlit supaya siapapun bisa coba input manual, lihat hitungannya step-by-step, dan cek evaluasi model."),
        ],
        size=10.0,
        space_after=7,
    )

    # SLIDE 05: ALUR KERJA SISTEM (TWO-STAGE PIPELINE)
    s5 = _new_slide(prs)
    _add_chrome(
        s5,
        5,
        "Bagian 01 · Alur Sistem",
        "Cara Kerja Sistem: Gabungan Fuzzy Mamdani + KNN",
        "Sistemnya berjalan dalam dua tahap berurutan: skor dari Fuzzy Mamdani dipakai sebagai fitur ke-4 untuk KNN.",
    )

    _add_rect(s5, 0.55, 1.58, 7.60, 5.26, C_WHITE, border_rgb=C_BORDER, border_pt=0.9, rounded=True)
    _add_image_fit(s5, FIG_DIR / "gambar_3_2_arsitektur_sistem.png", 0.68, 1.70, 7.34, 4.72)
    _add_text(
        s5,
        0.72,
        6.48,
        7.25,
        0.28,
        "Alur dua tahap sistem: input air masuk ke mesin Mamdani dulu, lalu hasilnya ikut masuk ke KNN.",
        size=9,
        italic=True,
        color=C_MUTED,
        align=PP_ALIGN.CENTER,
    )

    _add_card(s5, 8.38, 1.58, 4.40, 1.65, "Tahap 1: Mesin Fuzzy Mamdani", accent_rgb=C_PRIMARY)
    _add_text(
        s5,
        8.68,
        2.02,
        3.92,
        1.12,
        "Input [pH, Hardness, Turbidity] diproses lewat kurva segitiga simetris, 27 aturan MIN-MAX, dan Centroid analitik. Outputnya satu angka jelas: fuzzy_quality_score (0 sampai 100).",
        size=9.9,
        color=C_BODY,
        line_spacing=1.24,
    )

    _add_card(s5, 8.38, 3.38, 4.40, 1.72, "Tahap 2: Model A (3D) vs Model B (4D)", accent_rgb=C_MINT)
    _add_text(
        s5,
        8.68,
        3.82,
        3.92,
        1.18,
        "Model A (Baseline): KNN cuma pakai 3 fitur asli [pH, Hardness, Turbidity].\nModel B (Fuzzy-Enhanced): KNN pakai 4 fitur [pH, Hardness, Turbidity, fuzzy_quality_score].\nTujuannya buat ngebuktiin efek skor fuzzy secara adil.",
        size=9.9,
        color=C_BODY,
        line_spacing=1.24,
    )

    _add_card(s5, 8.38, 5.25, 4.40, 1.59, "Dibangun From-Scratch (Python & NumPy)", accent_rgb=C_PRIMARY, fill_rgb=C_PRIMARY_SOFT)
    _add_text(
        s5,
        8.68,
        5.68,
        3.92,
        1.06,
        "Mesin fuzzy (src/fuzzy_mamdani.py) dan KNN (src/knn_model.py) kita tulis manual tanpa library fuzzy instan. Hasil KNN-nya nanti kita cocokkan dengan scikit-learn (match 100%).",
        size=9.9,
        color=C_PRIMARY_DARK,
        line_spacing=1.24,
    )

    # =========================================================================
    # BAGIAN 02: DATASET & PREPROCESSING (Presenter 2: I Wayan Arya Adi Guna)
    # =========================================================================
    _add_section_divider(
        prs,
        page_num=6,
        part_pill="BAGIAN 02  ·  DATASET & PREPROCESSING",
        title_big="DATASET KAGGLE &\nDATA CLEANING",
        description="Sekarang kita lihat data apa yang kita pakai, gimana proses bersihinnya supaya tidak bias, dan kenapa kita pilih 3 fitur utama ditambah 1 skor fuzzy.",
        presenter_name="I Wayan Arya Adi Guna",
        presenter_nim="2408561019",
        top_right_tag="BAGIAN 02 / 05",
    )

    # SLIDE 07: CLEANING DATA & STATISTIK DESKRIPTIF
    s7 = _new_slide(prs)
    _add_chrome(
        s7,
        7,
        "Bagian 02 · Data Cleaning",
        "Dari 3.276 Baris Mentah Kaggle Jadi 600 Sampel Siap Uji",
        "Dataset diambil dari Kaggle Water Potability, lalu dibersihkan dan diseimbangkan biar model tidak berat sebelah.",
    )

    steps = [
        ("LANGKAH 1", "Data Mentah Kaggle", "3.276 baris, 10 kolom.\nMasih banyak data kosong (491 nilai pH kosong).", C_PRIMARY),
        ("LANGKAH 2", "Bersihkan Data", "Buang baris kosong dan filter ke rentang valid:\npH [0,14], Hard [60,300], Turb [1,6].", C_MINT),
        ("LANGKAH 3", "Seimbangkan Kelas", "Ambil 600 sampel seimbang: 300 Potable dan\n300 Not Potable supaya tidak bias.", C_PRIMARY),
        ("LANGKAH 4", "Split Anti-Leakage", "Bagi 80:20 jadi 480 Train dan 120 Test.\nScaler cuma di-fit dari data Train.", C_MINT),
    ]
    sx = 0.55
    for idx, (tag, stitle, sdesc, acc) in enumerate(steps):
        _add_rect(s7, sx, 1.60, 2.86, 1.52, C_WHITE, border_rgb=C_BORDER, border_pt=0.85, rounded=True)
        _add_rect(s7, sx, 1.60, 2.86, 0.08, None, grad_angle=0.0)
        _add_text(s7, sx + 0.14, 1.74, 1.3, 0.22, tag, size=8.5, bold=True, color=C_PRIMARY)
        _add_text(s7, sx + 0.14, 1.96, 2.58, 0.28, stitle, size=11.8, bold=True, color=C_INK, font=FONT_HEAD)
        _add_text(s7, sx + 0.14, 2.28, 2.58, 0.76, sdesc, size=9.3, color=C_BODY, line_spacing=1.20)
        if idx < 3:
            _add_text(s7, sx + 2.87, 2.15, 0.25, 0.35, "→", size=16, bold=True, color=C_PRIMARY, align=PP_ALIGN.CENTER)
        sx += 3.12

    _add_text(s7, 0.55, 3.34, 6.9, 0.28, "RINGKASAN STATISTIK DATASET BERSIH (600 SAMPEL)", size=10.2, bold=True, color=C_PRIMARY)
    stat_headers = ["Fitur / Variabel", "Min", "Mean", "Std Dev", "Max", "Dipakai Untuk"]
    stat_rows = [
        ["ph (X1)", "1.4318", "7.1165", "1.7151", "13.3499", "Input Mamdani & KNN"],
        ["Hardness (X2)", "73.4922", "195.2735", "34.0901", "286.5680", "Input Mamdani & KNN"],
        ["Turbidity (X3)", "1.8444", "3.9713", "0.7570", "5.9568", "Input Mamdani & KNN"],
        ["fuzzy_quality_score (Y)", "20.3883", "46.3661", "4.8023", "60.0580", "Hasil Mamdani -> Fitur 4"],
        ["Solids (ppm)", "1372.09", "22237.82", "8482.93", "55334.70", "Info eksplorasi saja"],
        ["Chloramines (ppm)", "2.4586", "7.2088", "1.6174", "13.1270", "Info eksplorasi saja"],
        ["Conductivity (uS/cm)", "201.62", "424.45", "79.67", "753.34", "Info eksplorasi saja"],
    ]
    _add_table(
        s7,
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

    _add_card(s7, 8.05, 3.68, 4.73, 3.12, "Kenapa Harus Seimbang & Anti-Leakage?", accent_rgb=C_MINT)
    _add_bullets(
        s7,
        8.35,
        4.14,
        4.25,
        2.55,
        [
            ("Proporsi 50:50: ", "Di data asli Kaggle, kelas Not Potable jauh lebih banyak. Kita samakan jadi 300:300 biar akurasinya jujur."),
            ("Tidak Ada Bocoran Data: ", "Nilai min dan max untuk normalisasi KNN cuma dihitung dari 480 data latih, tidak mengintip 120 data uji."),
            ("Siap Dicek Ulang: ", "Script cleaning-nya (src/prepare_dataset.py) pakai random seed tetap sehingga hasilnya selalu konsisten."),
        ],
        size=10.0,
        space_after=8,
    )

    # SLIDE 08: ALASAN 3 FITUR INTI + 5 SAMPEL MANUAL S1-S5
    s8 = _new_slide(prs)
    _add_chrome(
        s8,
        8,
        "Bagian 02 · Fitur & Data Uji",
        "Kenapa Cuma 3 Fitur Inti + 5 Sampel Referensi Manual?",
        "Memilih jumlah fitur yang pas bikin rule base fuzzy tetap masuk akal dan bisa kita cek manual satu per satu.",
    )

    _add_card(s8, 0.55, 1.60, 5.35, 5.20, "Alasan Kita Pakai 3 Fitur Fisik + 1 Skor Fuzzy", accent_rgb=C_PRIMARY)
    _add_bullets(
        s8,
        0.85,
        2.08,
        4.85,
        4.52,
        [
            ("Mencegah Rule Explosion: ", "Kalau semua 9 kolom Kaggle dimasukkan ke Fuzzy Mamdani (masing-masing 3 kategori), aturannya meledak jadi 3^9 = 19.683 rule! Dengan 3 fitur utama, kita dapat tepat 3^3 = 27 rule yang lengkap dan masih bisa diaudit manusia."),
            ("Paling Mudah Dipahami: ", "pH (keasaman), Hardness (kesadahan mineral), dan Turbidity (kekeruhan) adalah 3 ukuran air paling dasar yang langsung kebayang artinya."),
            ("Fitur ke-4 yang Bernilai: ", "Skor fuzzy_quality_score merangkum interaksi ketiga fitur tadi jadi satu angka 0-100 yang siap membantu KNN memisahkan kelas air."),
            ("Data Mini untuk Cek Manual: ", "Selain 600 data Kaggle, kita juga siapkan 5 sampel referensi (S1 sampai S5) buat membandingkan hitungan kertas vs kode program."),
        ],
        size=10.1,
        space_after=9,
    )

    _add_text(s8, 6.18, 1.60, 6.6, 0.28, "5 SAMPEL REFERENSI MANUAL (manual_calc_sample.csv)", size=10.2, bold=True, color=C_PRIMARY)
    s_headers = ["Kode", "pH", "Hardness", "Turbidity", "Skor Fuzzy", "Label Asli"]
    s_rows = [
        ["S1", "3.50", "240.0", "4.750", "44.0476", "Not Potable"],
        ["S2", "10.50", "240.0", "4.750", "44.0476", "Not Potable"],
        ["S3", "7.00", "180.0", "3.500", "50.0000", "Not Potable"],
        ["S4", "7.00", "120.0", "2.250", "55.9524", "Potable"],
        ["S5", "7.00", "90.0", "1.625", "64.6739", "Potable"],
    ]
    _add_table(
        s8,
        6.18,
        1.94,
        6.60,
        2.68,
        s_headers,
        s_rows,
        col_widths=[0.72, 0.86, 1.15, 1.15, 1.32, 1.40],
        font_size=9.4,
        header_bg=C_BLUE_MID,
        aligns=[PP_ALIGN.CENTER, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT, PP_ALIGN.CENTER],
        row_bg_fn=lambda r, c, v: C_MINT_SOFT if (c == 5 and v == "Potable") else (C_CORAL_SOFT if (c == 5 and v == "Not Potable") else (C_WHITE if r % 2 == 0 else C_ROW_ALT)),
    )

    _add_card(s8, 6.18, 4.84, 6.60, 1.96, "Fungsi 5 Sampel S1-S5 di Presentasi & GUI", accent_rgb=C_MINT)
    _add_bullets(
        s8,
        6.48,
        5.28,
        6.10,
        1.42,
        [
            ("Bukti Hitungan Manual: ", "Sampel S4 dipakai di Bagian 3 buat nunjukin hitungan manual Mamdani yang cocok 0.0000 dengan kode."),
            ("Data Latih Mini KNN: ", "Kelima sampel ini juga dipakai di Bagian 4 sebagai tetangga untuk mengetes kasus uji baru Q* secara manual."),
        ],
        size=10.0,
        space_after=6,
    )

    # =========================================================================
    # BAGIAN 03: FUZZY MAMDANI (Presenter 3: Komang Dhika Artika Nurdi)
    # =========================================================================
    _add_section_divider(
        prs,
        page_num=9,
        part_pill="BAGIAN 03  ·  FUZZY MAMDANI",
        title_big="FUZZY MAMDANI &\nHITUNGAN MANUAL",
        description="Di bagian ini kita masuk ke dapur Fuzzy Mamdani: gimana bentuk kurva keanggotaannya, isi lengkap 27 rule base-nya, dan pembuktian hitungan manual sampel S4.",
        presenter_name="Komang Dhika Artika Nurdi",
        presenter_nim="2408561055",
        top_right_tag="BAGIAN 03 / 05",
    )

    # SLIDE 10: FUNGSI KEANGGOTAAN SEGITIGA SIMETRIS
    s10 = _new_slide(prs)
    _add_chrome(
        s10,
        10,
        "Bagian 03 · Kurva Keanggotaan",
        "Desain Kurva Segitiga Simetris (a, b, c) untuk Semua Variabel",
        "Tiap variabel dibagi jadi 3 himpunan segitiga simetris sehingga total derajat keanggotaannya selalu tepat 1.",
    )

    _add_rect(s10, 0.55, 1.58, 6.75, 5.26, C_WHITE, border_rgb=C_BORDER, border_pt=0.9, rounded=True)
    _add_image_fit(s10, FIG_DIR / "gambar_3_1_membership_functions.png", 0.66, 1.68, 6.53, 4.74)
    _add_text(
        s10,
        0.68,
        6.48,
        6.50,
        0.28,
        "Kurva fungsi keanggotaan segitiga simetris untuk 3 input (pH, Hardness, Turbidity) dan 1 output (Quality Score).",
        size=8.9,
        italic=True,
        color=C_MUTED,
        align=PP_ALIGN.CENTER,
    )

    _add_text(s10, 7.50, 1.56, 5.3, 0.28, "PARAMETER KURVA SEGITIGA (a, b, c)", size=10.2, bold=True, color=C_PRIMARY)
    mf_headers = ["Variabel & Rentang", "3 Kategori Fuzzy", "Titik (a, b, c)"]
    mf_rows = [
        ["pH (X1) [0, 14]", "Acidic / Neutral / Alkaline", "(0,0,7)  |  (0,7,14)  |  (7,14,14)"],
        ["Hardness (X2) [60, 300]", "Soft / Moderate / Hard", "(60,60,180) | (60,180,300) | (180,300,300)"],
        ["Turbidity (X3) [1, 6]", "Clear / Moderate / Turbid", "(1,1,3.5)  |  (1,3.5,6)  |  (3.5,6,6)"],
        ["Quality Score (Y) [0, 100]", "Poor / Moderate / Good", "(0,0,50)  |  (0,50,100)  |  (50,100,100)"],
    ]
    _add_table(
        s10,
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

    _add_card(s10, 7.50, 4.42, 5.28, 2.42, "Rumus & Kelebihan Kurva Simetris", accent_rgb=C_MINT)
    _add_text(
        s10,
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
        s10,
        7.80,
        5.44,
        4.80,
        1.32,
        [
            ("Tidak Ada Titik Kosong: ", "Nilai x berapapun di dalam rentang selalu punya sum(mu) = 1.0000, jadi tidak pernah ada kasus rule mati semua."),
            ("Transisi Halus: ", "Di titik perpotongan (misal pH = 3.5), nilainya terbagi adil 0.50 di dua kategori sekaligus."),
        ],
        size=9.7,
        space_after=5,
    )

    # SLIDE 11: 27 RULE BASE LENGKAP
    s11 = _new_slide(prs)
    _add_chrome(
        s11,
        11,
        "Bagian 03 · 27 Rule Base",
        "Basis Aturan Lengkap Fuzzy Mamdani (27 Rules: R01 - R27)",
        "Semua kombinasi 3 x 3 x 3 kondisi input kita petakan lengkap pakai operator AND = MIN dan agregasi MAX.",
    )

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
        ["Σ 27", "3 x 3 x 3", "27 Rules", "Lengkap", "3G · 9M · 15P"],
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

    _add_table(s11, 0.55, 1.58, 3.45, 5.25, r_headers, rules_left, [0.46, 0.71, 0.76, 0.74, 0.78], font_size=8.0, row_bg_fn=rule_bg, margin_lr=0.02)
    _add_table(s11, 4.52, 1.58, 3.45, 5.25, r_headers, rules_right, [0.46, 0.71, 0.76, 0.74, 0.78], font_size=8.0, row_bg_fn=rule_bg, margin_lr=0.02)

    _add_card(s11, 8.55, 1.58, 4.23, 2.38, "Sebaran Hasil 27 Aturan", accent_rgb=C_MINT)
    _add_pill(s11, 8.83, 2.06, 3.68, 0.42, "GOOD : 3 Rules (R10, R11, R13)", C_MINT_SOFT, C_MINT_TEXT, font_size=9.5)
    _add_pill(s11, 8.83, 2.60, 3.68, 0.42, "MODERATE : 9 Rules (Perbatasan)", C_PRIMARY_SOFT, C_PRIMARY_DARK, font_size=9.5)
    _add_pill(s11, 8.83, 3.14, 3.68, 0.42, "POOR : 15 Rules (Kualitas Rendah)", C_CORAL_SOFT, C_CORAL, font_size=9.5)
    _add_text(s11, 8.83, 3.62, 3.68, 0.28, "Aturan dibuat ketat biar air berisiko tidak lolos.", size=8.9, italic=True, color=C_MUTED)

    _add_card(s11, 8.55, 4.14, 4.23, 2.69, "Cara Kerja Inferensi Mamdani", accent_rgb=C_PRIMARY)
    _add_bullets(
        s11,
        8.83,
        4.58,
        3.75,
        2.16,
        [
            ("Cari Kekuatan Rule (MIN): ", "alpha_k = min(mu_pH, mu_Hardness, mu_Turbidity) untuk tiap rule."),
            ("Potong Kurva Output: ", "Kurva output (Poor/Moderate/Good) dipotong setinggi nilai alpha_k."),
            ("Gabungkan Semua (MAX): ", "Ambil batas atas tertinggi dari semua rule aktif jadi satu kurva gabungan."),
            ("Logika Utamanya: ", "Output Good cuma keluar kalau pH Neutral dan tidak ada kondisi Hard atau Turbid."),
        ],
        size=9.5,
        space_after=5,
    )

    # SLIDE 12: VERIFIKASI HITUNGAN MANUAL SAMPEL S4 (CENTROID ANALITIK)
    s12 = _new_slide(prs)
    _add_chrome(
        s12,
        12,
        "Bagian 03 · Cek Manual S4",
        "Buktikan Hitungan Manual vs Program: Sampel S4",
        "Kita coba hitung manual S4 (pH = 7.00, Hardness = 120.0, Turbidity = 2.25) pakai Centroid analitik eksak.",
    )

    _add_card(s12, 0.55, 1.58, 6.05, 1.98, "Langkah 1: Fuzzifikasi Input S4", accent_rgb=C_PRIMARY)
    fuz_headers = ["Variabel", "Nilai x", "Derajat Keanggotaan (mu)"]
    fuz_rows = [
        ["pH (X1)", "7.00", "Acidic = 0.0000  |  Neutral = 1.0000  |  Alkaline = 0.0000"],
        ["Hardness (X2)", "120.0", "Soft = 0.5000  |  Moderate = 0.5000  |  Hard = 0.0000"],
        ["Turbidity (X3)", "2.25", "Clear = 0.5000  |  Moderate = 0.5000  |  Turbid = 0.0000"],
    ]
    _add_table(s12, 0.80, 2.04, 5.20, 1.36, fuz_headers, fuz_rows, col_widths=[1.05, 0.65, 3.50], font_size=8.6, aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT])

    _add_card(s12, 0.55, 3.74, 6.05, 3.10, "Langkah 2: 4 Rule Aktif (MIN) & Gabungan (MAX)", accent_rgb=C_MINT)
    s4_r_headers = ["Rule", "Kondisi (X1, X2, X3)", "mu1, mu2, mu3", "alpha", "Output"]
    s4_r_rows = [
        ["R10", "(Neutral, Soft, Clear)", "1.0, 0.5, 0.5", "0.5000", "Good"],
        ["R11", "(Neutral, Soft, Moderate)", "1.0, 0.5, 0.5", "0.5000", "Good"],
        ["R13", "(Neutral, Moderate, Clear)", "1.0, 0.5, 0.5", "0.5000", "Good"],
        ["R14", "(Neutral, Moderate, Mod.)", "1.0, 0.5, 0.5", "0.5000", "Moderate"],
    ]
    _add_table(
        s12,
        0.80,
        4.20,
        5.20,
        1.82,
        s4_r_headers,
        s4_r_rows,
        col_widths=[0.50, 1.80, 1.04, 0.76, 1.10],
        font_size=8.6,
        header_bg=C_BLUE_MID,
        aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER],
        row_bg_fn=lambda r, c, v: C_MINT_SOFT if v == "Good" else (C_PRIMARY_SOFT if v == "Moderate" else (C_WHITE if r % 2 == 0 else C_ROW_ALT)),
    )
    _add_text(
        s12,
        0.80,
        6.14,
        5.65,
        0.58,
        "Hasil MAX: Poor = 0.0000 | Moderate = 0.5000 | Good = 0.5000\nKurva akhirnya rata di tinggi 0.50 mulai z = 25 sampai z = 100.",
        size=9.4,
        bold=True,
        color=C_INK,
        line_spacing=1.22,
    )

    _add_card(s12, 6.82, 1.58, 5.96, 3.35, "Langkah 3: Hitung Luas (A) & Momen (M) Analitik", accent_rgb=C_PRIMARY)
    int_headers = ["Segmen", "Interval z", "Persamaan mu(z)", "Luas A_i", "Momen M_i"]
    int_rows = [
        ["Segmen 1", "[0.00, 25.00]", "mu(z) = 0.0200 z", "6.2500", "104.1667"],
        ["Segmen 2", "[25.00, 100.00]", "mu(z) = 0.5000", "37.5000", "2343.7500"],
        ["TOTAL", "[0.00, 100.00]", "Jumlah A & M", "43.7500", "2447.9167"],
    ]
    _add_table(
        s12,
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
        s12,
        7.08,
        3.86,
        5.52,
        0.95,
        "Karena pakai integral eksak per segmen (bukan taksiran grid titik):\nA1 = 0.5 * 25 * 0.50 = 6.2500   |   M1 = (0.02 / 3) * 25^3 = 104.1667\nA2 = (100 - 25) * 0.50 = 37.5000 | M2 = 0.25 * (100^2 - 25^2) = 2343.7500",
        size=9.4,
        color=C_BODY,
        line_spacing=1.28,
    )

    _add_rect(s12, 6.82, 5.12, 5.96, 1.72, None, rounded=True, grad_angle=0.0)
    _add_text(s12, 7.10, 5.28, 5.48, 0.26, "HASIL AKHIR DEFUZZIFIKASI & COCOKAN KODE", size=9.5, bold=True, color=C_WHITE)
    _add_text(s12, 7.10, 5.64, 5.48, 0.44, "z* (S4) = 2447.9167 / 43.7500 = 55.9524", size=16.2, bold=True, color=C_WHITE, font=FONT_HEAD)
    _add_text(s12, 7.10, 6.20, 5.48, 0.44, "Output Program = 55.9524  |  Selisih = 0.0000 (100% COCOK)", size=10.2, bold=True, color=RGBColor(0xF0, 0xFB, 0xF7))

    # =========================================================================
    # BAGIAN 04: KNN & EVALUASI MODEL (Presenter 4: Kadek Phatra Adisuta T.)
    # =========================================================================
    _add_section_divider(
        prs,
        page_num=13,
        part_pill="BAGIAN 04  ·  KNN & EVALUASI MODEL",
        title_big="KLASIFIKASI KNN &\nHASIL EVALUASI",
        description="Setelah skor Mamdani keluar, sekarang kita lihat gimana KNN 4D bekerja pada kasus uji baru Q*, lalu kita adu akurasi Model A (3D) vs Model B (4D).",
        presenter_name="Kadek Phatra Adisuta Timonuli",
        presenter_nim="2408561076",
        top_right_tag="BAGIAN 04 / 05",
    )

    # SLIDE 14: TRACE END-TO-END KASUS UJI BARU Q*
    s14 = _new_slide(prs)
    _add_chrome(
        s14,
        14,
        "Bagian 04 · Trace Kasus Q*",
        "Simulasi End-to-End pada Sampel Baru Q* (Mamdani -> KNN 4D)",
        "Misal ada sampel air baru Q* = (pH 5.25, Hardness 150.0, Turbidity 2.25). Ini alur lengkap sampai keluar keputusannya.",
    )

    _add_card(s14, 0.55, 1.58, 5.65, 5.26, "Tahap 1: Hitung Skor Fuzzy Mamdani untuk Q*", accent_rgb=C_PRIMARY)
    _add_bullets(
        s14,
        0.84,
        2.02,
        5.18,
        1.42,
        [
            ("Fuzzifikasi: ", "pH (Acidic=0.25, Neutral=0.75); Hardness (Soft=0.25, Moderate=0.75); Turbidity (Clear=0.50, Moderate=0.50)."),
            ("8 Rule Aktif: ", "R01, R02, R04, R05 (alpha=0.25); R10, R11 (alpha=0.25); R13, R14 (alpha=0.50)."),
            ("Hasil MAX: ", "Poor = 0.2500  |  Moderate = 0.5000  |  Good = 0.5000."),
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
        s14,
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

    _add_rect(s14, 0.80, 5.66, 5.20, 0.96, C_MINT_SOFT, border_rgb=C_MINT_TEXT, border_pt=1.0, rounded=True)
    _add_text(s14, 0.98, 5.76, 4.88, 0.36, "z* (Q*) = 2454.4271 / 45.3125 = 54.1667", size=14.5, bold=True, color=C_MINT_TEXT)
    _add_text(s14, 0.98, 6.16, 4.88, 0.34, "Vektor 4D Q* = [5.25, 150.0, 2.25, 54.1667] -> Scaled [0.250, 0.400, 0.200, 0.491]", size=8.9, bold=True, color=C_INK)

    _add_card(s14, 6.42, 1.58, 6.36, 5.26, "Tahap 2: Normalisasi Min-Max 4D & Cari Tetangga Terdekat", accent_rgb=C_MINT)
    _add_text(
        s14,
        6.68,
        2.02,
        5.90,
        0.46,
        "Semua 4 fitur diskalakan ke [0, 1] pakai rentang S1-S5, lalu dihitung jarak Euclidean 4D dari Q* ke tiap sampel referensi:",
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
        s14,
        6.68,
        2.58,
        5.55,
        2.45,
        knn_headers,
        knn_rows,
        col_widths=[0.44, 0.54, 2.20, 0.80, 0.99, 0.58],
        font_size=8.6,
        header_bg=C_BLUE_MID,
        aligns=[PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.RIGHT, PP_ALIGN.CENTER, PP_ALIGN.CENTER],
        row_bg_fn=lambda r, c, v: C_MINT_SOFT if (r in (0, 2) and c in (4, 5)) else (C_CORAL_SOFT if (r == 1 and c == 4) else (C_WHITE if r % 2 == 0 else C_ROW_ALT)),
    )

    _add_rect(s14, 6.72, 5.26, 5.88, 1.36, None, rounded=True, grad_angle=0.0)
    _add_text(s14, 6.96, 5.38, 5.4, 0.26, "HASIL VOTING 3 TETANGGA TERDEKAT (K = 3)", size=9.2, bold=True, color=C_WHITE)
    _add_text(s14, 6.96, 5.66, 5.4, 0.44, "Prediksi Q* = POTABLE  (Vote: 2 Potable vs 1 Not Potable)", size=14.0, bold=True, color=C_WHITE, font=FONT_HEAD)
    _add_text(
        s14,
        6.96,
        6.16,
        5.4,
        0.38,
        "3 tetangga terdekat: S4 (Potable), S3 (Not Potable), dan S5 (Potable). Hasil ini 100% sama dengan fitur Step-by-Step di GUI.",
        size=9.0,
        color=RGBColor(0xF0, 0xFB, 0xF7),
    )

    # SLIDE 15: PERBANDINGAN MODEL A VS MODEL B LINTAS K
    s15 = _new_slide(prs)
    _add_chrome(
        s15,
        15,
        "Bagian 04 · Model A vs B",
        "Hasil Uji Coba: Model A (3 Fitur) vs Model B (4 Fitur + Fuzzy)",
        "Diadu pada 120 data uji (480 train / 120 test) untuk K = 3, 5, 7, 9, dan 11. Semua dihitung from-scratch dan dicek ke scikit-learn.",
    )

    _add_rect(s15, 0.55, 1.58, 6.30, 5.26, C_WHITE, border_rgb=C_BORDER, border_pt=0.9, rounded=True)
    _add_image_fit(s15, FIG_DIR / "gambar_4_1_perbandingan_model_k.png", 0.66, 1.72, 6.08, 4.65)
    _add_text(
        s15,
        0.68,
        6.46,
        6.05,
        0.30,
        "Grafik akurasi dan Macro-F1 Model A (Baseline 3D) vs Model B (Fuzzy-Enhanced 4D) lintas K.",
        size=9,
        italic=True,
        color=C_MUTED,
        align=PP_ALIGN.CENTER,
    )

    _add_text(s15, 7.05, 1.56, 5.7, 0.28, "TABEL PERBANDINGAN AKURASI (120 DATA UJI)", size=10.2, bold=True, color=C_PRIMARY)
    ev_headers = ["Nilai K", "Model A", "Model B", "Selisih", "Macro-F1 B", "Sklearn"]
    ev_rows = [
        ["K = 3", "92.50%", "95.83%", "+3.33%", "95.83%", "100%"],
        ["K = 5", "92.50%", "95.00%", "+2.50%", "95.00%", "100%"],
        ["K = 7", "93.33%", "95.83%", "+2.50%", "95.83%", "100%"],
        ["K = 9", "91.67%", "95.83%", "+4.17%", "95.83%", "100%"],
        ["K = 11", "93.33%", "97.50%", "+4.17%", "97.50%", "100%"],
    ]
    _add_table(
        s15,
        7.05,
        1.88,
        5.73,
        2.55,
        ev_headers,
        ev_rows,
        col_widths=[0.84, 0.90, 0.96, 1.01, 1.12, 0.90],
        font_size=9.4,
        aligns=[PP_ALIGN.CENTER] * 6,
        row_bg_fn=lambda r, c, v: C_MINT_SOFT if (r == 4 or c == 3) else (C_WHITE if r % 2 == 0 else C_ROW_ALT),
        highlight_col=2,
    )

    _add_card(s15, 7.05, 4.62, 5.73, 2.22, "Apa yang Bisa Kita Lihat dari Hasil Ini?", accent_rgb=C_MINT)
    _add_bullets(
        s15,
        7.35,
        5.04,
        5.26,
        1.70,
        [
            ("Model B Menang di Semua K: ", "Nambahin skor fuzzy bikin akurasi naik terus +2.50% sampai +4.17% tanpa pernah turun sekali pun."),
            ("Paling Bagus di K = 11: ", "Akurasi tembus 97.50% dengan Macro-F1 97.50%, artinya dari 120 data uji cuma salah 3 data saja."),
            ("Kode Scratch Terbukti Valid: ", "100% prediksi KNN buatan kita sendiri cocok persis dengan KNeighborsClassifier dari scikit-learn."),
        ],
        size=9.8,
        space_after=6,
    )

    # SLIDE 16: CONFUSION MATRIX OPTIMAL (K = 11)
    s16 = _new_slide(prs)
    _add_chrome(
        s16,
        16,
        "Bagian 04 · Analisis Error",
        "Bedah Kesalahan Prediksi di K = 11 (Confusion Matrix)",
        "Dengan tambahan fitur fuzzy_quality_score, jumlah salah tebak turun drastis dari 8 sampel jadi cuma 3 sampel.",
    )

    _add_rect(s16, 0.55, 1.58, 6.45, 5.26, C_WHITE, border_rgb=C_BORDER, border_pt=0.9, rounded=True)
    _add_image_fit(s16, FIG_DIR / "slide_confusion_matrix_k11.png", 0.66, 1.72, 6.23, 4.65)
    _add_text(
        s16,
        0.68,
        6.46,
        6.20,
        0.30,
        "Confusion Matrix di K = 11: Model A (kiri, 93.33%) dibanding Model B (kanan, 97.50%) pada 120 data uji.",
        size=9,
        italic=True,
        color=C_MUTED,
        align=PP_ALIGN.CENTER,
    )

    _add_text(s16, 7.20, 1.56, 5.58, 0.28, "DETAIL METRIK PER KELAS MODEL B (K = 11)", size=10.2, bold=True, color=C_PRIMARY)
    pc_headers = ["Kelas", "Precision", "Recall", "F1-Score", "Jumlah"]
    pc_rows = [
        ["Not Potable (0)", "98.31%", "96.67%", "97.48%", "60"],
        ["Potable (1)", "96.72%", "98.33%", "97.52%", "60"],
        ["Rata-rata Macro", "97.51%", "97.50%", "97.50%", "120"],
    ]
    _add_table(
        s16,
        7.20,
        1.88,
        5.58,
        1.78,
        pc_headers,
        pc_rows,
        col_widths=[1.58, 1.00, 1.00, 1.00, 1.00],
        font_size=9.5,
        header_bg=C_BLUE_MID,
        aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER],
        row_bg_fn=lambda r, c, v: C_PRIMARY_SOFT if r == 2 else (C_WHITE if r % 2 == 0 else C_ROW_ALT),
    )

    _add_kpi_tile(s16, 7.20, 3.84, 2.68, 1.18, "Error Model A (3D)", "8 / 120", "2 FP + 6 FN (Recall Potable 90%)", accent=C_CORAL)
    _add_kpi_tile(s16, 10.10, 3.84, 2.68, 1.18, "Error Model B (4D)", "3 / 120", "2 FP + 1 FN (Turun 62.5%!)", accent=C_MINT)

    _add_card(s16, 7.20, 5.18, 5.58, 1.66, "Poin Penting dari Analisis Error", accent_rgb=C_PRIMARY)
    _add_bullets(
        s16,
        7.50,
        5.60,
        5.12,
        1.16,
        [
            ("Salah Tolak (FN) Turun Tajam: ", "Air layak minum yang salah ditebak turun dari 6 sampel di Model A jadi cuma 1 sampel di Model B."),
            ("Tetap Aman untuk Air Buruk: ", "False Positive tetap kecil banget (2 dari 60 sampel Not Potable) dengan Precision 98.31%."),
        ],
        size=9.8,
        space_after=5,
    )

    # =========================================================================
    # BAGIAN 05: DEMO APLIKASI & PENUTUP (Presenter 5: I Putu Maichail Ganio W.)
    # =========================================================================
    _add_section_divider(
        prs,
        page_num=17,
        part_pill="BAGIAN 05  ·  DEMO APLIKASI & PENUTUP",
        title_big="APLIKASI STREAMLIT &\nKESIMPULAN PROJECT",
        description="Terakhir, kita bakal tunjukin langsung tampilan aplikasi Streamlit 6 halaman yang sudah kita bangun, plus ringkasan kesimpulan project sebelum masuk ke tanya jawab.",
        presenter_name="I Putu Maichail Ganio Wijaya",
        presenter_nim="2408561123",
        top_right_tag="BAGIAN 05 / 05",
    )

    # SLIDE 18: GUI STREAMLIT HALAMAN 01 - 03
    s18 = _new_slide(prs)
    _add_chrome(
        s18,
        18,
        "Bagian 05 · Demo GUI (1/2)",
        "Tampilan Aplikasi Streamlit Kita: Halaman 01 s.d. 03",
        "Aplikasi web interaktif dibangun modular pakai Streamlit & Plotly (app.py + src/ui/) supaya mudah didemokan.",
    )

    gui_1_3 = [
        (
            "01 · Dashboard",
            FIG_DIR / "gui_01_dashboard.png",
            "Halaman depan buat lihat ringkasan angka penting (600 data, skor rata-rata 46.37, akurasi Model B 97.50%, 100% match sklearn), alur sistem, dan profil Kelompok 1.",
        ),
        (
            "02 · Input & Dataset",
            FIG_DIR / "gui_02_input_dataset.png",
            "Tempat simulasi langsung: bisa geser slider pH/Hardness/Turbidity, klik preset S1-S5 atau Q*, pilih mode tetangga KNN, sampai upload file CSV sendiri.",
        ),
        (
            "03 · Step-by-Step Process",
            FIG_DIR / "gui_03_step_by_step.png",
            "Mode transparansi (white-box): nunjukin posisi input di kurva segitiga, rule mana saja yang nyala, bentuk kurva hasil MAX, Centroid eksak, dan jarak KNN-nya.",
        ),
    ]
    gx = 0.55
    for title_g, img_g, desc_g in gui_1_3:
        _add_rect(s18, gx, 1.58, 3.92, 5.26, C_WHITE, border_rgb=C_BORDER, border_pt=0.9, rounded=True)
        _add_rect(s18, gx, 1.58, 3.92, 0.08, None, grad_angle=0.0)
        _add_pill(s18, gx + 0.16, 1.76, 2.65, 0.32, title_g, None, C_WHITE, font_size=9.2, gradient=True, margin_left=0.18, margin_right=0.18)
        _add_rect(s18, gx + 0.14, 2.20, 3.64, 2.40, RGBColor(0x0B, 0x10, 0x1C), border_rgb=C_BORDER, border_pt=0.5)
        _add_image_fit(s18, img_g, gx + 0.16, 2.22, 3.60, 2.36)
        _add_text(s18, gx + 0.18, 4.74, 3.56, 1.96, desc_g, size=10.1, color=C_BODY, line_spacing=1.26)
        gx += 4.15

    # SLIDE 19: GUI STREAMLIT HALAMAN 04 - 06
    s19 = _new_slide(prs)
    _add_chrome(
        s19,
        19,
        "Bagian 05 · Demo GUI (2/2)",
        "Tampilan Aplikasi Streamlit Kita: Halaman 04 s.d. 06",
        "Dilengkapi ranking seluruh dataset, lab uji coba Model A vs Model B secara interaktif, dan halaman panduan rumus.",
    )

    gui_4_6 = [
        (
            "04 · Classification Results",
            FIG_DIR / "gui_04_results.png",
            "Menampilkan hasil penilaian 600 sampel sekaligus, lengkap dengan filter kelas Potable/Not Potable, filter skor minimum, grafik distribusi, dan tombol download CSV.",
        ),
        (
            "05 · Model Evaluation",
            FIG_DIR / "gui_05_evaluation.png",
            "Lab eksperimen langsung: bisa ubah nilai K, ganti metode scaling (Min-Max / Z-Score), lihat Confusion Matrix, dan bukti kecocokan 100% dengan scikit-learn.",
        ),
        (
            "06 · Docs & Guide",
            FIG_DIR / "gui_06_docs.png",
            "Halaman dokumentasi singkat di dalam aplikasi berisi rumus Fuzzy Mamdani & KNN 4D, tabel lengkap 27 rule base, dan petunjuk pemakaian tiap menu.",
        ),
    ]
    gx = 0.55
    for title_g, img_g, desc_g in gui_4_6:
        _add_rect(s19, gx, 1.58, 3.92, 5.26, C_WHITE, border_rgb=C_BORDER, border_pt=0.9, rounded=True)
        _add_rect(s19, gx, 1.58, 3.92, 0.08, None, grad_angle=0.0)
        _add_pill(s19, gx + 0.16, 1.76, 2.75, 0.32, title_g, None, C_WHITE, font_size=9.2, gradient=True, margin_left=0.18, margin_right=0.18)
        _add_rect(s19, gx + 0.14, 2.20, 3.64, 2.40, RGBColor(0x0B, 0x10, 0x1C), border_rgb=C_BORDER, border_pt=0.5)
        _add_image_fit(s19, img_g, gx + 0.16, 2.22, 3.60, 2.36)
        _add_text(s19, gx + 0.18, 4.74, 3.56, 1.96, desc_g, size=10.1, color=C_BODY, line_spacing=1.26)
        gx += 4.15

    # SLIDE 20: KESIMPULAN & PENUTUP (Q&A)
    s20 = _new_slide(prs)
    _add_chrome(
        s20,
        20,
        "Bagian 05 · Penutup",
        "Kesimpulan Project & Sesi Tanya Jawab",
        "Ringkasan apa yang berhasil kita buktikan di project ini beserta ide pengembangannya ke depan.",
    )

    _add_kpi_tile(s20, 0.55, 1.58, 2.90, 1.18, "Akurasi Terbaik (Model B)", "97.50%", "Di K = 11 (Macro-F1: 97.50%)", accent=C_PRIMARY)
    _add_kpi_tile(s20, 3.66, 1.58, 2.90, 1.18, "Kenaikan vs Model A", "+4.17%", "Selalu unggul di semua nilai K", accent=C_MINT)
    _add_kpi_tile(s20, 6.77, 1.58, 2.90, 1.18, "Selisih Hitungan Manual", "0.0000", "Persis sama untuk S4 & Q*", accent=C_PRIMARY)
    _add_kpi_tile(s20, 9.88, 1.58, 2.90, 1.18, "Validasi Kode", "100%", "Match scikit-learn · 5/5 Pytest", accent=C_MINT)

    _add_card(s20, 0.55, 2.96, 6.45, 3.88, "Poin Utama yang Kita Buktikan", accent_rgb=C_PRIMARY)
    _add_bullets(
        s20,
        0.86,
        3.42,
        5.96,
        3.28,
        [
            ("Fuzzy Mamdani Jelas & Akurat: ", "Pakai kurva segitiga simetris, 27 rule lengkap, dan Centroid analitik, hasil program kita cocok 100% (selisih 0.0000) sama hitungan manual."),
            ("Skor Fuzzy Beneran Bantu KNN: ", "Nambahin fuzzy_quality_score di Model B bikin akurasi naik di semua nilai K dan memangkas error dari 8 jadi cuma 3 sampel di K = 11."),
            ("Evaluasi Jujur & Teruji: ", "Scaling Min-Max di-fit khusus dari data latih (anti-leakage), plus semua unit test (5/5) dan validasi scikit-learn tembus 100%."),
            ("Siap Langsung Didemokan: ", "Lewat GUI Streamlit 6 halaman, siapapun bisa langsung coba input sampel baru dan lihat proses hitungannya transparan."),
        ],
        size=10.2,
        space_after=8,
    )

    _add_card(s20, 7.22, 2.96, 5.56, 1.98, "Ide Pengembangan Selanjutnya", accent_rgb=C_MINT)
    _add_bullets(
        s20,
        7.52,
        3.40,
        5.08,
        1.45,
        [
            ("Coba Fitur & Pembobotan Tambahan: ", "Bisa diuji pakai Weighted KNN atau ditambah parameter lain dari dataset (seperti Solids dan Chloramines)."),
            ("Sambungkan ke Sensor IoT: ", "Mesin Mamdani + KNN ini siap dipakai baca data sensor pH dan kekeruhan secara real-time."),
        ],
        size=9.7,
        space_after=6,
    )

    _add_rect(s20, 7.22, 5.12, 5.56, 1.72, None, rounded=True, grad_angle=0.0)
    _add_text(s20, 7.50, 5.26, 5.05, 0.44, "TERIMA KASIH  ·  ADA PERTANYAAN?", size=16.5, bold=True, color=C_WHITE, font=FONT_HEAD)
    _add_text(
        s20,
        7.50,
        5.76,
        5.05,
        0.96,
        "Kelompok 1 · Informatika Universitas Udayana\nGitHub: github.com/dhikrtika/Water-Quality-Decision\nDemo Lokal:  streamlit run app.py  (http://localhost:8501)",
        size=9.8,
        color=RGBColor(0xF0, 0xFB, 0xF7),
        line_spacing=1.28,
    )

    OUT_PPTX.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT_PPTX))
    print(f"[SUCCESS] Generated {TOTAL_SLIDES}-slide presentation: {OUT_PPTX} ({OUT_PPTX.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build_presentation()
