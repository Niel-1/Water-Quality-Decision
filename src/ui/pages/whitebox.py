"""Page 3: White-Box Step-by-Step Fuzzy Mamdani & KNN Mathematical Audit."""

from html import escape
import pandas as pd
import streamlit as st

from src.fuzzy_mamdani import MF_PARAMS
from src.ui.charts import plot_aggregated_centroid, plot_membership_functions
from src.ui.components import (
    render_alpha_bar,
    render_focus_cue,
    render_html,
    render_kpi_grid,
    render_next_step_bar,
    render_notice,
    render_page_header,
    render_table,
    status_badge,
)
from src.ui.constants import REFERENCE_MODES
from src.ui.data import evaluate_single_sample


def _format_mf_step(x: float, a: float, b: float, c: float, mu: float) -> str:
    """Format substitusi rumus kurva segitiga untuk perhitungan manual."""
    if a == b:
        if x <= a:
            return f"x = {x:.2f} &le; {a:g} &rarr; <strong>{mu:.4f}</strong>"
        if x >= c:
            return f"x = {x:.2f} &ge; {c:g} &rarr; <strong>{mu:.4f}</strong>"
        return f"({c:g} - {x:.2f}) / ({c:g} - {b:g}) = <strong>{mu:.4f}</strong>"
    if b == c:
        if x >= c:
            return f"x = {x:.2f} &ge; {c:g} &rarr; <strong>{mu:.4f}</strong>"
        if x <= a:
            return f"x = {x:.2f} &le; {a:g} &rarr; <strong>{mu:.4f}</strong>"
        return f"({x:.2f} - {a:g}) / ({b:g} - {a:g}) = <strong>{mu:.4f}</strong>"
    if x <= a or x >= c:
        return f"x = {x:.2f} di luar ({a:g}, {c:g}) &rarr; <strong>{mu:.4f}</strong>"
    if abs(x - b) < 1e-9:
        return f"x = {x:.2f} tepat di puncak {b:g} &rarr; <strong>{mu:.4f}</strong>"
    if a < x < b:
        return f"({x:.2f} - {a:g}) / ({b:g} - {a:g}) = <strong>{mu:.4f}</strong>"
    return f"({c:g} - {x:.2f}) / ({c:g} - {b:g}) = <strong>{mu:.4f}</strong>"


def _format_segment_area_step(seg: dict) -> str:
    """Format substitusi rumus luas segmen A_i."""
    z0, z1 = seg["z_start"], seg["z_end"]
    y0, y1 = seg["mu_start"], seg["mu_end"]
    if abs(y0 - y1) < 1e-7:
        return f"({z1:.2f} - {z0:.2f}) &times; {y0:.4f} = <strong>{seg['area']:.4f}</strong>"
    return f"0.5 &times; ({z1:.2f} - {z0:.2f}) &times; ({y0:.4f} + {y1:.4f}) = <strong>{seg['area']:.4f}</strong>"


def _format_segment_moment_step(seg: dict) -> str:
    """Format substitusi rumus momen segmen M_i."""
    z0, z1 = seg["z_start"], seg["z_end"]
    y0, y1 = seg["mu_start"], seg["mu_end"]
    dz = z1 - z0
    if abs(y0 - y1) < 1e-7:
        return f"0.5 &times; {y0:.4f} &times; ({z1:.2f}&sup2; - {z0:.2f}&sup2;) = <strong>{seg['moment']:.4f}</strong>"
    return (
        f"({dz:.2f} / 6) &times; [{y0:.4f}&times;({2*z0 + z1:.2f}) + {y1:.4f}&times;({z0 + 2*z1:.2f})] "
        f"= <strong>{seg['moment']:.4f}</strong>"
    )


