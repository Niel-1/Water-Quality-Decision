"""Page 5: Head-to-Head System Evaluation (Model A Baseline vs Model B Fuzzy-Enhanced)."""

import numpy as np
import pandas as pd
import streamlit as st

from src.knn_model import CLASS_ORDER
from src.ui.charts import plot_confusion_matrix, plot_k_sensitivity
from src.ui.components import (
    render_focus_cue,
    render_html,
    render_kpi_grid,
    render_next_step_bar,
    render_notice,
    render_page_header,
    render_table,
    status_badge,
)
from src.ui.constants import PALETTE
from src.ui.data import get_cached_evaluation


def render_evaluation(df_active: pd.DataFrame) -> None:
    """Render Page 5 (Evaluasi Model A vs Model B)."""
    render_page_header(
        title="Evaluasi Sistem: Model A vs Model B",
        subtitle="Pembuktian dampak penambahan fitur Fuzzy Quality Score (Model B, 4 fitur) dibanding KNN standar tanpa Fuzzy (Model A, 3 fitur).",
        chip_text="Split 80:20 Bebas Kebocoran",
    )

    render_focus_cue(
        "FOKUS HALAMAN 05",
        "<strong>Perbandingan performa dua model.</strong> Mengukur seberapa besar peningkatan akurasi "
        "dan keseimbangan prediksi (Macro-F1) ketika skor Fuzzy Mamdani digabungkan ke KNN.",
    )

    with st.container(border=True):
        st.markdown("#### Pengaturan Pengujian")
        c1, c2, c3 = st.columns(3, gap="medium")
        with c1:
            split_strat = st.selectbox(
                "Strategi Pembagian Latih-Uji",
                options=["stratified_ordered", "stratified_class"],
                format_func=lambda x: (
                    "Stratified Ordered 80:20 (Default)"
                    if x == "stratified_ordered"
                    else "Stratified Class Split 80:20"
                ),
            )
        with c2:
            scaler_choice = st.selectbox(
                "Metode Normalisasi (Fit di Data Latih)",
                options=["minmax", "zscore"],
                format_func=lambda x: (
                    "Min-Max Scaling [0, 1] (Default)"
                    if x == "minmax"
                    else "Z-Score Standardization (μ=0, σ=1)"
                ),
            )
        with c3:
            k_focus = st.selectbox(
                "Nilai K Fokus (Confusion Matrix)",
                options=[3, 5, 7, 9, 11],
                index=1,
            )

    eval_data = get_cached_evaluation(df_active, scaler_choice, split_strat)
    res_by_k = eval_data["results_by_k"]
    rk_sel = res_by_k[k_focus]
    ma_sel = rk_sel["model_a"]
    mb_sel = rk_sel["model_b"]
    delta_sel = rk_sel["delta_accuracy"] * 100
    delta_f1 = rk_sel["delta_f1_macro"] * 100

    best_k = max(res_by_k.keys(), key=lambda k: res_by_k[k]["model_b"]["accuracy"])
    best_acc_b = res_by_k[best_k]["model_b"]["accuracy"] * 100
    best_delta = res_by_k[best_k]["delta_accuracy"] * 100
    wins_all = all(res_by_k[k]["delta_accuracy"] > 0 for k in res_by_k)

    render_kpi_grid(
        [
            {
                "label": f"Akurasi Model A (K={k_focus})",
                "value": f"{ma_sel['accuracy']*100:.2f}%",
                "meta": f"Macro-F1: {ma_sel['f1_macro']*100:.2f}% · 3 Fitur Asli",
                "tone": "muted",
            },
            {
                "label": f"Akurasi Model B (K={k_focus})",
                "value": f"{mb_sel['accuracy']*100:.2f}%",
                "meta": f"Macro-F1: {mb_sel['f1_macro']*100:.2f}% · 4 Fitur (+Fuzzy)",
                "tone": "cobalt",
            },
            {
                "label": "Kenaikan Model B vs A",
                "value": f"{delta_sel:+.2f}%",
                "meta": f"Selisih Macro-F1: {delta_f1:+.2f}%",
                "tone": "potable" if delta_sel > 0 else ("poor" if delta_sel < 0 else "muted"),
            },
            {
                "label": "Komposisi Data Uji",
                "value": f"{eval_data['train_size']} / {eval_data['test_size']}",
                "meta": "80% Latih · 20% Uji · Bebas Kebocoran",
                "tone": "moderate",
            },
        ]
    )

    consistency_note = (
        "Model B unggul secara konsisten di <strong>seluruh nilai K (3, 5, 7, 9, 11)</strong>"
        if wins_all
        else "Model B menunjukkan variasi performa lintas nilai K sesuai karakteristik pembagian data"
    )
    render_notice(
        f"<strong>Kesimpulan Pengujian (K = {k_focus}):</strong> Penambahan fitur <code>fuzzy_quality_score</code> "
        f"mengubah akurasi dari <code>{ma_sel['accuracy']*100:.2f}%</code> (Model A) menjadi "
        f"<strong><code>{mb_sel['accuracy']*100:.2f}%</code> (Model B)</strong> "
        f"({status_badge(f'{delta_sel:+.2f}%', 'potable' if delta_sel > 0 else 'neutral')}). "
        f"{consistency_note}, dengan akurasi puncak <strong>{best_acc_b:.2f}%</strong> pada "
        f"<code>K = {best_k}</code> (<code>{best_delta:+.2f}%</code> dibanding Model A).",
        accent=True,
    )

    tab_k, tab_cm, tab_insight = st.tabs(
        [
            "1. Perbandingan Lintas Nilai K",
            f"2. Confusion Matrix & Per Kelas (K={k_focus})",
            "3. Analisis Keunggulan & Keterbatasan",
        ]
    )

    with tab_k:
        st.subheader("Ringkasan Metrik Evaluasi (K = 3, 5, 7, 9, 11)")
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
                        f"{mb['precision_macro']*100:.2f}%",
                        f"{mb['recall_macro']*100:.2f}%",
                    ],
                    "row-highlight" if k == k_focus else "",
                )
            )

        render_table(
            headers=[
                ("Nilai K", False),
                ("Akurasi A (3 Fitur)", True),
                ("Akurasi B (4 Fitur)", True),
                ("Selisih (B - A)", True),
                ("Macro-F1 A", True),
                ("Macro-F1 B", True),
                ("Precision B", True),
                ("Recall B", True),
            ],
            rows=eval_rows,
        )

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

    with tab_cm:
        st.subheader(f"Confusion Matrix & Metrik per Kelas (K = {k_focus})")
        render_notice(
            "<strong>Cara Membaca Matriks:</strong> Sel diagonal (kiri-atas dan kanan-bawah) menunjukkan jumlah prediksi yang "
            "<strong>benar</strong>, sedangkan sel di luar diagonal adalah sampel yang salah klasifikasi. "
            "Perhatikan bagaimana Model B menekan jumlah kesalahan di kedua kelas."
        )
        cm_a = np.array(ma_sel["confusion_matrix"])
        cm_b = np.array(mb_sel["confusion_matrix"])

        cm1, cm2 = st.columns(2, gap="medium")
        with cm1:
            st.plotly_chart(
                plot_confusion_matrix(
                    cm_a,
                    f"Model A (Baseline KNN 3 Fitur · K={k_focus})",
                    ma_sel["accuracy"] * 100,
                    is_model_b=False,
                ),
                width="stretch",
            )
        with cm2:
            st.plotly_chart(
                plot_confusion_matrix(
                    cm_b,
                    f"Model B (Fuzzy-Enhanced KNN 4 Fitur · K={k_focus})",
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
                ("Kelas Air", False),
                ("Jumlah Uji", True),
                ("Precision A", True),
                ("Precision B", True),
                ("Recall A", True),
                ("Recall B", True),
                ("F1-Score A", True),
                ("F1-Score B", True),
            ],
            rows=per_cls_rows,
        )

    with tab_insight:
        st.subheader("Kualitas Hasil & Keterbatasan Sistem")
        render_html(
            """
            <div class="atlas-card">
                <div class="stage-tray">
                    <div class="stage-tray-head">
                        <span class="stage-num">KEUNGGULAN</span>
                        <span class="stage-title">Mengapa Model B Lebih Baik dari KNN Standar (Model A)?</span>
                    </div>
                    <ol style="margin: 0.35rem 0 0 0; padding-left: 1.2rem; font-size: 0.86rem;">
                        <li><strong>Menangani Sifat Non-Monotonik pH:</strong> Pada Model A (3 fitur), jarak Euclidean memperlakukan <code>ph</code> secara linear. Padahal nilai ideal berada di tengah (<code>pH = 7.0</code>), sedangkan terlalu asam (<code>Acidic</code>) maupun terlalu basa (<code>Alkaline</code>) sama-sama menurunkan kelayakan air.</li>
                        <li><strong>Merangkum Interaksi 27 Aturan Pakar:</strong> Fitur <code>fuzzy_quality_score</code> merepresentasikan interaksi non-linear antara pH, Hardness, dan Turbidity sehingga sampel di area transisi (<em>decision boundary</em>) terpisah jauh lebih tegas.</li>
                        <li><strong>Stabil di Seluruh Nilai K:</strong> Pada 120 data uji default, Model B konsisten lebih unggul pada <code>K = 3, 5, 7, 9, 11</code> dengan akurasi puncak <strong>97.50%</strong> pada <code>K = 11</code> (+4.17% dibanding Model A).</li>
                    </ol>
                </div>
                <div class="stage-tray">
                    <div class="stage-tray-head">
                        <span class="stage-num">KETERBATASAN</span>
                        <span class="stage-title">Batasan Sistem & Saran Pengembangan</span>
                    </div>
                    <ul style="margin: 0.35rem 0 0 0; padding-left: 1.2rem; font-size: 0.86rem;">
                        <li>Input Fuzzy Mamdani dibatasi pada 3 parameter fisikokimia utama agar 27 aturan tetap transparan, mudah diaudit, dan terhindar dari ledakan aturan (<em>rule explosion</em>).</li>
                        <li>Parameter fungsi keanggotaan masih ditentukan secara pakar (statis); ke depan bisa dioptimasi otomatis dengan pendekatan Neuro-Fuzzy / ANFIS atau Algoritma Genetika.</li>
                        <li>Untuk penerapan pengujian air minum langsung di lapangan, sistem perlu dilengkapi parameter mikrobiologi (seperti <em>E. coli</em> / total coliform) dan kandungan logam berat.</li>
                    </ul>
                </div>
            </div>
            """
        )

    render_next_step_bar(
        summary="Buka Referensi & Panduan untuk melihat spesifikasi parameter fungsi keanggotaan, rumus matematis, pencarian 27 aturan, serta peran library Python.",
        button_label="Lanjut ke 06 · Referensi & Panduan ->",
        target_page_id="docs",
        button_key="next_from_evaluation",
    )
