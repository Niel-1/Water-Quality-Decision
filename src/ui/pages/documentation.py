"""Page 6: Mathematical Specification, Complete 27 Rule Base & User Manual."""

import pandas as pd
import streamlit as st

from src.fuzzy_mamdani import RULES_27
from src.ui.components import render_html, render_page_header


def render_documentation() -> None:
    """Render Page 6 (System Docs & Math Reference)."""
    render_page_header(
        title="System Docs & Math Reference",
        subtitle="Ringkasan rumus Fuzzy Mamdani dan Fuzzy-Enhanced KNN, tabel lengkap 27 rule base, dan panduan singkat cara pakai setiap halaman.",
        chip_text="27 Rule Base · Math Spec",
    )

    c1, c2 = st.columns(2, gap="large")
    with c1:
        with st.container(border=True):
            st.subheader("1. Fuzzy Mamdani Formulas")
            st.markdown(
                """
                **a. Triangular Membership Function:**
                $$\\mu(x; a, b, c) = \\max\\left(0, \\min\\left(\\frac{x - a}{b - a}, \\frac{c - x}{c - b}\\right)\\right)$$
                dengan shoulder kiri ($a = b$) dan shoulder kanan ($b = c$) sehingga $\\sum \\mu(x) = 1$.

                **b. Rule Evaluation & AND Operator (Min):**
                $$\\alpha_k = \\min\\left(\\mu_{A_k}(X_1),\\; \\mu_{B_k}(X_2),\\; \\mu_{C_k}(X_3)\\right), \\quad k = 1, 2, \\dots, 27$$

                **c. Mamdani Implication (MIN) & Aggregation (MAX):**
                $$\\mu_{\\text{agg}}(z) = \\max_{k=1..27} \\min\\left(\\alpha_k,\\; \\mu_{\\text{out}, k}(z)\\right)$$

                **d. Analytic Centroid Defuzzification:**
                $$z^* = \\frac{\\int_{0}^{100} z \\cdot \\mu_{\\text{agg}}(z)\\,dz}{\\int_{0}^{100} \\mu_{\\text{agg}}(z)\\,dz} = \\frac{\\sum_{i} M_i}{\\sum_{i} A_i}$$
                """
            )

    with c2:
        with st.container(border=True):
            st.subheader("2. Fuzzy-Enhanced KNN Formulas")
            st.markdown(
                """
                **a. Leakage-Free Min-Max Scaling (Fit on Train):**
                $$x'_{ij} = \\frac{x_{ij} - \\min(X_{\\text{train}, j})}{\\max(X_{\\text{train}, j}) - \\min(X_{\\text{train}, j})}$$

                **b. Euclidean Distance in 4D Space ($[X'_1, X'_2, X'_3, Y']$):**
                $$d(x_q, x_i) = \\sqrt{\\sum_{j=1}^{4} \\left(x'_{qj} - x'_{ij}\\right)^2}$$

                **c. Majority Voting ($K$ Nearest Neighbors):**
                $$\\hat{y}_q = \\arg\\max_{c \\in \\{\\text{Not Potable, Potable}\\}} \\sum_{i \\in N_K(x_q)} \\mathbb{I}(y_i = c)$$
                Kalau hasil voting seri (tie), keputusan diambil dari rata-rata jarak Euclidean terdekat di kelas yang seri.
                """
            )

    st.divider()
    st.subheader("3. Complete 27 Rule Base (3 × 3 × 3)")
    df_rules = pd.DataFrame(RULES_27)[
        ["rule_id", "ph", "Hardness", "Turbidity", "water_quality_score", "description"]
    ].rename(
        columns={
            "rule_id": "Rule ID",
            "ph": "IF pH (X1)",
            "Hardness": "AND Hardness (X2)",
            "Turbidity": "AND Turbidity (X3)",
            "water_quality_score": "THEN Quality (Y)",
            "description": "Description",
        }
    )
    st.dataframe(df_rules, width="stretch", hide_index=True)

    st.divider()
    st.subheader("4. Quick User Guide")
    render_html(
        """
        <div class="atlas-card">
            <div class="stage-tray">
                <div class="stage-tray-head"><span class="stage-num">01</span><span class="stage-title">Dashboard</span></div>
                <p class="stage-desc">Ringkasan dataset 600 sampel bersih, alur Two-Stage Pipeline (Fuzzy Mamdani + KNN), metrik performa Model B, distribusi kelas, dan profil anggota Kelompok 1.</p>
            </div>
            <div class="stage-tray">
                <div class="stage-tray-head"><span class="stage-num">02</span><span class="stage-title">Input & Dataset</span></div>
                <p class="stage-desc">Simulasi prediksi satu sampel air (pilih preset Q* / S1-S5 atau input manual) dan atur KNN Reference Mode di Tab 1, atau upload custom CSV dan cek statistik dataset di Tab 2.</p>
            </div>
            <div class="stage-tray">
                <div class="stage-tray-head"><span class="stage-num">03</span><span class="stage-title">Step-by-Step Process</span></div>
                <p class="stage-desc">Lihat detail hitungan 4 desimal untuk sampel aktif: kurva Membership Function, tabel Fuzzification, Firing Strength 27 rule, kurva MAX Aggregation, integral Analytic Centroid, sampai Euclidean Distance KNN.</p>
            </div>
            <div class="stage-tray">
                <div class="stage-tray-head"><span class="stage-num">04</span><span class="stage-title">Classification Results</span></div>
                <p class="stage-desc">Ranking kualitas seluruh sampel berdasarkan prediksi Model B, filter kelas dan minimum Fuzzy Score, chart distribusi data, serta tombol download hasil ke CSV.</p>
            </div>
            <div class="stage-tray">
                <div class="stage-tray-head"><span class="stage-num">05</span><span class="stage-title">Model Evaluation</span></div>
                <p class="stage-desc">Perbandingan Model A (3 fitur) vs Model B (4 fitur) untuk K = 3, 5, 7, 9, 11 lengkap dengan pilihan split/scaler, chart sensitivitas K, Confusion Matrix, dan metrik per kelas.</p>
            </div>
        </div>
        """
    )
