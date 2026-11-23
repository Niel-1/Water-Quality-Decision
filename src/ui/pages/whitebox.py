"""Page 3: White-Box Step-by-Step Fuzzy Mamdani & KNN Mathematical Audit."""

from html import escape
import pandas as pd
import streamlit as st

from src.ui.charts import plot_aggregated_centroid, plot_membership_functions
from src.ui.components import (
    render_alpha_bar,
    render_html,
    render_kpi_grid,
    render_notice,
    render_page_header,
    render_physicochemical_strip,
    render_table,
    status_badge,
)
from src.ui.constants import REFERENCE_MODES
from src.ui.data import evaluate_single_sample


def render_whitebox(df_active: pd.DataFrame, df_manual: pd.DataFrame) -> None:
    """Render Page 3 (Proses Pengolahan White-Box Step-by-Step)."""
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

    render_page_header(
        title="Step-by-Step Process (White-Box)",
        subtitle="Trace perhitungan lengkap 4 desimal (0.0000) dari fuzzifikasi segitiga simetris, 27 rules Mamdani, integral Centroid analitik, sampai Euclidean Distance KNN.",
        chip_text=f"K={k_eff} · {REFERENCE_MODES.get(ref_mode, ref_mode)}",
    )

    render_html(
        """
        <div class="stepper-grid">
            <div class="step-card">
                <div class="step-code">STEP 01</div>
                <div class="step-title">Fuzzification</div>
                <p class="step-desc">Memetakan pH, Hardness, dan Turbidity ke derajat keanggotaan &mu; &isin; [0, 1] dengan &Sigma;&mu; = 1.</p>
            </div>
            <div class="step-card">
                <div class="step-code">STEP 02-03</div>
                <div class="step-title">27 Rules & Implication</div>
                <p class="step-desc">Menghitung firing strength &alpha; = min(&mu;1, &mu;2, &mu;3) dan memotong tinggi kurva output (MIN).</p>
            </div>
            <div class="step-card">
                <div class="step-code">STEP 04-05</div>
                <div class="step-title">Aggregation & Centroid</div>
                <p class="step-desc">Menggabungkan output (MAX) lalu menghitung titik pusat massa z* = &Sigma;M / &Sigma;A secara analitik.</p>
            </div>
            <div class="step-card">
                <div class="step-code">STEP 06</div>
                <div class="step-title">Min-Max & KNN Distance</div>
                <p class="step-desc">Normalisasi vektor 4D ke [0, 1], hitung jarak Euclidean, dan tentukan kelas lewat majority voting.</p>
            </div>
        </div>
        """
    )

    render_physicochemical_strip(x1, x2, x3)

    # Step 1: 4 Membership Function Charts
    st.subheader("Step 1: Membership Function Curves")
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

    # Step 2: Fuzzification Table
    st.divider()
    st.subheader("Step 2: Input Fuzzification Table (μ)")
    fuz = fuzzy_res["fuzzified"]
    render_table(
        headers=[
            ("Input Variable", False),
            ("Crisp Value", True),
            ("Set 1", False),
            ("μ1", True),
            ("Set 2", False),
            ("μ2", True),
            ("Set 3", False),
            ("μ3", True),
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

    # Step 3: 27 Rule Base Evaluation with Inline Firing-Strength Bars
    st.divider()
    st.subheader("Step 3: 27 Rule Base Evaluation & Firing Strength (α)")
    only_active = st.checkbox(
        "Tampilkan hanya active rules (α > 0.0000)",
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
                    status_badge("Active" if r["is_active"] else "Inactive", "potable" if r["is_active"] else "neutral"),
                ],
                row_cls,
            )
        )

    render_table(
        headers=[
            ("Rule", False),
            ("IF pH", False),
            ("μ(X1)", True),
            ("AND Hardness", False),
            ("μ(X2)", True),
            ("AND Turbidity", False),
            ("μ(X3)", True),
            ("α = min(μ1,μ2,μ3)", True),
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
        "<strong>MAX Aggregation per Output Set:</strong> &nbsp; "
        f"{status_badge(lbl_poor, 'poor')} &nbsp; "
        f"{status_badge(lbl_mod, 'moderate')} &nbsp; "
        f"{status_badge(lbl_good, 'potable')}"
    )

    # Step 4 & 5: Aggregated Curve & Analytic Integral Segments
    st.divider()
    st.subheader("Step 4 & 5: Implication (MIN), Aggregation (MAX) & Analytic Centroid")
    st.plotly_chart(plot_aggregated_centroid(fuzzy_res), width="stretch")

    tot_a = fuzzy_res["analytic"]["total_area"]
    tot_m = fuzzy_res["analytic"]["total_moment"]
    z_disc = fuzzy_res["discrete_centroid"]

    seg_rows = [
        (
            [
                f"<strong>Segment {s['segment_id']}</strong>",
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
            ("Segment", False),
            ("Interval [z0, z1]", True),
            ("Equation μ_agg(z)", False),
            ("μ(z0)", True),
            ("μ(z1)", True),
            ("Area A_i", True),
            ("Moment M_i", True),
        ],
        rows=seg_rows,
    )

    render_kpi_grid(
        [
            {"label": "Total Moment (∑ M_i)", "value": f"{tot_m:.4f}", "meta": "Integral Numerator", "tone": "muted"},
            {"label": "Total Area (∑ A_i)", "value": f"{tot_a:.4f}", "meta": "Integral Denominator", "tone": "muted"},
            {"label": "Analytic Centroid (z*)", "value": f"{z_star:.4f}", "meta": "0.0000 Diff vs Manual", "tone": "cobalt"},
            {"label": "Discrete Centroid (1001 pts)", "value": f"{z_disc:.4f}", "meta": f"Diff: {abs(z_star - z_disc):.4f}", "tone": "moderate"},
        ]
    )

    st.latex(
        rf"z^* = \frac{{\int_{{0}}^{{100}} z \cdot \mu_{{\text{{agg}}}}(z)\,dz}}{{\int_{{0}}^{{100}} \mu_{{\text{{agg}}}}(z)\,dz}} = \frac{{\sum M_i}}{{\sum A_i}} = \frac{{{tot_m:.4f}}}{{{tot_a:.4f}}} = {z_star:.4f}"
    )

    # Step 6: Min-Max Normalization & Euclidean KNN Distances
    st.divider()
    st.subheader("Step 6: Min-Max Scaling, Euclidean Distance & Majority Voting")
    scaler = sim["scaler"]
    q_raw = sim["query_raw"]
    q_sc = sim["query_scaled"]

    render_table(
        headers=[
            ("Feature Vector", False),
            ("X1: pH", True),
            ("X2: Hardness (mg/L)", True),
            ("X3: Turbidity (NTU)", True),
            ("Y: Fuzzy Score", True),
        ],
        rows=[
            (["<strong>Train Min (X_min)</strong>", f"{scaler.min_[0]:.4f}", f"{scaler.min_[1]:.4f}", f"{scaler.min_[2]:.4f}", f"{scaler.min_[3]:.4f}"], ""),
            (["<strong>Train Max (X_max)</strong>", f"{scaler.max_[0]:.4f}", f"{scaler.max_[1]:.4f}", f"{scaler.max_[2]:.4f}", f"{scaler.max_[3]:.4f}"], ""),
            (["<strong>Raw Query Vector (Q*)</strong>", f"{q_raw[0]:.4f}", f"{q_raw[1]:.4f}", f"{q_raw[2]:.4f}", f"{q_raw[3]:.4f}"], ""),
            (["<strong>Normalized Query (Q'*)</strong>", f"<strong>{q_sc[0]:.4f}</strong>", f"<strong>{q_sc[1]:.4f}</strong>", f"<strong>{q_sc[2]:.4f}</strong>", f"<strong>{q_sc[3]:.4f}</strong>"], "row-highlight"),
        ],
    )

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
                    status_badge(f"Top-{k_eff}", "cobalt") if is_topk else status_badge("Outside K", "neutral"),
                ],
                "row-highlight" if is_topk else "",
            )
        )

    render_table(
        headers=[
            ("Rank", True),
            ("Sample ID", False),
            ("Raw [X1, X2, X3, Y]", True),
            ("Scaled [X'1, X'2, X'3, Y']", True),
            ("Squared Diff Sum", True),
            ("Distance d(Q*, S_i)", True),
            ("Label", False),
            ("Voting", False),
        ],
        rows=knn_rows,
    )

    render_notice(
        f"<strong>Final Majority Voting (K = {k_eff}):</strong> "
        f"Votes = <code>{escape(str(knn_det['vote_counts']))}</code> &rarr; "
        f"Predicted Class = {status_badge(knn_det['predicted_class'])}",
        accent=True,
    )
