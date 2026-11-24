"""Page 6: Conceptual Reference, Variable Parameters, Interactive 27 Rule Base & User Guide."""

import streamlit as st

from src.fuzzy_mamdani import RULES_27
from src.ui.components import (
    render_focus_cue,
    render_html,
    render_next_step_bar,
    render_page_header,
    render_table,
    status_badge,
)
from src.ui.constants import LIBRARY_SPECS, VARIABLE_SPECS


def render_documentation() -> None:
    """Render Page 6 (Referensi Konsep, Parameter, Library & Panduan Sistem)."""
    render_page_header(
        title="Referensi Konsep & Panduan Sistem",
        subtitle="Dokumentasi spesifikasi variabel dan parameter kurva keanggotaan, rumus matematis, filter 27 basis aturan, fungsi library Python, serta panduan penggunaan.",
        chip_text="Dokumentasi · 27 Aturan",
    )

    render_focus_cue(
        "FOKUS HALAMAN 06",
        "<strong>Dokumentasi teknis dan panduan aplikasi.</strong> Pilih salah satu dari 4 tab di bawah "
        "untuk melihat spesifikasi parameter kurva, rumus matematis, pencarian aturan tertentu, atau peran library Python.",
    )

    tab_vars, tab_math, tab_rules, tab_guide = st.tabs(
        [
            "1. Variabel & Parameter MF",
            "2. Rumus & Konsep Integrasi",
            "3. Pencarian 27 Basis Aturan",
            "4. Library Python & Panduan Pakai",
        ]
    )

    with tab_vars:
        st.subheader("Spesifikasi Variabel Input, Output & Titik Segitiga [a, b, c]")
        var_rows = []
        for v in VARIABLE_SPECS:
            set_chips = " ".join(
                f'<code class="nowrap-code">{part.strip()}</code>'
                for part in v["Himpunan & Titik [a, b, c]"].split("·")
            )
            var_rows.append(
                (
                    [
                        f"<strong>{v['Variabel']}</strong>",
                        v["Peran"],
                        f'<code class="nowrap-code">{v["Domain"]}</code>',
                        set_chips,
                        v["Keterangan"],
                    ],
                    "",
                )
            )
        render_table(
            headers=[
                ("Variabel", False),
                ("Peran", False),
                ("Domain", False),
                ("Himpunan & Parameter [a, b, c]", False),
                ("Penjelasan Konseptual", False),
            ],
            rows=var_rows,
        )

    with tab_math:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            with st.container(border=True):
                st.subheader("Tahap 1: Rumus Fuzzy Mamdani")
                st.markdown(
                    """
                    **a. Fungsi Keanggotaan Segitiga:**
                    $$\\mu(x; a, b, c) = \\max\\left(0, \\min\\left(\\frac{x - a}{b - a}, \\frac{c - x}{c - b}\\right)\\right)$$
                    dengan bahu kiri ($a = b$) dan bahu kanan ($b = c$) sehingga partisi simetris memenuhi $\\sum \\mu(x) = 1$.

                    **b. Evaluasi Aturan & Operator AND (Min):**
                    $$\\alpha_k = \\min\\left(\\mu_{A_k}(X_1),\\; \\mu_{B_k}(X_2),\\; \\mu_{C_k}(X_3)\\right), \\quad k = 1, 2, \\dots, 27$$

                    **c. Implikasi Mamdani (MIN) & Agregasi (MAX):**
                    $$\\mu_{\\text{agg}}(z) = \\max_{k=1..27} \\min\\left(\\alpha_k,\\; \\mu_{\\text{out}, k}(z)\\right)$$

                    **d. Defuzzifikasi Centroid Analitik (Output `fuzzy_quality_score`):**
                    $$\\text{fuzzy\\_quality\\_score} = z^* = \\frac{\\int_{0}^{100} z \\cdot \\mu_{\\text{agg}}(z)\\,dz}{\\int_{0}^{100} \\mu_{\\text{agg}}(z)\\,dz} = \\frac{\\sum_{i} M_i}{\\sum_{i} A_i}$$
                    dengan luas tiap segmen $A_i = \\frac{1}{2}(z_1 - z_0)(\\mu_0 + \\mu_1)$ dan momen $M_i = \\frac{z_1 - z_0}{6}\\big(\\mu_0(2z_0 + z_1) + \\mu_1(z_0 + 2z_1)\\big)$.
                    """
                )

        with c2:
            with st.container(border=True):
                st.subheader("Tahap 2: Rumus Fuzzy-Enhanced KNN")
                st.markdown(
                    """
                    **a. Normalisasi Min-Max (Dipasangkan di Data Latih):**
                    $$x'_{ij} = \\frac{x_{ij} - \\min(X_{\\text{train}, j})}{\\max(X_{\\text{train}, j}) - \\min(X_{\\text{train}, j})}$$

                    **b. Jarak Euclidean di Ruang 4 Dimensi ($[X'_1, X'_2, X'_3, Y']$):**
                    $$d(x_q, x_i) = \\sqrt{\\sum_{j=1}^{4} \\left(x'_{qj} - x'_{ij}\\right)^2}$$

                    **c. Pemungutan Suara Mayoritas ($K$ Tetangga Terdekat):**
                    $$\\hat{y}_q = \\arg\\max_{c \\in \\{\\text{Not Potable, Potable}\\}} \\sum_{i \\in N_K(x_q)} \\mathbb{I}(y_i = c)$$
                    Jika jumlah suara seri, kelas diputuskan dari rata-rata jarak Euclidean terdekat pada kelas yang seri.
                    """
                )

    with tab_rules:
        st.subheader("Basis Aturan Lengkap 27 Aturan (3 x 3 x 3)")
        rf1, rf2 = st.columns(2, gap="medium")
        with rf1:
            filter_out = st.selectbox(
                "Filter Output Kualitas (THEN)",
                options=["Semua Output", "Good", "Moderate", "Poor"],
            )
        with rf2:
            filter_ph = st.selectbox(
                "Filter Kondisi pH (IF pH)",
                options=["Semua pH", "Acidic", "Neutral", "Alkaline"],
            )

        filtered_rules = [
            r
            for r in RULES_27
            if (filter_out == "Semua Output" or r["water_quality_score"] == filter_out)
            and (filter_ph == "Semua pH" or r["ph"] == filter_ph)
        ]

        rule_rows = [
            (
                [
                    f"<code>{r['rule_id']}</code>",
                    r["ph"],
                    r["Hardness"],
                    r["Turbidity"],
                    status_badge(r["water_quality_score"]),
                    r["description"],
                ],
                "",
            )
            for r in filtered_rules
        ]
        st.caption(f"Menampilkan {len(filtered_rules)} dari 27 aturan.")
        render_table(
            headers=[
                ("Rule ID", False),
                ("IF pH (X1)", False),
                ("AND Hardness (X2)", False),
                ("AND Turbidity (X3)", False),
                ("THEN Quality (Y)", False),
                ("Deskripsi", False),
            ],
            rows=rule_rows,
        )

    with tab_guide:
        st.subheader("Peran Setiap Library Python yang Digunakan")
        lib_rows = [
            (
                [
                    f"<strong>{lib['Library']}</strong>",
                    status_badge(lib["Kategori"], "cobalt"),
                    lib["Fungsi di Aplikasi"],
                ],
                "",
            )
            for lib in LIBRARY_SPECS
        ]
        render_table(
            headers=[
                ("Library", False),
                ("Kategori", False),
                ("Fungsi dalam Implementasi", False),
            ],
            rows=lib_rows,
        )

        st.divider()
        st.subheader("Panduan Penggunaan 6 Halaman Aplikasi")
        render_html(
            """
            <div class="atlas-card">
                <div class="stage-tray">
                    <div class="stage-tray-head"><span class="stage-num">01</span><span class="stage-title">Ringkasan Sistem</span></div>
                    <p class="stage-desc">Memuat gambaran permasalahan kualitas air minum, alur arsitektur dua tahap (Fuzzy Mamdani + KNN), statistik ringkas, dan distribusi 600 sampel seimbang.</p>
                </div>
                <div class="stage-tray">
                    <div class="stage-tray-head"><span class="stage-num">02</span><span class="stage-title">Simulasi &amp; Data</span></div>
                    <p class="stage-desc">Untuk menguji satu sampel air secara interaktif (pilih preset Q* / S1-S5 atau input manual) lalu klik <strong>Jalankan Perhitungan</strong>, atau unggah dataset CSV kustom di tab kedua.</p>
                </div>
                <div class="stage-tray">
                    <div class="stage-tray-head"><span class="stage-num">03</span><span class="stage-title">Bedah Perhitungan (1 Sampel)</span></div>
                    <p class="stage-desc">Menampilkan transparansi perhitungan 4 desimal dalam 3 tab: kurva MF &amp; 27 aturan, kurva agregasi MAX &amp; integral Centroid, serta normalisasi &amp; jarak Euclidean tetangga KNN.</p>
                </div>
                <div class="stage-tray">
                    <div class="stage-tray-head"><span class="stage-num">04</span><span class="stage-title">Hasil &amp; Ranking (600 Sampel)</span></div>
                    <p class="stage-desc">Menjalankan klasifikasi pada seluruh dataset sekaligus, menampilkan interpretasi hasil, sorotan Top 5 sampel terbaik vs 5 sampel paling berisiko, grafik sebaran, dan unduh CSV.</p>
                </div>
                <div class="stage-tray">
                    <div class="stage-tray-head"><span class="stage-num">05</span><span class="stage-title">Evaluasi Model A vs B</span></div>
                    <p class="stage-desc">Membandingkan kinerja Model B (4 fitur dengan skor Fuzzy) terhadap Model A (3 fitur tanpa Fuzzy) lintas K = 3..11 lengkap dengan Confusion Matrix, metrik per kelas, serta analisis batasan sistem.</p>
                </div>
                <div class="stage-tray">
                    <div class="stage-tray-head"><span class="stage-num">06</span><span class="stage-title">Referensi &amp; Panduan (Halaman Ini)</span></div>
                    <p class="stage-desc">Berisi spesifikasi parameter fungsi keanggotaan, rumus matematis, pencarian 27 basis aturan, daftar peran library Python, dan petunjuk penggunaan aplikasi.</p>
                </div>
            </div>
            """
        )

    render_next_step_bar(
        summary="Kembali ke halaman utama untuk melihat ringkasan arsitektur dan statistik dataset.",
        button_label="Kembali ke 01 · Ringkasan Sistem",
        target_page_id="dashboard",
        button_key="next_from_docs",
    )
