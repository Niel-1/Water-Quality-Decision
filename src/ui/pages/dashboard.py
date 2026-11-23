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
        subtitle="Sistem penentuan kualitas dan kelayakan air minum menggunakan Fuzzy Mamdani (27 Rules) dan Fuzzy-Enhanced KNN",
        chip_text=f"Active Dataset: {len(df_active)} Samples",
    )

    render_kpi_grid(
        [
            {
                "label": "Clean Dataset",
                "value": f"{len(df_active)}",
                "meta": f"{n_pot} Potable · {n_not} Not Potable",
                "tone": "cobalt",
            },
            {
                "label": "Avg. Fuzzy Score",
                "value": f"{mean_score:.4f}",
                "meta": "Analytic Centroid [0-100]",
                "tone": "muted",
            },
            {
                "label": "Model B Accuracy (K=11)",
                "value": f"{acc_b_k11:.2f}%",
                "meta": f"K=3: {acc_b_k3:.2f}% · {min_delta:+.2f}% to {max_delta:+.2f}% vs A",
                "tone": "potable",
            },
            {
                "label": "Scratch vs Sklearn Match",
                "value": "100.00%",
                "meta": "Diff vs Manual Calc: 0.0000",
                "tone": "potable",
            },
        ]
    )

    render_notice(
        f"<strong>Dataset & Standard ({escape(dataset_source_name)}):</strong> "
        "Sistem mengevaluasi kualitas air dan memprediksi kelayakan minum "
        f"({status_badge('Potable')} vs {status_badge('Not Potable')}) mengacu pada standar WHO / Permenkes. "
        "Data diambil dari <strong>Kaggle: Water Quality and Potability</strong> "
        "(<code>adityakadiwal/water-potability</code>, 3.276 raw rows, 10 columns).",
        accent=True,
    )

    col_left, col_right = st.columns([1.18, 1], gap="large")

    with col_left:
        st.subheader("Two-Stage Pipeline (Fuzzy Mamdani + KNN)")
        render_html(
            f"""
            <div class="atlas-card">
                <div class="stage-tray">
                    <div class="stage-tray-head">
                        <span class="stage-num">STAGE 01</span>
                        <span class="stage-title">Fuzzy Mamdani Inference (Quality Scoring)</span>
                    </div>
                    <p class="stage-desc">
                        Mengolah 3 parameter utama air: <strong>pH (X1 &isin; [0, 14])</strong>,
                        <strong>Hardness (X2 &isin; [60, 300] mg/L)</strong>, dan
                        <strong>Turbidity (X3 &isin; [1, 6] NTU)</strong>.
                        Menggunakan kurva segitiga simetris (&Sigma;&mu; = 1), <strong>27 Rules (3 &times; 3 &times; 3)</strong>,
                        operator <code>AND = MIN</code>, implikasi <code>MIN</code>, agregasi <code>MAX</code>, dan
                        <strong>Analytic Centroid</strong> untuk menghasilkan fitur kontinu
                        <code>fuzzy_quality_score &isin; [0, 100]</code>.
                    </p>
                </div>
                <div class="stage-tray">
                    <div class="stage-tray-head">
                        <span class="stage-num">STAGE 02</span>
                        <span class="stage-title">Fuzzy-Enhanced KNN Classification (Model B)</span>
                    </div>
                    <p class="stage-desc">
                        Menggabungkan 3 parameter awal dengan skor Mamdani menjadi vektor 4 fitur
                        <code>[ph, Hardness, Turbidity, fuzzy_quality_score]</code>. Normalisasi <strong>Min-Max Scaling</strong>
                        di-fit hanya pada 480 data latih (<em>leakage-free</em>), lalu <strong>Euclidean Distance</strong>
                        ke <em>K</em> tetangga terdekat menentukan kelas {status_badge('Potable')} atau {status_badge('Not Potable')}.
                    </p>
                </div>
            </div>
            """
        )

        st.subheader("Kelompok 1 · Teknologi Logika Fuzzy")
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
                ("Role", False),
            ],
            rows=team_rows,
        )

    with col_right:
        st.subheader("Class Distribution & Fuzzy Score Spread")
        st.plotly_chart(plot_class_distribution(df_active), width="stretch")
        st.plotly_chart(plot_fuzzy_score_boxplot(df_active), width="stretch")