def render_whitebox(df_active: pd.DataFrame, df_manual: pd.DataFrame) -> None:
    """Render Page 3 (Bedah Perhitungan 1 Sampel Aktif)."""
    inp = st.session_state["manual_input"]
    x1, x2, x3 = inp["ph"], inp["Hardness"], inp["Turbidity"]
    k_val = inp["k_neighbors"]
    ref_mode = inp.get("reference_mode", "manual_5")

    sim = evaluate_single_sample(
        ph=x1,
        hardness=x2,
        turbidity=x3,
        k_neighbors=k_val,
        reference_mode=ref_mode,
        df_active=df_active,
        df_manual=df_manual,
    )
    fuzzy_res = sim["fuzzy"]
    knn_det = sim["knn_detail"]
    k_eff = sim["k_eff"]
    z_star = fuzzy_res["water_quality_score"]
    pred_cls = knn_det["predicted_class"]

    render_page_header(
        title="Bedah Perhitungan (Sampel Aktif)",
        subtitle="Penelusuran matematis 4 desimal untuk 1 sampel aktif: dari fuzzifikasi, evaluasi 27 aturan, integral Centroid, hingga jarak Euclidean KNN.",
        chip_text=f"K={k_eff} · {REFERENCE_MODES.get(ref_mode, ref_mode)}",
    )

    render_focus_cue(
        "FOKUS HALAMAN 03",
        "<strong>Bedah mendalam untuk 1 sampel aktif.</strong> Gunakan 3 tab di bawah untuk menelusuri alur perhitungan "
        "secara bertahap dari Fuzzy Mamdani sampai keputusan kelas KNN.",
    )

    render_html(
        f"""
        <div class="sample-ribbon">
            <div class="sample-ribbon-items">
                <span class="sample-ribbon-kv"><span class="k">pH (X1)</span><span class="v">{x1:.2f}</span></span>
                <span class="sample-ribbon-kv"><span class="k">Hardness (X2)</span><span class="v">{x2:.2f} mg/L</span></span>
                <span class="sample-ribbon-kv"><span class="k">Turbidity (X3)</span><span class="v">{x3:.4f} NTU</span></span>
                <span class="sample-ribbon-kv"><span class="k">Skor Fuzzy (z*)</span><span class="v">{z_star:.4f}</span></span>
                <span class="sample-ribbon-kv"><span class="k">Aturan Aktif</span><span class="v">{len(fuzzy_res['active_rules'])} / 27</span></span>
            </div>
            <div>{status_badge(fuzzy_res['quality_linguistic'])} &nbsp; {status_badge(pred_cls)}</div>
        </div>
        """
    )

    tab_fuz, tab_defuz, tab_knn = st.tabs(
        [
            "1. Fuzzifikasi & 27 Aturan",
            "2. Agregasi & Defuzzifikasi Centroid",
            "3. Normalisasi & Klasifikasi KNN",
        ]
    )

    with tab_fuz:
        st.subheader("1A. Kurva Fungsi Keanggotaan Input & Output")
        g1, g2 = st.columns(2, gap="medium")
        with g1:
            st.plotly_chart(
                plot_membership_functions("ph", "Input 1: pH (X1 · Domain 0-14)", "pH", x1),
                width="stretch",
            )
            st.plotly_chart(
                plot_membership_functions("Turbidity", "Input 3: Turbidity (X3 · 1-6 NTU)", "Turbidity (NTU)", x3),
                width="stretch",
            )
        with g2:
            st.plotly_chart(
                plot_membership_functions("Hardness", "Input 2: Hardness (X2 · 60-300 mg/L)", "Hardness (mg/L)", x2),
                width="stretch",
            )
            st.plotly_chart(
                plot_membership_functions(
                    "water_quality_score",
                    "Output: Fuzzy Quality Score (Y · 0-100)",
                    "Water Quality Score (0-100)",
                    z_star,
                ),
                width="stretch",
            )

        st.divider()
        st.subheader("1B. Tabel Derajat Keanggotaan Input (μ)")
        fuz = fuzzy_res["fuzzified"]
        render_table(
            headers=[
                ("Variabel Input", False),
                ("Nilai Crisp", True),
                ("Himpunan 1", False),
                ('<span class="math-sym">μ</span>1', True),
                ("Himpunan 2", False),
                ('<span class="math-sym">μ</span>2', True),
                ("Himpunan 3", False),
                ('<span class="math-sym">μ</span>3', True),
            ],
            rows=[
                (
                    [
                        "<strong>X1: pH (0-14)</strong>",
                        f"{x1:.4f}",
                        status_badge("Acidic [0, 0, 7]", "poor"),
                        f"{fuz['ph']['Acidic']:.4f}",
                        status_badge("Neutral [0, 7, 14]", "cobalt"),
                        f"{fuz['ph']['Neutral']:.4f}",
                        status_badge("Alkaline [7, 14, 14]", "moderate"),
                        f"{fuz['ph']['Alkaline']:.4f}",
                    ],
                    "",
                ),
                (
                    [
                        "<strong>X2: Hardness (mg/L)</strong>",
                        f"{x2:.4f}",
                        status_badge("Soft [60, 60, 180]", "potable"),
                        f"{fuz['Hardness']['Soft']:.4f}",
                        status_badge("Moderate [60, 180, 300]", "moderate"),
                        f"{fuz['Hardness']['Moderate']:.4f}",
                        status_badge("Hard [180, 300, 300]", "poor"),
                        f"{fuz['Hardness']['Hard']:.4f}",
                    ],
                    "",
                ),
                (
                    [
                        "<strong>X3: Turbidity (NTU)</strong>",
                        f"{x3:.4f}",
                        status_badge("Clear [1, 1, 3.5]", "potable"),
                        f"{fuz['Turbidity']['Clear']:.4f}",
                        status_badge("Moderate [1, 3.5, 6]", "moderate"),
                        f"{fuz['Turbidity']['Moderate']:.4f}",
                        status_badge("Turbid [3.5, 6, 6]", "poor"),
                        f"{fuz['Turbidity']['Turbid']:.4f}",
                    ],
                    "",
                ),
            ],
        )

        with st.expander("Jabaran Hitung Manual Fuzzifikasi (Substitusi Rumus Kurva Segitiga)", expanded=True):
            st.latex(
                r"\mu(x; a, b, c) = \max\left(0,\; \min\left(\frac{x - a}{b - a},\; \frac{c - x}{c - b}\right)\right)"
            )
            mf_step_rows = []
            for var_key, var_label, raw_val in [
                ("ph", "X1: pH", max(0.0, min(14.0, float(x1)))),
                ("Hardness", "X2: Hardness", max(60.0, min(300.0, float(x2)))),
                ("Turbidity", "X3: Turbidity", max(1.0, min(6.0, float(x3)))),
            ]:
                for set_name, (a, b, c) in MF_PARAMS[var_key]["sets"].items():
                    mu_val = fuz[var_key][set_name]
                    mf_step_rows.append(
                        (
                            [
                                f"<strong>{var_label}</strong>",
                                f"{set_name} <code>[{a:g}, {b:g}, {c:g}]</code>",
                                _format_mf_step(raw_val, a, b, c, mu_val),
                            ],
                            "row-highlight" if mu_val > 0.0 else "",
                        )
                    )
            render_table(
                headers=[
                    ("Variabel", False),
                    ("Himpunan & Titik [a, b, c]", False),
                    ("Substitusi Hitung Manual", False),
                ],
                rows=mf_step_rows,
            )

        st.divider()
        st.subheader("1C. Evaluasi 27 Basis Aturan & Firing Strength (α)")
        only_active = st.checkbox(
            "Tampilkan hanya aturan aktif (α > 0.0000)",
            value=True,
        )
        rules_list = fuzzy_res["active_rules"] if only_active else fuzzy_res["rules"]

        rule_rows = []
        for r in rules_list:
            row_cls = "row-highlight" if (r["is_active"] and not only_active) else ""
            rule_rows.append(
                (
                    [
                        f"<code>{r['rule_id']}</code>",
                        r["ph"],
                        f"{r['mu_ph']:.4f}",
                        r["Hardness"],
                        f"{r['mu_hardness']:.4f}",
                        r["Turbidity"],
                        f"{r['mu_turbidity']:.4f}",
                        render_alpha_bar(r["alpha"], r["water_quality_score"]),
                        status_badge(r["water_quality_score"]),
                        status_badge("Aktif" if r["is_active"] else "Nonaktif", "potable" if r["is_active"] else "neutral"),
                    ],
                    row_cls,
                )
            )

        render_table(
            headers=[
                ("Rule", False),
                ("IF pH", False),
                ('<span class="math-sym">μ</span>(X1)', True),
                ("AND Hardness", False),
                ('<span class="math-sym">μ</span>(X2)', True),
                ("AND Turbidity", False),
                ('<span class="math-sym">μ</span>(X3)', True),
                ('<span class="math-sym">α = min(μ1, μ2, μ3)</span>', True),
                ("THEN Quality", False),
                ("Status", False),
            ],
            rows=rule_rows,
        )

        agg = fuzzy_res["aggregated_alpha"]
        lbl_poor = f"α_Poor = {agg['Poor']:.4f}"
        lbl_mod = f"α_Moderate = {agg['Moderate']:.4f}"
        lbl_good = f"α_Good = {agg['Good']:.4f}"
        render_notice(
            "<strong>Hasil Agregasi MAX per Himpunan Output:</strong> &nbsp; "
            f"{status_badge(lbl_poor, 'poor')} &nbsp; "
            f"{status_badge(lbl_mod, 'moderate')} &nbsp; "
            f"{status_badge(lbl_good, 'potable')}"
        )

    with tab_defuz:
        st.subheader("2A. Kurva Agregasi MAX & Titik Centroid (z*)")
        st.plotly_chart(plot_aggregated_centroid(fuzzy_res), width="stretch")

        tot_a = fuzzy_res["analytic"]["total_area"]
        tot_m = fuzzy_res["analytic"]["total_moment"]
        z_disc = fuzzy_res["discrete_centroid"]

        st.subheader("2B. Rincian Integral Segmen Centroid Analitik")
        seg_rows = [
            (
                [
                    f"<strong>Segmen {s['segment_id']}</strong>",
                    f"[{s['z_start']:.4f}, {s['z_end']:.4f}]",
                    f"<code>{s['equation']}</code>",
                    f"{s['mu_start']:.4f}",
                    f"{s['mu_end']:.4f}",
                    f"{s['area']:.4f}",
                    f"<strong>{s['moment']:.4f}</strong>",
                ],
                "",
            )
            for s in fuzzy_res["analytic"]["segments"]
        ]
        seg_rows.append(
            (
                [
                    "<strong>TOTAL INTEGRAL</strong>",
                    "[0.0000, 100.0000]",
                    "<code>&Sigma; A_i &amp; &Sigma; M_i</code>",
                    "-",
                    "-",
                    f"{tot_a:.4f}",
                    f"{tot_m:.4f}",
                ],
                "row-total",
            )
        )

        render_table(
            headers=[
                ("Segmen", False),
                ("Interval [z0, z1]", True),
                ('Persamaan <span class="math-sym">μ_agg(z)</span>', False),
                ('<span class="math-sym">μ(z0)</span>', True),
                ('<span class="math-sym">μ(z1)</span>', True),
                ("Luas A_i", True),
                ("Momen M_i", True),
            ],
            rows=seg_rows,
        )

        with st.expander("Jabaran Hitung Manual Luas (A_i) & Momen (M_i) per Segmen", expanded=True):
            st.latex(
                r"A_i = \frac{1}{2}(z_1 - z_0)\big(\mu(z_0) + \mu(z_1)\big), \qquad "
                r"M_i = \int_{z_0}^{z_1} z \cdot \mu(z)\,dz = \frac{z_1 - z_0}{6}\Big(\mu(z_0)(2z_0 + z_1) + \mu(z_1)(z_0 + 2z_1)\Big)"
            )
            seg_step_rows = [
                (
                    [
                        f"<strong>Segmen {s['segment_id']}</strong> <code>[{s['z_start']:.2f}, {s['z_end']:.2f}]</code>",
                        _format_segment_area_step(s),
                        _format_segment_moment_step(s),
                    ],
                    "",
                )
                for s in fuzzy_res["analytic"]["segments"]
            ]
            render_table(
                headers=[
                    ("Segmen & Interval", False),
                    ("Substitusi Luas A_i", False),
                    ("Substitusi Momen M_i", False),
                ],
                rows=seg_step_rows,
            )

        render_kpi_grid(
            [
                {"label": "Total Momen (∑ M_i)", "value": f"{tot_m:.4f}", "meta": "Pembilang Integral", "tone": "muted"},
                {"label": "Total Luas (∑ A_i)", "value": f"{tot_a:.4f}", "meta": "Penyebut Integral", "tone": "muted"},
                {"label": "Fuzzy Quality Score (z*)", "value": f"{z_star:.4f}", "meta": "Output Defuzzifikasi Centroid", "tone": "cobalt"},
                {"label": "Centroid Diskrit (1001 titik)", "value": f"{z_disc:.4f}", "meta": f"Selisih Aproksimasi: {abs(z_star - z_disc):.4f}", "tone": "moderate"},
            ]
        )

        st.latex(
            rf"\text{{fuzzy\_quality\_score}} = z^* = \frac{{\int_{{0}}^{{100}} z \cdot \mu_{{\text{{agg}}}}(z)\,dz}}{{\int_{{0}}^{{100}} \mu_{{\text{{agg}}}}(z)\,dz}} = \frac{{\sum M_i}}{{\sum A_i}} = \frac{{{tot_m:.4f}}}{{{tot_a:.4f}}} = {z_star:.4f}"
        )

    with tab_knn:
        st.subheader("3A. Normalisasi Min-Max pada Vektor 4 Fitur [pH, Hardness, Turbidity, z*]")
        scaler = sim["scaler"]
        q_raw = sim["query_raw"]
        q_sc = sim["query_scaled"]

        render_table(
            headers=[
                ("Vektor Fitur", False),
                ("X1: pH", True),
                ("X2: Hardness (mg/L)", True),
                ("X3: Turbidity (NTU)", True),
                ("Y: Skor Fuzzy (z*)", True),
            ],
            rows=[
                (["<strong>Min Data Latih (X_min)</strong>", f"{scaler.min_[0]:.4f}", f"{scaler.min_[1]:.4f}", f"{scaler.min_[2]:.4f}", f"{scaler.min_[3]:.4f}"], ""),
                (["<strong>Max Data Latih (X_max)</strong>", f"{scaler.max_[0]:.4f}", f"{scaler.max_[1]:.4f}", f"{scaler.max_[2]:.4f}", f"{scaler.max_[3]:.4f}"], ""),
                (["<strong>Vektor Sampel Asli (Q*)</strong>", f"{q_raw[0]:.4f}", f"{q_raw[1]:.4f}", f"{q_raw[2]:.4f}", f"{q_raw[3]:.4f}"], ""),
                (["<strong>Sampel Ternormalisasi (Q'*)</strong>", f"<strong>{q_sc[0]:.4f}</strong>", f"<strong>{q_sc[1]:.4f}</strong>", f"<strong>{q_sc[2]:.4f}</strong>", f"<strong>{q_sc[3]:.4f}</strong>"], "row-highlight"),
            ],
        )

        st.subheader(f"3B. Jarak Euclidean 4D & Pemungutan Suara (K = {k_eff})")
        knn_rows = []
        for n in sim["neighbors_table"]:
            rf = n["raw_features"]
            sf = n["scaled_features"]
            sq = n["feature_sq_diffs"]
            is_topk = n["rank"] <= k_eff
            knn_rows.append(
                (
                    [
                        f"<strong>#{n['rank']}</strong>",
                        f"<code>{escape(str(n['sample_id']))}</code>",
                        f"[{rf[0]:.2f}, {rf[1]:.2f}, {rf[2]:.3f}, {rf[3]:.4f}]",
                        f"[{sf[0]:.4f}, {sf[1]:.4f}, {sf[2]:.4f}, {sf[3]:.4f}]",
                        f"{sq[0]:.4f} + {sq[1]:.4f} + {sq[2]:.4f} + {sq[3]:.4f} = {n['sum_sq_diff']:.4f}",
                        f"<strong>{n['distance']:.4f}</strong>",
                        status_badge(n["label"]),
                        status_badge(f"Top-{k_eff}", "cobalt") if is_topk else status_badge("Di luar K", "neutral"),
                    ],
                    "row-highlight" if is_topk else "",
                )
            )

        render_table(
            headers=[
                ("Rank", True),
                ("ID Sampel", False),
                ("Nilai Asli [X1, X2, X3, Y]", True),
                ("Skala [X'1, X'2, X'3, Y']", True),
                ("Jumlah Kuadrat Selisih", True),
                ("Jarak d(Q*, S_i)", True),
                ("Label", False),
                ("Voting", False),
            ],
            rows=knn_rows,
        )

        render_notice(
            f"<strong>Keputusan Voting Mayoritas (K = {k_eff}):</strong> "
            f"Perolehan suara = <code>{escape(str(knn_det['vote_counts']))}</code> &rarr; "
            f"Prediksi Akhir = {status_badge(pred_cls)}",
            accent=True,
        )

    render_next_step_bar(
        summary="Setelah membedah 1 sampel aktif, lihat bagaimana Model B memeringkat seluruh dataset (600 sampel) sekaligus beserta interpretasinya.",
        button_label="Lanjut ke 04 · Hasil & Ranking ->",
        target_page_id="results",
        button_key="next_from_whitebox",
    )
