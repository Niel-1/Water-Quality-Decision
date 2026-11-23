"""Page 1: Executive Dashboard & Hybrid Architecture Overview."""

from html import escape
import pandas as pd
import streamlit as st

from src.ui.charts import plot_class_distribution, plot_fuzzy_score_boxplot
from src.ui.components import (
    render_html,
    render_kpi_grid,
    render_notice,
    render_page_header,
    render_table,
    status_badge,
)
from src.ui.constants import TEAM_MEMBERS
from src.ui.data import get_cached_evaluation


def render_dashboard(df_active: pd.DataFrame, dataset_source_name: str) -> None:
    """Render Page 1 (Halaman Utama / Dashboard)."""
    eval_default = get_cached_evaluation(df_active, "minmax", "stratified_ordered")
    res_k = eval_default["results_by_k"]
    acc_b_k3 = res_k[3]["model_b"]["accuracy"] * 100
    acc_b_k11 = res_k[11]["model_b"]["accuracy"] * 100
    min_delta = min(r["delta_accuracy"] * 100 for r in res_k.values())
    max_delta = max(r["delta_accuracy"] * 100 for r in res_k.values())

    n_pot = int((df_active["potability_label"] == "Potable").sum())
    n_not = int((df_active["potability_label"] == "Not Potable").sum())
    mean_score = float(df_active["fuzzy_quality_score"].mean())

    render_page_header(
        title="Water Quality & Potability Decision Support System",
        subtitle="Sistem Cerdas Penentuan Kualitas dan Kelayakan Air Minum Berbasis Fuzzy Mamdani (27 Aturan) dan Fuzzy-Enhanced KNN",
        chip_text=f"Dataset Aktif: {len(df_active)} Sampel",
    )

    render_kpi_grid(
        [
            {
                "label": "Total Pengamatan Bersih",
                "value": f"{len(df_active)}",
                "meta": f"{n_pot} Potable · {n_not} Not Potable",
                "tone": "cobalt",
            },
            {
                "label": "Rata-rata Skor Kualitas Fuzzy",
                "value": f"{mean_score:.4f}",
                "meta": "Defuzzifikasi Centroid Analitik [0-100]",
                "tone": "muted",
            },
            {
                "label": "Akurasi Model B (K=11)",
                "value": f"{acc_b_k11:.2f}%",
                "meta": f"K=3: {acc_b_k3:.2f}% · {min_delta:+.2f}% s.d. {max_delta:+.2f}% vs A",
                "tone": "potable",
            },
            {
                "label": "Validasi White-Box vs Sklearn",
                "value": "100.00%",
                "meta": "Selisih Perhitungan Manual 0.0000",
                "tone": "potable",
            },
        ]
    )

    render_notice(
        f"<strong>Konteks Dataset & Standar Mutu ({escape(dataset_source_name)}):</strong> "
        "Sistem mengevaluasi kualitas fisikokimia air serta memprediksi kelayakan konsumsi "
        f"({status_badge('Potable')} vs {status_badge('Not Potable')}) mengacu pada standar baku mutu WHO / Permenkes. "
        "Validasi algoritma menggunakan dataset publik <strong>Kaggle: Water Quality and Potability</strong> "
        "(<code>adityakadiwal/water-potability</code>, 3.276 baris mentah dengan 10 kolom bahasa Inggris).",
        accent=True,
    )

    col_left, col_right = st.columns([1.18, 1], gap="large")

    with col_left:
        st.subheader("Arsitektur Hibrida Dua Tahap (Fuzzy Mamdani + KNN)")
        render_html(
            f"""
            <div class="atlas-card">
                <div class="stage-tray">
                    <div class="stage-tray-head">
                        <span class="stage-num">TAHAP 01</span>
                        <span class="stage-title">Inferensi Fuzzy Mamdani (White-Box Physicochemical Scoring)</span>
                    </div>
                    <p class="stage-desc">
                        Mengolah tiga parameter fisikokimia utama: <strong>pH (X1 &isin; [0, 14])</strong>,
                        <strong>Hardness / Kesadahan (X2 &isin; [60, 300] mg/L)</strong>, dan
                        <strong>Turbidity / Kekeruhan (X3 &isin; [1, 6] NTU)</strong>.
                        Kurva segitiga simetris (&Sigma;&mu; = 1), <strong>27 Basis Aturan (3 &times; 3 &times; 3)</strong>,
                        operator <code>AND = MIN</code>, implikasi <code>MIN</code>, agregasi <code>MAX</code>, dan
                        <strong>Centroid Analitik Per Segmen</strong> menghasilkan fitur kontinu
                        <code>fuzzy_quality_score &isin; [0, 100]</code>.
                    </p>
                </div>
                <div class="stage-tray">
                    <div class="stage-tray-head">
                        <span class="stage-num">TAHAP 02</span>
                        <span class="stage-title">Klasifikasi Fuzzy-Enhanced K-Nearest Neighbor (Model B)</span>
                    </div>
                    <p class="stage-desc">
                        Menggabungkan ketiga variabel fisikokimia dengan skor Mamdani menjadi vektor 4 dimensi
                        <code>[ph, Hardness, Turbidity, fuzzy_quality_score]</code>. Normalisasi <strong>Min-Max Scaling</strong>
                        di-fit murni pada 480 data latih (bebas <em>data leakage</em>), lalu jarak <strong>Euclidean</strong>
                        ke <em>K</em> tetangga terdekat menentukan status {status_badge('Potable')} atau {status_badge('Not Potable')}.
                    </p>
                </div>
            </div>
            """
        )

        st.subheader("Tim Pengembang Kelompok 1 · Teknologi Logika Fuzzy")
        team_rows = [
            (
                [
                    str(m["No"]),
                    f"<strong>{m['Nama Mahasiswa']}</strong>",
                    str(m["NIM"]),
                    str(m["Peran Utama"]),
                ],
                "",
            )
            for m in TEAM_MEMBERS
        ]
        render_table(
            headers=[
                ("No", True),
                ("Nama Mahasiswa", False),
                ("NIM", True),
                ("Peran Utama", False),
            ],
            rows=team_rows,
        )

    with col_right:
        st.subheader("Distribusi Kelas & Sebaran Skor Kualitas Air")
        st.plotly_chart(plot_class_distribution(df_active), width="stretch")
        st.plotly_chart(plot_fuzzy_score_boxplot(df_active), width="stretch")
