"""Page 2: Single-Sample Water Simulator, Presets & Kaggle Dataset Explorer."""

import pandas as pd
import streamlit as st

from src.ui.components import (
    render_html,
    render_kpi_grid,
    render_notice,
    render_page_header,
    render_physicochemical_strip,
    status_badge,
)
from src.ui.constants import REFERENCE_MODES, SAMPLE_PRESETS
from src.ui.data import evaluate_single_sample, process_uploaded_csv


def render_input_dataset(
    df_default: pd.DataFrame, df_active: pd.DataFrame, df_manual: pd.DataFrame
) -> None:
    """Render Page 2 (Input & Dataset Explorer)."""
    render_page_header(
        title="Input & Dataset Explorer",
        subtitle="Test satu sampel air secara live (preset S1-S5, Q*, atau input manual), atau eksplorasi dan upload custom CSV.",
        chip_text=f"Active: {len(df_active)} Samples",
    )

    tab_sim, tab_data = st.tabs(
        [
            "Single-Sample Simulator (Preset & Manual)",
            "Dataset Explorer & Upload CSV",
        ]
    )

    with tab_sim:
        inp = st.session_state["manual_input"]

        with st.container(border=True):
            st.markdown("#### 1. Sample Preset & Water Parameters")
            preset_labels = list(SAMPLE_PRESETS.keys())
            preset_choice = st.selectbox(
                "Pilih Sample Preset (dari Laporan)",
                options=preset_labels,
                index=0,
                help="Otomatis mengisi pH, Hardness, dan Turbidity sesuai sampel acuan S1-S5 dan Q*.",
            )
            preset_vals = SAMPLE_PRESETS[preset_choice]
            if preset_vals is not None:
                def_ph, def_hard, def_turb = preset_vals
            else:
                def_ph, def_hard, def_turb = inp["ph"], inp["Hardness"], inp["Turbidity"]

            c1, c2, c3 = st.columns(3, gap="medium")
            with c1:
                in_ph = st.number_input(
                    "pH (0.0 - 14.0 · Ideal 6.5-8.5)",
                    min_value=0.0,
                    max_value=14.0,
                    value=float(def_ph),
                    step=0.25,
                    format="%.2f",
                )
            with c2:
                in_hard = st.number_input(
                    "Hardness (60 - 300 mg/L)",
                    min_value=60.0,
                    max_value=300.0,
                    value=float(def_hard),
                    step=5.0,
                    format="%.2f",
                )
            with c3:
                in_turb = st.number_input(
                    "Turbidity (1.0 - 6.0 NTU)",
                    min_value=1.0,
                    max_value=6.0,
                    value=float(def_turb),
                    step=0.125,
                    format="%.4f",
                )

            st.markdown("#### 2. Reference Data & KNN Settings")
            c4, c5 = st.columns([1.3, 1], gap="large")
            with c4:
                mode_keys = list(REFERENCE_MODES.keys())
                cur_mode = inp.get("reference_mode", "manual_5")
                mode_idx = mode_keys.index(cur_mode) if cur_mode in mode_keys else 0
                ref_mode = st.radio(
                    "KNN Reference Data",
                    options=mode_keys,
                    index=mode_idx,
                    format_func=lambda k: REFERENCE_MODES[k],
                    horizontal=True,
                )
            with c5:
                k_val = st.select_slider(
                    "Jumlah Tetangga (K)",
                    options=[3, 5, 7, 9, 11],
                    value=int(inp.get("k_neighbors", 3)),
                )

        # Persist state immediately so sidebar telemetry and Page 3 stay in sync
        st.session_state["manual_input"] = {
            "ph": float(in_ph),
            "Hardness": float(in_hard),
            "Turbidity": float(in_turb),
            "k_neighbors": int(k_val),
            "reference_mode": ref_mode,
        }

        render_physicochemical_strip(in_ph, in_hard, in_turb)

        sim = evaluate_single_sample(
            ph=in_ph,
            hardness=in_hard,
            turbidity=in_turb,
            k_neighbors=k_val,
            reference_mode=ref_mode,
            df_active=df_active,
            df_manual=df_manual,
        )
        f_out = sim["fuzzy"]
        knn_det = sim["knn_detail"]
        k_eff = sim["k_eff"]
        pred_cls = knn_det["predicted_class"]
        pred_tone = "potable" if pred_cls == "Potable" else "poor"

        render_kpi_grid(
            [
                {
                    "label": "Fuzzy Quality Score (z*)",
                    "value": f"{f_out['water_quality_score']:.4f}",
                    "meta": f"Category: {f_out['quality_linguistic']}",
                    "tone": "cobalt",
                },
                {
                    "label": f"KNN Prediction (K={k_eff})",
                    "value": pred_cls,
                    "meta": f"Votes: Potable {knn_det['vote_counts'].get('Potable', 0)} · Not Potable {knn_det['vote_counts'].get('Not Potable', 0)}",
                    "tone": pred_tone,
                },
                {
                    "label": "Active Fuzzy Rules",
                    "value": f"{len(f_out['active_rules'])} / 27",
                    "meta": "AND = MIN · Aggregation = MAX",
                    "tone": "moderate",
                },
                {
                    "label": "Discrete Centroid (Ref)",
                    "value": f"{f_out['discrete_centroid']:.4f}",
                    "meta": f"Diff vs Analytic: {abs(f_out['water_quality_score'] - f_out['discrete_centroid']):.4f}",
                    "tone": "muted",
                },
            ]
        )

        render_notice(
            f"<strong>Sample Tersimpan:</strong> Input <code>[pH={in_ph:.2f}, Hardness={in_hard:.2f}, Turbidity={in_turb:.4f}]</code> "
            f"menghasilkan <code>z* = {f_out['water_quality_score']:.4f}</code> dengan prediksi {status_badge(pred_cls)}. "
            "Buka menu <strong>03 · Step-by-Step Process</strong> di sidebar untuk melihat trace lengkap kurva MF, 27 rules, integral segmen, dan jarak Euclidean.",
            accent=True,
        )

        st.subheader("5 Manual Reference Samples (S1-S5)")
        st.dataframe(
            df_manual.style.format(
                {
                    "ph": "{:.2f}",
                    "Hardness": "{:.2f}",
                    "Turbidity": "{:.4f}",
                    "Solids": "{:.2f}",
                    "Chloramines": "{:.2f}",
                    "Conductivity": "{:.2f}",
                    "fuzzy_quality_score": "{:.4f}",
                }
            ),
            width="stretch",
            hide_index=True,
        )

    with tab_data:
        with st.container(border=True):
            st.markdown("#### Upload Custom CSV (Opsional)")
            up_col, btn_col = st.columns([2.2, 1], gap="medium")
            with up_col:
                uploaded = st.file_uploader(
                    "Pilih file CSV (wajib punya kolom ph, Hardness, Turbidity)",
                    type=["csv"],
                )
            with btn_col:
                st.write("")
                st.write("")
                if st.button("Reset ke Default Kaggle (600 Rows)", width="stretch"):
                    st.session_state["active_dataset"] = df_default.copy()
                    st.session_state["dataset_source_name"] = (
                        "Kaggle Water Potability Clean Dataset (600 Samples)"
                    )
                    st.rerun()

            if uploaded is not None:
                try:
                    df_up, src_name = process_uploaded_csv(uploaded)
                    st.session_state["active_dataset"] = df_up
                    st.session_state["dataset_source_name"] = src_name
                    df_active = df_up
                    st.success(f"Dataset {uploaded.name} ({len(df_up)} rows) berhasil dimuat dan skor Fuzzy Mamdani sudah dihitung.")
                except Exception as exc:
                    st.error(f"Gagal memproses CSV: {exc}")

        st.markdown(f"**Active Source:** `{st.session_state['dataset_source_name']}`")
        st.dataframe(
            df_active.head(50).style.format(
                {
                    "ph": "{:.4f}",
                    "Hardness": "{:.4f}",
                    "Turbidity": "{:.4f}",
                    "Solids": "{:.2f}",
                    "Chloramines": "{:.4f}",
                    "Conductivity": "{:.2f}",
                    "fuzzy_quality_score": "{:.4f}",
                },
                na_rep="-",
            ),
            width="stretch",
            hide_index=True,
        )

        st.subheader("Descriptive Statistics (4-Decimal Precision)")
        num_cols = [
            c
            for c in ["ph", "Hardness", "Turbidity", "Solids", "Chloramines", "Conductivity", "fuzzy_quality_score"]
            if c in df_active.columns
        ]
        desc_df = df_active[num_cols].describe().T.round(4)
        st.dataframe(desc_df.style.format("{:.4f}"), width="stretch")

        st.subheader("Preprocessing & Feature Engineering")
        render_html(
            """
            <div class="atlas-card">
                <ol style="margin: 0; padding-left: 1.25rem;">
                    <li><strong>Raw Dataset Kaggle:</strong> Mengimpor <code>data/raw/water_potability.csv</code> (3.276 rows, 10 columns) dari <em>Kaggle Water Quality and Potability</em>.</li>
                    <li><strong>Cleaning & Domain Filter:</strong> Menghapus nilai <code>NaN</code> dan memfilter data ke domain kurva keanggotaan: <code>ph &isin; [0.0, 14.0]</code>, <code>Hardness &isin; [60.0, 300.0] mg/L</code>, dan <code>Turbidity &isin; [1.0, 6.0] NTU</code>.</li>
                    <li><strong>Fuzzy Score Extraction:</strong> Menghitung fitur baru <code>fuzzy_quality_score &isin; [0, 100]</code> menggunakan Fuzzy Mamdani 27 rules dan Analytic Centroid.</li>
                    <li><strong>Balanced Split 80:20 (Leakage-Free):</strong> Menyusun 600 sampel seimbang (300 Potable, 300 Not Potable) dibagi jadi 480 train set dan 120 test set.</li>
                </ol>
            </div>
            """
        )
