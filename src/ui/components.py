"""Reusable HTML UI primitives for crisp dark-slate analytical rendering."""

from html import escape
from typing import Dict, List, Optional, Sequence, Tuple
import streamlit as st

from src.ui.constants import PALETTE

# Crisp inline SVG icon (1.85px stroke, consistent geometry)
WATER_ICON_SVG = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>'
    '<path d="M9.5 14.5a3 3 0 0 0 3 2.5"/>'
    "</svg>"
)


def render_html(raw_html: str) -> None:
    """Render multi-line HTML safely in Streamlit without triggering Markdown code blocks."""
    cleaned = "\n".join(line.strip() for line in raw_html.strip().splitlines() if line.strip())
    st.markdown(cleaned, unsafe_allow_html=True)


def status_badge(label: str, variant: Optional[str] = None) -> str:
    """Return an HTML semantic status pill matching Potable/Moderate/Poor/Neutral."""
    low = str(label).strip().lower()
    if variant is None:
        if low in ("potable", "good", "aktif", "layak") or low.startswith("top-"):
            variant = "potable"
        elif low in ("moderate", "transisi", "sedang"):
            variant = "moderate"
        elif low in ("not potable", "poor", "acidic", "hard", "turbid", "tidak layak"):
            variant = "poor"
        elif low in ("neutral", "model b", "white-box"):
            variant = "cobalt"
        else:
            variant = "neutral"
    return f'<span class="badge badge-{variant}">{escape(str(label))}</span>'


def render_sidebar_brand() -> None:
    """Render the brand header at the top of the dark navigation rail."""
    render_html(
        f"""
        <div class="sb-brand">
            <div class="sb-brand-icon">{WATER_ICON_SVG}</div>
            <div>
                <div class="sb-brand-title">Water Quality DSS</div>
                <div class="sb-brand-sub">Kelompok 1 · Informatika Unud</div>
            </div>
        </div>
        """
    )


def render_sidebar_telemetry(
    ph: float,
    hardness: float,
    turbidity: float,
    z_star: float,
    k_neighbors: int,
    dataset_rows: int,
    quality_label: str,
) -> None:
    """Render the recessed active sample telemetry card in the sidebar."""
    render_html(
        f"""
        <div class="sb-tray">
            <div class="sb-tray-head">
                <span class="sb-tray-title">Active Sample</span>
                {status_badge(quality_label)}
            </div>
            <div class="sb-kv"><span class="k">pH (X1)</span><span class="v">{ph:.2f}</span></div>
            <div class="sb-kv"><span class="k">Hardness (X2)</span><span class="v">{hardness:.1f} mg/L</span></div>
            <div class="sb-kv"><span class="k">Turbidity (X3)</span><span class="v">{turbidity:.3f} NTU</span></div>
            <div class="sb-kv"><span class="k">Centroid (z*)</span><span class="v">{z_star:.4f}</span></div>
            <div class="sb-kv"><span class="k">KNN Neighbors</span><span class="v">K = {k_neighbors}</span></div>
            <div class="sb-kv"><span class="k">Active Dataset</span><span class="v">{dataset_rows} rows</span></div>
        </div>
        """
    )


def render_page_header(title: str, subtitle: str, chip_text: Optional[str] = None) -> None:
    """Render a clean top header bar with optional right-aligned status chip."""
    chip_html = f'<div class="header-chip">{escape(chip_text)}</div>' if chip_text else ""
    render_html(
        f"""
        <div class="page-header">
            <div class="page-header-copy">
                <div class="page-title" role="heading" aria-level="1">{escape(title)}</div>
                <p class="page-subtitle">{escape(subtitle)}</p>
            </div>
            {chip_html}
        </div>
        """
    )


def render_kpi_grid(cards: Sequence[Dict[str, str]]) -> None:
    """Render a 4-column monospace KPI strip."""
    items_html = []
    for c in cards:
        tone = c.get("tone", "cobalt")
        items_html.append(
            f'<div class="kpi-card">'
            f'<div class="kpi-label">{escape(c["label"])}</div>'
            f'<div class="kpi-value">{escape(c["value"])}</div>'
            f'<div class="kpi-meta {tone}">{escape(c.get("meta", ""))}</div>'
            f"</div>"
        )
    render_html(f'<div class="kpi-grid">{"".join(items_html)}</div>')


def render_notice(html_body: str, accent: bool = False) -> None:
    """Render a crisp full-bordered info callout."""
    cls = "atlas-notice accent" if accent else "atlas-notice"
    render_html(f'<div class="{cls}">{html_body}</div>')


def render_focus_cue(tag: str, html_text: str) -> None:
    """Render a compact single-row focus cue clarifying what to inspect on this page."""
    render_html(
        f'<div class="focus-cue">'
        f'<span class="focus-cue-tag">{escape(tag)}</span>'
        f"<span>{html_text}</span>"
        f"</div>"
    )


def navigate_to(page_id: str) -> None:
    """Navigate cleanly to another page while keeping sidebar radio and URL synced."""
    st.session_state["nav_page"] = page_id
    st.session_state["_last_q_page"] = page_id
    st.query_params["page"] = page_id


