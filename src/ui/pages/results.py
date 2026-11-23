"""Page 4: Full-Dataset Batch Classification, Quality Ranking & Export."""

import numpy as np
import pandas as pd
import streamlit as st

from src.knn_model import CLASS_ORDER, KNNClassifierScratch
from src.ui.charts import plot_physicochemical_scatter, plot_results_histogram
from src.ui.components import render_kpi_grid, render_page_header
from src.ui.data import get_cached_evaluation


def render_results(df_active: pd.DataFrame) -> None:
    """Render Page 4 (Classification Results & Ranking)."""
    render_page_header(
        title="Classification Results & Ranking",
        subtitle="Ranking kualitas air dan hasil prediksi Potable vs Not Potable untuk seluruh dataset menggunakan Fuzzy-Enhanced KNN (Model B).",
        chip_text=f"Model B · {len(df_active)} Samples",
    )

    eval_res = get_cached_evaluation(df_active, "minmax", "stratified_ordered")
    tr_df = eval_res["train_df"]
    X_tr_b = eval_res["scaler_b"].transform(
        tr_df[["ph", "Hardness", "Turbidity", "fuzzy_quality_score"]].values
    )
    y_tr = tr_df["potability_label"].values

    with st.container(border=True):
        st.markdown("#### Batch Classification Filters")
        f0, f1, f2 = st.columns([1.0, 1.4, 1.5], gap="medium")
        with f0:
            k_sel = st.selectbox(
                "KNN Neighbors (K)",
                options=[3, 5, 7, 9, 11],
                index=1,
            )
        with f1:
            filter_cls = st.multiselect(
                "Filter Predicted Class",
                options=CLASS_ORDER,
                default=CLASS_ORDER,
            )
        with f2:
            min_score = st.slider(
                "Min. Fuzzy Quality Score (0-100)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=1.0,
            )

    knn_b_all = KNNClassifierScratch(k=k_sel).fit(X_tr_b, y_tr)
    X_all_b = eval_res["scaler_b"].transform(
        df_active[["ph", "Hardness", "Turbidity", "fuzzy_quality_score"]].values
    )
    preds_b = knn_b_all.predict(X_all_b)

    df_res = df_active.copy()
    df_res["predicted_potability_knn"] = preds_b
    df_res["_cls_order"] = df_res["predicted_potability_knn"].map({"Potable": 2, "Not Potable": 1})
    df_res = df_res.sort_values(
        ["_cls_order", "fuzzy_quality_score"], ascending=[False, False]
    ).reset_index(drop=True)
    df_res["quality_rank"] = np.arange(1, len(df_res) + 1)
    df_res = df_res.drop(columns=["_cls_order"])

    mask = (df_res["predicted_potability_knn"].isin(filter_cls)) & (
        df_res["fuzzy_quality_score"] >= min_score
    )
    df_filtered = df_res[mask].reset_index(drop=True)

    n_total = len(df_filtered)
    n_pot = int((df_filtered["predicted_potability_knn"] == "Potable").sum())
    n_not = int((df_filtered["predicted_potability_knn"] == "Not Potable").sum())
    avg_score = float(df_filtered["fuzzy_quality_score"].mean()) if n_total > 0 else 0.0

    render_kpi_grid(
        [
            {"label": "Filtered Samples", "value": f"{n_total}", "meta": f"dari {len(df_active)} total rows", "tone": "cobalt"},
            {"label": "Predicted Potable", "value": f"{n_pot}", "meta": "Layak Minum (Model B)", "tone": "potable"},
            {"label": "Predicted Not Potable", "value": f"{n_not}", "meta": "Tidak Layak Minum", "tone": "poor"},
            {"label": "Avg. Fuzzy Score", "value": f"{avg_score:.4f}", "meta": f"Evaluasi pada K = {k_sel}", "tone": "muted"},
        ]
    )

    if df_filtered.empty:
        st.info("Belum ada sampel yang cocok dengan filter ini. Coba turunkan minimum Fuzzy Score atau pilih kelas lain.")
        return

    display_cols = [
        c
        for c in [
            "quality_rank",
            "sample_id",
            "ph",
            "Hardness",
            "Turbidity",
            "Solids",
            "Chloramines",
            "Conductivity",
            "fuzzy_quality_score",
            "predicted_potability_knn",
            "potability_label",
        ]
        if c in df_filtered.columns
    ]
    st.dataframe(
        df_filtered[display_cols].style.format(
            {
                "ph": "{:.4f}",
                "Hardness": "{:.4f}",
                "Turbidity": "{:.4f}",
                "Solids": "{:.2f}",
                "Chloramines": "{:.4f}",
                "Conductivity": "{:.2f}",
                "fuzzy_quality_score": "{:.4f}",
            }
        ),
        width="stretch",
        hide_index=True,
    )

    csv_bytes = df_filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Results (CSV)",
        data=csv_bytes,
        file_name="hasil_kelayakan_air_fuzzy_knn_kelompok1.csv",
        mime="text/csv",
    )

    st.divider()
    g_left, g_right = st.columns(2, gap="medium")
    with g_left:
        st.plotly_chart(plot_results_histogram(df_filtered), width="stretch")
    with g_right:
        st.plotly_chart(plot_physicochemical_scatter(df_filtered), width="stretch")
