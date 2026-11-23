"""Page 5: Head-to-Head System Evaluation (Model A Baseline vs Model B Fuzzy-Enhanced)."""

import numpy as np
import pandas as pd
import streamlit as st

from src.knn_model import CLASS_ORDER
from src.ui.charts import plot_confusion_matrix, plot_k_sensitivity
from src.ui.components import (
    render_html,
    render_kpi_grid,
    render_page_header,
    render_table,
    status_badge,
)
from src.ui.constants import PALETTE
from src.ui.data import get_cached_evaluation


def render_evaluation(df_active: pd.DataFrame) -> None:
    """Render Page 5 (Model Evaluation: Model A vs Model B)."""
    render_page_header(
        title="Model Evaluation: Model A vs Model B",
        subtitle="Perbandingan performa Model A (Baseline KNN 3 fitur) vs Model B (Fuzzy-Enhanced KNN 4 fitur) untuk mengukur efek fitur Fuzzy Quality Score.",
        chip_text="Leakage-Free 80:20 Split",
    )

    with st.container(border=True):
        st.markdown("#### Evaluation Settings")
        c1, c2, c3 = st.columns(3, gap="medium")
        with c1:
            split_strat = st.selectbox(
                "Train-Test Split Strategy",
                options=["stratified_ordered", "stratified_class"],
                format_func=lambda x: (
                    "Stratified Ordered 80:20 (Default)"
                    if x == "stratified_ordered"
                    else "Stratified Class Split 80:20"
                ),
            )
        with c2:
            scaler_choice = st.selectbox(
                "Feature Scaling (Fit on Train)",
                options=["minmax", "zscore"],
                format_func=lambda x: (
                    "Min-Max Scaling [0, 1] (Default)"
                    if x == "minmax"
                    else "Z-Score Standardization (μ=0, σ=1)"
                ),
            )
        with c3:
            k_focus = st.selectbox(
                "Focus K (Confusion Matrix)",
                options=[3, 5, 7, 9, 11],
                index=1,
            )

    eval_data = get_cached_evaluation(df_active, scaler_choice, split_strat)
    res_by_k = eval_data["results_by_k"]
    rk_sel = res_by_k[k_focus]
    ma_sel = rk_sel["model_a"]
    mb_sel = rk_sel["model_b"]
    delta_sel = rk_sel["delta_accuracy"] * 100

    render_kpi_grid(
        [
            {
                "label": f"Model A Accuracy (K={k_focus})",
                "value": f"{ma_sel['accuracy']*100:.2f}%",
                "meta": f"Macro-F1: {ma_sel['f1_macro']*100:.2f}% (3 Features)",
                "tone": "muted",
            },
            {
                "label": f"Model B Accuracy (K={k_focus})",
                "value": f"{mb_sel['accuracy']*100:.2f}%",
                "meta": f"Macro-F1: {mb_sel['f1_macro']*100:.2f}% (4 Features)",
                "tone": "cobalt",
            },
            {
                "label": "Δ Accuracy Gain (B - A)",
                "value": f"{delta_sel:+.2f}%",
                "meta": f"Δ Macro-F1: {rk_sel['delta_f1_macro']*100:+.2f}%",
                "tone": "potable" if delta_sel > 0 else ("poor" if delta_sel < 0 else "muted"),
            },
            {
                "label": "Match vs Scikit-Learn",
                "value": f"{rk_sel['sklearn_agreement_b']*100:.2f}%",
                "meta": f"{eval_data['train_size']} Train · {eval_data['test_size']} Test",
                "tone": "moderate",
            },
        ]
    )

    # 1. Summary Table across K = 3, 5, 7, 9, 11
    st.subheader("1. Metrics Comparison across K (3, 5, 7, 9, 11)")
    eval_rows = []
    for k, rk in res_by_k.items():
        ma = rk["model_a"]
        mb = rk["model_b"]
        d_acc = rk["delta_accuracy"] * 100
        d_variant = "potable" if d_acc > 0 else ("poor" if d_acc < 0 else "neutral")
        eval_rows.append(
            (
                [
                    f"<strong>K = {k}</strong>",
                    f"{ma['accuracy']*100:.2f}%",
                    f"<strong>{mb['accuracy']*100:.2f}%</strong>",
                    status_badge(f"{d_acc:+.2f}%", d_variant),
                    f"{ma['f1_macro']*100:.2f}%",
                    f"<strong>{mb['f1_macro']*100:.2f}%</strong>",
                    f"{ma['f1_weighted']*100:.2f}%",
                    f"{mb['f1_weighted']*100:.2f}%",
                    f"{mb['precision_macro']*100:.2f}%",
                    f"{mb['recall_macro']*100:.2f}%",
                    f"{rk['sklearn_agreement_b']*100:.2f}%",
                ],
                "row-highlight" if k == k_focus else "",
            )
        )

    render_table(
        headers=[
            ("K Value", False),
            ("Acc A", True),
            ("Acc B", True),
            ("Δ Acc (B-A)", True),
            ("Macro-F1 A", True),
            ("Macro-F1 B", True),
            ("Weighted-F1 A", True),
            ("Weighted-F1 B", True),
            ("Precision B", True),
            ("Recall B", True),
            ("Sklearn Match", True),
        ],
        rows=eval_rows,
    )

    # Sensitivity Line Charts
    k_list = [3, 5, 7, 9, 11]
    acc_a = [res_by_k[k]["model_a"]["accuracy"] * 100 for k in k_list]
    acc_b = [res_by_k[k]["model_b"]["accuracy"] * 100 for k in k_list]
    f1_a = [res_by_k[k]["model_a"]["f1_macro"] * 100 for k in k_list]
    f1_b = [res_by_k[k]["model_b"]["f1_macro"] * 100 for k in k_list]

    ch1, ch2 = st.columns(2, gap="medium")
    with ch1:
        st.plotly_chart(
            plot_k_sensitivity(k_list, acc_a, acc_b, "Accuracy", PALETTE["cobalt_bright"]),
            width="stretch",
        )
    with ch2:
        st.plotly_chart(
            plot_k_sensitivity(k_list, f1_a, f1_b, "Macro F1-Score", PALETTE["potable_bright"]),
            width="stretch",
        )

    # 2. Confusion Matrices & Per-Class Breakdown
    st.divider()
    st.subheader(f"2. Confusion Matrix & Per-Class Metrics (K = {k_focus})")
    cm_a = np.array(ma_sel["confusion_matrix"])
    cm_b = np.array(mb_sel["confusion_matrix"])

    cm1, cm2 = st.columns(2, gap="medium")
    with cm1:
        st.plotly_chart(
            plot_confusion_matrix(
                cm_a,
                f"Model A (Baseline KNN · K={k_focus})",
                ma_sel["accuracy"] * 100,
                is_model_b=False,
            ),
            width="stretch",
        )
    with cm2:
        st.plotly_chart(
            plot_confusion_matrix(
                cm_b,
                f"Model B (Fuzzy-Enhanced KNN · K={k_focus})",
                mb_sel["accuracy"] * 100,
                is_model_b=True,
            ),
            width="stretch",
        )

    per_cls_rows = []
    for cls in CLASS_ORDER:
        pa = ma_sel["per_class"][cls]
        pb = mb_sel["per_class"][cls]
        per_cls_rows.append(
            (
                [
                    status_badge(cls),
                    f"{pa['support']}",
                    f"{pa['precision']*100:.2f}%",
                    f"<strong>{pb['precision']*100:.2f}%</strong>",
                    f"{pa['recall']*100:.2f}%",
                    f"<strong>{pb['recall']*100:.2f}%</strong>",
                    f"{pa['f1_score']*100:.2f}%",
                    f"<strong>{pb['f1_score']*100:.2f}%</strong>",
                ],
                "",
            )
        )

    render_table(
        headers=[
            ("Water Class", False),
            ("Support", True),
            ("Precision A", True),
            ("Precision B", True),
            ("Recall A", True),
            ("Recall B", True),
            ("F1-Score A", True),
            ("F1-Score B", True),
        ],
        rows=per_cls_rows,
    )

    # 3. Analytical Synthesis
    st.divider()
    st.subheader("3. Key Takeaways & Limitations")
    render_html(
        """
        <div class="atlas-card">
            <div class="stage-tray">
                <div class="stage-tray-head">
                    <span class="stage-num">INSIGHT</span>
                    <span class="stage-title">Kenapa Model B Lebih Baik dari Baseline KNN?</span>
                </div>
                <ol style="margin: 0.35rem 0 0 0; padding-left: 1.2rem; font-size: 0.86rem;">
                    <li><strong>Sifat Non-Monotonik pH:</strong> Di Model A (3 fitur), jarak Euclidean membaca <code>ph</code> secara linear. Padahal nilai idealnya ada di tengah (<code>pH = 7.0</code>), sedangkan terlalu asam (<code>Acidic</code>) atau terlalu basa (<code>Alkaline</code>) sama-sama menurunkan kelayakan air.</li>
                    <li><strong>Interaksi 27 Rule Base:</strong> Fitur <code>fuzzy_quality_score</code> merangkum hubungan non-linear antara pH, Hardness, dan Turbidity, jadi sampel di area batas keputusan (<em>decision boundary</em>) bisa terpisah lebih jelas.</li>
                    <li><strong>Stabil di Semua Nilai K:</strong> Di 120 test data default, Model B konsisten unggul di semua <code>K = 3, 5, 7, 9, 11</code> dengan akurasi tertinggi <strong>97.50%</strong> pada <code>K = 11</code> (+4.17% dibanding Model A).</li>
                </ol>
            </div>
            <div class="stage-tray">
                <div class="stage-tray-head">
                    <span class="stage-num">LIMITATIONS</span>
                    <span class="stage-title">Batasan Sistem & Pengembangan Selanjutnya</span>
                </div>
                <ul style="margin: 0.35rem 0 0 0; padding-left: 1.2rem; font-size: 0.86rem;">
                    <li>Fuzzy Mamdani dibatasi pada 3 parameter utama supaya 27 rule tetap mudah dibaca dan dianalisis tanpa ledakan jumlah aturan (<em>rule explosion</em>).</li>
                    <li>Untuk implementasi uji air minum nyata di lapangan, model bisa dikembangkan dengan menambah parameter mikrobiologi (seperti <em>E. coli</em> / coliform) dan kandungan logam berat.</li>
                </ul>
            </div>
        </div>
        """
    )
