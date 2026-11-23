"""Page 6: Mathematical Specification, Complete 27 Rule Base & User Manual."""

import pandas as pd
import streamlit as st

from src.fuzzy_mamdani import RULES_27
from src.ui.components import render_html, render_page_header


def render_documentation() -> None:
    """Render Page 6 (Informasi Sistem, Landasan Matematis & Petunjuk Penggunaan)."""
    render_page_header(
        title="Informasi Sistem & Landasan Matematis",
        subtitle="Spesifikasi rumus Fuzzy Mamdani analitik, algoritma Fuzzy-Enhanced KNN, tabel lengkap 27 aturan kualitas air, dan panduan pengoperasian aplikasi.",
        chip_text="27 Rule Base · White-Box Spec",
    )

    c1, c2 = st.columns(2, gap="large")
    with c1:
        with st.container(border=True):
            st.subheader("1. Formulasi Matematis Fuzzy Mamdani")
            st.markdown(
                """
                **a. Fungsi Keanggotaan Segitiga Ruspini (Triangular MF):**
                $$\\mu(x; a, b, c) = \\max\\left(0, \\min\\left(\\frac{x - a}{b - a}, \\frac{c - x}{c - b}\\right)\\right)$$
                dengan penanganan bahu kiri ($a = b$) dan bahu kanan ($b = c$) sehingga $\\sum \\mu(x) = 1$.

                **b. Evaluasi Aturan & Operator AND (Minimum):**
                $$\\alpha_k = \\min\\left(\\mu_{A_k}(X_1),\\; \\mu_{B_k}(X_2),\\; \\mu_{C_k}(X_3)\\right), \\quad k = 1, 2, \\dots, 27$$

                **c. Implikasi Mamdani (MIN) & Agregasi Antar-Aturan (MAX):**
                $$\\mu_{\\text{agg}}(z) = \\max_{k=1..27} \\min\\left(\\alpha_k,\\; \\mu_{\\text{out}, k}(z)\\right)$$

                **d. Defuzzifikasi Centroid Analitik Per Segmen:**
                $$z^* = \\frac{\\int_{0}^{100} z \\cdot \\mu_{\\text{agg}}(z)\\,dz}{\\int_{0}^{100} \\mu_{\\text{agg}}(z)\\,dz} = \\frac{\\sum_{i} M_i}{\\sum_{i} A_i}$$
                """
            )

    with c2:
        with st.container(border=True):
            st.subheader("2. Formulasi Matematis Fuzzy-Enhanced KNN")
            st.markdown(
                """
                **a. Normalisasi Min-Max Bebas Data Leakage (Fit pada Data Latih):**
                $$x'_{ij} = \\frac{x_{ij} - \\min(X_{\\text{train}, j})}{\\max(X_{\\text{train}, j}) - \\min(X_{\\text{train}, j})}$$

                **b. Jarak Euclidean pada Ruang 4 Fitur ($[X'_1, X'_2, X'_3, Y']$):**
                $$d(x_q, x_i) = \\sqrt{\\sum_{j=1}^{4} \\left(x'_{qj} - x'_{ij}\\right)^2}$$

                **c. Majority Voting $K$ Tetangga Terdekat:**
                $$\\hat{y}_q = \\arg\\max_{c \\in \\{\\text{Not Potable, Potable}\\}} \\sum_{i \\in N_K(x_q)} \\mathbb{I}(y_i = c)$$
                Jika terjadi seri suara, keputusan dipilih berdasarkan rata-rata jarak Euclidean terdekat pada kelas yang seri.
                """
            )

    st.divider()
    st.subheader("3. Tabel Lengkap 27 Rule Base Fuzzy Mamdani (3 × 3 × 3)")
    df_rules = pd.DataFrame(RULES_27)[
        ["rule_id", "ph", "Hardness", "Turbidity", "water_quality_score", "description"]
    ].rename(
        columns={
            "rule_id": "Kode Rule",
            "ph": "IF pH (X1)",
            "Hardness": "AND Hardness (X2)",
            "Turbidity": "AND Turbidity (X3)",
            "water_quality_score": "THEN Quality (Y)",
            "description": "Deskripsi Aturan",
        }
    )
    st.dataframe(df_rules, width="stretch", hide_index=True)

    st.divider()
    st.subheader("4. Panduan Pengoperasian Aplikasi (User Manual)")
    render_html(
        """
        <div class="atlas-card">
            <div class="stage-tray">
                <div class="stage-tray-head"><span class="stage-num">01</span><span class="stage-title">Halaman Utama (Dashboard)</span></div>
                <p class="stage-desc">Ringkasan eksekutif dataset Kaggle 600 sampel bersih, arsitektur hibrida dua tahap, perbandingan performa Model B, distribusi kelas, dan profil tim pengembang Kelompok 1.</p>
            </div>
            <div class="stage-tray">
                <div class="stage-tray-head"><span class="stage-num">02</span><span class="stage-title">Input Data & Eksplorasi Dataset</span></div>
                <p class="stage-desc">Simulasikan satu sampel air (preset Q* serta S1-S5 atau angka manual) dan atur mode referensi KNN pada Tab 1, atau unggah dataset CSV kustom serta audit statistik deskriptif pada Tab 2.</p>
            </div>
            <div class="stage-tray">
                <div class="stage-tray-head"><span class="stage-num">03</span><span class="stage-title">Proses Pengolahan (White-Box Step-by-Step)</span></div>
                <p class="stage-desc">Telusuri seluruh perhitungan 4 desimal untuk sampel aktif: kurva fungsi keanggotaan, tabel fuzzifikasi, kekuatan tembak 27 aturan, grafik agregasi MAX, integral segmen Centroid eksak, hingga jarak Euclidean KNN.</p>
            </div>
            <div class="stage-tray">
                <div class="stage-tray-head"><span class="stage-num">04</span><span class="stage-title">Hasil Pengolahan & Klasifikasi Kelayakan</span></div>
                <p class="stage-desc">Peringkat kualitas seluruh dataset berdasarkan prediksi Model B, filter kelas kelayakan dan ambang skor Fuzzy, visualisasi sebaran fisikokimia, serta tombol ekspor CSV.</p>
            </div>
            <div class="stage-tray">
                <div class="stage-tray-head"><span class="stage-num">05</span><span class="stage-title">Evaluasi Sistem (Model A vs Model B)</span></div>
                <p class="stage-desc">Komparasi langsung Model A (3 fitur) dan Model B (4 fitur) di seluruh variasi K = 3, 5, 7, 9, 11, lengkap dengan opsi split/scaler, kurva sensitivitas K, Confusion Matrix berdampingan, dan metrik per kelas.</p>
            </div>
        </div>
        """
    )