def render_next_step_bar(
    summary: str,
    button_label: str,
    target_page_id: str,
    button_key: str,
) -> None:
    """Render a consistent bottom navigation bar to step smoothly between pages."""
    st.divider()
    with st.container(border=True):
        c_text, c_btn = st.columns([2.4, 1.0], gap="medium", vertical_alignment="center")
        with c_text:
            st.markdown(f"**Langkah Berikutnya**\n\n{summary}")
        with c_btn:
            st.button(
                button_label,
                key=button_key,
                type="primary",
                width="stretch",
                on_click=navigate_to,
                args=(target_page_id,),
            )


def render_physicochemical_strip(ph: float, hardness: float, turbidity: float) -> None:
    """Render the signature live physicochemical WHO/Permenkes range-compliance strip."""
    ph_pct = max(0.0, min(100.0, (ph / 14.0) * 100.0))
    if 6.5 <= ph <= 8.5:
        ph_color, ph_note = PALETTE["potable"], "WHO Ideal (6.5-8.5)"
    elif 5.0 <= ph <= 9.5:
        ph_color, ph_note = PALETTE["moderate"], "Borderline pH"
    else:
        ph_color, ph_note = PALETTE["poor"], "Extreme Acidic/Alkaline"

    h_pct = max(0.0, min(100.0, ((hardness - 60.0) / 240.0) * 100.0))
    if hardness <= 150.0:
        h_color, h_note = PALETTE["potable"], "Soft"
    elif hardness <= 210.0:
        h_color, h_note = PALETTE["moderate"], "Moderate"
    else:
        h_color, h_note = PALETTE["poor"], "Hard"

    t_pct = max(0.0, min(100.0, ((turbidity - 1.0) / 5.0) * 100.0))
    if turbidity <= 2.5:
        t_color, t_note = PALETTE["potable"], "Clear"
    elif turbidity <= 4.0:
        t_color, t_note = PALETTE["moderate"], "Slightly Turbid"
    else:
        t_color, t_note = PALETTE["poor"], "Turbid"

    render_html(
        f"""
        <div class="spectrum-grid">
            <div class="spectrum-card">
                <div class="spectrum-top">
                    <span class="spectrum-name">pH (X1)</span>
                    <span class="spectrum-val">{ph:.2f}</span>
                </div>
                <div class="spectrum-track">
                    <div class="spectrum-fill" style="width: {ph_pct:.1f}%; background-color: {ph_color};"></div>
                </div>
                <div class="spectrum-meta"><span>0.0 - 14.0</span><span style="color:{ph_color};">{ph_note}</span></div>
            </div>
            <div class="spectrum-card">
                <div class="spectrum-top">
                    <span class="spectrum-name">Hardness (X2)</span>
                    <span class="spectrum-val">{hardness:.1f} mg/L</span>
                </div>
                <div class="spectrum-track">
                    <div class="spectrum-fill" style="width: {h_pct:.1f}%; background-color: {h_color};"></div>
                </div>
                <div class="spectrum-meta"><span>60 - 300 mg/L</span><span style="color:{h_color};">{h_note}</span></div>
            </div>
            <div class="spectrum-card">
                <div class="spectrum-top">
                    <span class="spectrum-name">Turbidity (X3)</span>
                    <span class="spectrum-val">{turbidity:.3f} NTU</span>
                </div>
                <div class="spectrum-track">
                    <div class="spectrum-fill" style="width: {t_pct:.1f}%; background-color: {t_color};"></div>
                </div>
                <div class="spectrum-meta"><span>1.0 - 6.0 NTU</span><span style="color:{t_color};">{t_note}</span></div>
            </div>
        </div>
        """
    )


def render_alpha_bar(alpha: float, quality_label: str) -> str:
    """Render an inline horizontal firing-strength bar alongside a 4-decimal readout."""
    pct = max(0.0, min(100.0, alpha * 100.0))
    color_map = {
        "Good": PALETTE["potable"],
        "Moderate": PALETTE["moderate"],
        "Poor": PALETTE["poor"],
    }
    fill = color_map.get(quality_label, PALETTE["cobalt_bright"])
    return (
        f'<div class="alpha-cell">'
        f'<div class="alpha-bar-track"><div class="alpha-bar-fill" style="width:{pct:.1f}%;background-color:{fill};"></div></div>'
        f"<strong>{alpha:.4f}</strong>"
        f"</div>"
    )


def render_table(
    headers: Sequence[Tuple[str, bool]],
    rows: Sequence[Tuple[Sequence[str], str]],
) -> None:
    """Render a precision HTML table with strict tabular numerals."""
    th_html = "".join(
        f'<th class="{"num" if is_num else ""}">{label}</th>' for label, is_num in headers
    )
    tr_list: List[str] = []
    for cells, row_cls in rows:
        cls_attr = f' class="{row_cls}"' if row_cls else ""
        td_html = []
        for idx, cell in enumerate(cells):
            is_num = headers[idx][1] if idx < len(headers) else False
            td_cls = ' class="num"' if is_num else ""
            td_html.append(f"<td{td_cls}>{cell}</td>")
        tr_list.append(f"<tr{cls_attr}>{''.join(td_html)}</tr>")

    render_html(
        f'<div class="atlas-table-wrap"><table class="atlas-table">'
        f"<thead><tr>{th_html}</tr></thead>"
        f'<tbody>{"".join(tr_list)}</tbody></table></div>'
    )
