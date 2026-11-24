"""Page 4: Full-Dataset Batch Classification, Quality Ranking & Export."""

from html import escape
import numpy as np
import pandas as pd
import streamlit as st

from src.knn_model import CLASS_ORDER, KNNClassifierScratch
from src.ui.charts import plot_physicochemical_scatter, plot_results_histogram
from src.ui.components import (
    render_focus_cue,
    render_kpi_grid,
    render_next_step_bar,
    render_notice,
    render_page_header,
    render_table,
    status_badge,
)
from src.ui.data import get_cached_evaluation


def _build_highlight_rows(df_slice: pd.DataFrame) -> list:
    rows = []
    for _, r in df_slice.iterrows():
        rows.append(
            (
                [
                    f"<strong>#{int(r['quality_rank'])}</strong>",
                    f'<code class="nowrap-code">{escape(str(r["sample_id"]))}</code>',
                    f"{float(r['ph']):.2f}",
                    f"{float(r['Hardness']):.1f}",
                    f"{float(r['Turbidity']):.2f}",
                    f"<strong>{float(r['fuzzy_quality_score']):.2f}</strong>",
                    status_badge(str(r["predicted_potability_knn"])),
                ],
                "",
            )
        )
    return rows


def render_results(df_active: pd.DataFrame) -> None:
    """Render Page 4 (Hasil & Ranking Seluruh Dataset)."""
    render_page_header(
        title="Hasil Klasifikasi & Ranking Dataset",
        subtitle="Penerapan Model B (Fuzzy-Enhanced KNN) pada seluruh sampel sekaligus untuk pemeringkatan prioritas sumber air, analisis pola sebaran, dan ekspor CSV.",
        chip_text=f"Skala Batch · {len(df_active)} Sampel",
    )

    render_focus_cue(
        "BEDANYA DARI HALAMAN 03",
        "Halaman 03 membedah <strong>1 sampel aktif</strong>, sedangkan halaman ini menjalankan model ke "
        "<strong>seluruh dataset sekaligus</strong> untuk melihat sampel mana yang paling layak minum vs paling berisiko.",
    )

    eval_res = get_cached_evaluation(df_active, "minmax", "stratified_ordered")
    tr_df = eval_res["train_df"]
    X_tr_b = eval_res["scaler_b"].transform(
        tr_df[["ph", "Hardness", "Turbidity", "fuzzy_quality_score"]].values
    )
    y_tr = tr_df["potability_label"].values

    with st.container(border=True):
        st.markdown("#### Filter Tampilan Hasil Batch")
        f0, f1, f2 = st.columns([1.0, 1.4, 1.5], gap="medium")
        with f0:
            k_sel = st.selectbox(
                "Tetangga KNN (K)",
                options=[3, 5, 7, 9, 11],
                index=1,
            )
        with f1:
            filter_cls = st.multiselect(
                "Filter Kelas Prediksi",
                options=CLASS_ORDER,
                default=CLASS_ORDER,
            )
        with f2:
            min_score = st.slider(
                "Batas Minimum Skor Fuzzy (0 - 100)",
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
            {"label": "Sampel Terfilter", "value": f"{n_total}", "meta": f"dari {len(df_active)} total sampel", "tone": "cobalt"},
            {"label": "Prediksi Potable", "value": f"{n_pot}", "meta": f"{(n_pot / n_total * 100):.1f}% Layak Minum" if n_total else "0.0%", "tone": "potable"},
            {"label": "Prediksi Not Potable", "value": f"{n_not}", "meta": f"{(n_not / n_total * 100):.1f}% Tidak Layak" if n_total else "0.0%", "tone": "poor"},
            {"label": "Rata-rata Skor Fuzzy", "value": f"{avg_score:.4f}", "meta": f"Evaluasi Model B pada K = {k_sel}", "tone": "muted"},
        ]
    )

    if df_filtered.empty:
        st.info("Belum ada sampel yang cocok dengan filter ini. Coba turunkan batas minimum Skor Fuzzy atau pilih kedua kelas.")
        return

    pot_subset = df_filtered[df_filtered["predicted_potability_knn"] == "Potable"]
    not_subset = df_filtered[df_filtered["predicted_potability_knn"] == "Not Potable"]
    avg_pot = float(pot_subset["fuzzy_quality_score"].mean()) if not pot_subset.empty else None
    avg_not = float(not_subset["fuzzy_quality_score"].mean()) if not not_subset.empty else None
    top_row = df_filtered.iloc[0]
    bot_row = df_filtered.iloc[-1]

    gap_text = ""
    if avg_pot is not None and avg_not is not None:
        gap_text = (
            f" Rata-rata skor Fuzzy kelompok {status_badge('Potable')} (<code>{avg_pot:.2f}</code>) "
            f"terpaut <strong>+{avg_pot - avg_not:.2f} poin</strong> lebih tinggi dibanding "
            f"{status_badge('Not Potable')} (<code>{avg_not:.2f}</code>), menunjukkan pemisahan kualitas yang konsisten."
        )

    render_notice(
        f"<strong>Interpretasi Hasil Klasifikasi (K = {k_sel}):</strong> Dari <strong>{n_total} sampel</strong> "
        f"yang ditampilkan, <strong>{n_pot} sampel ({(n_pot / n_total * 100):.1f}%)</strong> diprediksi layak minum "
        f"dan <strong>{n_not} sampel ({(n_not / n_total * 100):.1f}%)</strong> memerlukan pengolahan lanjut.{gap_text} "
        f"Peringkat tertinggi ditempati <code>{escape(str(top_row['sample_id']))}</code> "
        f"(skor <code>{float(top_row['fuzzy_quality_score']):.2f}</code>), sedangkan yang paling berisiko "
        f"adalah <code>{escape(str(bot_row['sample_id']))}</code> "
        f"(skor <code>{float(bot_row['fuzzy_quality_score']):.2f}</code>).",
        accent=True,
    )

    tab_overview, tab_table = st.tabs(
        [
            "Ringkasan Sorotan & Grafik Sebaran",
            f"Tabel Ranking Lengkap ({n_total} Baris) & Ekspor CSV",
        ]
    )

    with tab_overview:
        st.subheader("Sorotan Sampel: Paling Layak vs Paling Berisiko")
        col_top, col_bot = st.columns(2, gap="medium")
        hl_headers = [
            ("Rank", True),
            ("ID", False),
            ("pH", True),
            ("Hard.", True),
            ("Turb.", True),
            ("Skor z*", True),
            ("Prediksi", False),
        ]
        with col_top:
            st.markdown("**Top 5 Sampel Kualitas Terbaik**")
            render_table(headers=hl_headers, rows=_build_highlight_rows(df_filtered.head(5)))
        with col_bot:
            st.markdown("**5 Sampel Paling Berisiko (Skor Terendah)**")
            bottom_5 = df_filtered.tail(5).sort_values("quality_rank", ascending=False)
            render_table(headers=hl_headers, rows=_build_highlight_rows(bottom_5))

        st.divider()
        st.subheader("Visualisasi Distribusi Skor & Sebaran Fisikokimia")
        g_left, g_right = st.columns(2, gap="medium")
        with g_left:
            st.plotly_chart(plot_results_histogram(df_filtered), width="stretch")
        with g_right:
            st.plotly_chart(plot_physicochemical_scatter(df_filtered), width="stretch")

    with tab_table:
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
            label="Unduh Hasil Ranking (CSV)",
            data=csv_bytes,
            file_name="hasil_kelayakan_air_fuzzy_knn_kelompok1.csv",
            mime="text/csv",
        )

    render_next_step_bar(
        summary="Buktikan mengapa kombinasi Fuzzy + KNN (Model B) lebih akurat dibanding KNN biasa tanpa Fuzzy (Model A) di berbagai nilai K.",
        button_label="Lanjut ke 05 · Evaluasi Model A vs B ->",
        target_page_id="evaluation",
        button_key="next_from_results",
    )
