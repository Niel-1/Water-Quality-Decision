"""Page 2: Single-Sample Water Simulator, Presets & Kaggle Dataset Explorer."""

import pandas as pd
import streamlit as st

from src.ui.components import (
    render_focus_cue,
    render_html,
    render_kpi_grid,
    render_next_step_bar,
    render_notice,
    render_page_header,
    render_physicochemical_strip,
    render_table,
    status_badge,
)
from src.ui.constants import REFERENCE_MODES, SAMPLE_PRESETS, VARIABLE_SPECS
from src.ui.data import evaluate_single_sample, process_uploaded_csv


def _validate_manual_inputs(ph: float, hardness: float, turbidity: float) -> list[str]:
    """Validate manual physicochemical inputs against the Fuzzy Mamdani domain."""
    errors = []
    if not (0.0 <= ph <= 14.0):
        errors.append(f"pH ({ph:.2f}) di luar domain valid 0.00 - 14.00.")
    if not (60.0 <= hardness <= 300.0):
        errors.append(f"Hardness ({hardness:.2f} mg/L) di luar domain valid 60.00 - 300.00 mg/L.")
    if not (1.0 <= turbidity <= 6.0):
        errors.append(f"Turbidity ({turbidity:.4f} NTU) di luar domain valid 1.0000 - 6.0000 NTU.")
    return errors


def render_input_dataset(
    df_default: pd.DataFrame, df_active: pd.DataFrame, df_manual: pd.DataFrame
) -> None:
    """Render Page 2 (Simulasi Sampel Tunggal & Eksplorasi Dataset)."""
    render_page_header(
        title="Simulasi Sampel & Eksplorasi Dataset",
        subtitle="Masukkan parameter 1 sampel air (preset Q* / S1-S5 atau input manual) untuk dijalankan, atau unggah dataset CSV kustom.",
        chip_text=f"Dataset Aktif: {len(df_active)} Sampel",
    )

    render_focus_cue(
        "FOKUS HALAMAN 02",
        "<strong>Input data & uji coba interaktif.</strong> Nilai yang dijalankan di sini otomatis menjadi sampel aktif "
        "yang akan dibedah langkah demi langkah di <strong>Halaman 03</strong>.",
    )

    tab_sim, tab_data = st.tabs(
        [
            "Simulasi 1 Sampel (Preset & Input Manual)",
            "Eksplorasi Dataset & Unggah CSV",
        ]
    )

    with tab_sim:
        inp = st.session_state["manual_input"]
        preset_labels = list(SAMPLE_PRESETS.keys())

        if "sim_preset" not in st.session_state:
            st.session_state["sim_preset"] = preset_labels[0]
        if "sim_form_ph" not in st.session_state:
            st.session_state["sim_form_ph"] = float(inp["ph"])
            st.session_state["sim_form_hard"] = float(inp["Hardness"])
            st.session_state["sim_form_turb"] = float(inp["Turbidity"])

        def _on_preset_change() -> None:
            choice = st.session_state["sim_preset"]
            vals = SAMPLE_PRESETS[choice]
            if vals is not None:
                st.session_state["sim_form_ph"] = float(vals[0])
                st.session_state["sim_form_hard"] = float(vals[1])
                st.session_state["sim_form_turb"] = float(vals[2])

        with st.container(border=True):
            st.markdown("#### 1. Pilih Preset Sampel (Opsional)")
            st.selectbox(
                "Muat otomatis parameter dari sampel acuan laporan (Q* / S1-S5)",
                options=preset_labels,
                key="sim_preset",
                on_change=_on_preset_change,
                help="Memilih preset akan mengisi angka pH, Hardness, dan Turbidity ke formulir di bawah.",
            )

        with st.form("single_sample_form", border=True):
            st.markdown("#### 2. Parameter Sampel Air & Pengaturan KNN")
            c1, c2, c3 = st.columns(3, gap="medium")
            with c1:
                in_ph = st.number_input(
                    "pH · Rentang 0.0 - 14.0 (Ideal WHO 6.5 - 8.5)",
                    value=float(st.session_state["sim_form_ph"]),
                    step=0.25,
                    format="%.2f",
                    help="Tingkat keasaman/kebasaan air dalam skala pH 0 sampai 14.",
                )
            with c2:
                in_hard = st.number_input(
                    "Hardness · Rentang 60 - 300 mg/L",
                    value=float(st.session_state["sim_form_hard"]),
                    step=5.0,
                    format="%.2f",
                    help="Kandungan kesadahan mineral (mg/L).",
                )
            with c3:
                in_turb = st.number_input(
                    "Turbidity · Rentang 1.0 - 6.0 NTU",
                    value=float(st.session_state["sim_form_turb"]),
                    step=0.125,
                    format="%.4f",
                    help="Tingkat kekeruhan air dalam Nephelometric Turbidity Units (NTU).",
                )

            c4, c5 = st.columns([1.35, 1], gap="large")
            with c4:
                mode_keys = list(REFERENCE_MODES.keys())
                cur_mode = inp.get("reference_mode", "manual_5")
                mode_idx = mode_keys.index(cur_mode) if cur_mode in mode_keys else 0
                ref_mode = st.radio(
                    "Data Referensi Tetangga KNN",
                    options=mode_keys,
                    index=mode_idx,
                    format_func=lambda k: REFERENCE_MODES[k],
                    horizontal=True,
                )
            with c5:
                k_val = st.select_slider(
                    "Jumlah Tetangga Terdekat (K)",
                    options=[3, 5, 7, 9, 11],
                    value=int(inp.get("k_neighbors", 3)),
                )

            submitted = st.form_submit_button(
                "Jalankan Perhitungan (Fuzzy Mamdani + KNN)",
                type="primary",
                width="stretch",
            )

        validation_errors = []
        if submitted:
            st.session_state["sim_form_ph"] = float(in_ph)
            st.session_state["sim_form_hard"] = float(in_hard)
            st.session_state["sim_form_turb"] = float(in_turb)
            validation_errors = _validate_manual_inputs(float(in_ph), float(in_hard), float(in_turb))
            if not validation_errors:
                st.session_state["manual_input"] = {
                    "ph": float(in_ph),
                    "Hardness": float(in_hard),
                    "Turbidity": float(in_turb),
                    "k_neighbors": int(k_val),
                    "reference_mode": ref_mode,
                }
                st.session_state["sim_flash_ok"] = (
                    f"Perhitungan selesai untuk pH={float(in_ph):.2f}, "
                    f"Hardness={float(in_hard):.2f} mg/L, Turbidity={float(in_turb):.4f} NTU."
                )
                st.rerun()

        if validation_errors:
            err_lines = " ".join(f"- {msg}" for msg in validation_errors)
            st.error(
                f"Input tidak valid. Perbaiki parameter berikut lalu klik Jalankan Perhitungan lagi: {err_lines}"
            )
        elif st.session_state.get("sim_flash_ok"):
            st.success(st.session_state.pop("sim_flash_ok"))

        active = st.session_state["manual_input"]
        act_ph, act_hard, act_turb = active["ph"], active["Hardness"], active["Turbidity"]
        act_k = active["k_neighbors"]
        act_mode = active.get("reference_mode", "manual_5")

        render_physicochemical_strip(act_ph, act_hard, act_turb)

        sim = evaluate_single_sample(
            ph=act_ph,
            hardness=act_hard,
            turbidity=act_turb,
            k_neighbors=act_k,
            reference_mode=act_mode,
            df_active=df_active,
            df_manual=df_manual,
        )
        f_out = sim["fuzzy"]
        knn_det = sim["knn_detail"]
        k_eff = sim["k_eff"]
        pred_cls = knn_det["predicted_class"]
        pred_tone = "potable" if pred_cls == "Potable" else "poor"
        qual_lbl = f_out["quality_linguistic"]
        qual_tone = "potable" if qual_lbl == "Good" else ("moderate" if qual_lbl == "Moderate" else "poor")

        render_kpi_grid(
            [
                {
                    "label": "Skor Kualitas Fuzzy (z*)",
                    "value": f"{f_out['water_quality_score']:.4f}",
                    "meta": "Centroid Analitik [0 - 100]",
                    "tone": "cobalt",
                },
                {
                    "label": "Kategori Kualitas Air",
                    "value": qual_lbl,
                    "meta": "Hasil Linguistik Mamdani",
                    "tone": qual_tone,
                },
                {
                    "label": "Aturan Fuzzy Aktif",
                    "value": f"{len(f_out['active_rules'])} / 27",
                    "meta": "Operator AND = MIN · Agregasi MAX",
                    "tone": "moderate",
                },
                {
                    "label": f"Prediksi Akhir KNN (K={k_eff})",
                    "value": pred_cls,
                    "meta": f"Suara: Potable {knn_det['vote_counts'].get('Potable', 0)} · Not Potable {knn_det['vote_counts'].get('Not Potable', 0)}",
                    "tone": pred_tone,
                },
            ]
        )

        render_notice(
            f"<strong>Hasil Sampel Aktif:</strong> Input <code>[pH={act_ph:.2f}, Hardness={act_hard:.2f}, Turbidity={act_turb:.4f}]</code> "
            f"menghasilkan skor kualitas <code>z* = {f_out['water_quality_score']:.4f}</code> ({status_badge(qual_lbl)}) "
            f"dan diklasifikasikan sebagai {status_badge(pred_cls)} melalui voting <code>K = {k_eff}</code> tetangga terdekat.",
            accent=True,
        )

        with st.expander("Penjelasan Variabel, Atribut & Domain Standar", expanded=False):
            var_rows = [
                (
                    [
                        f"<strong>{v['Variabel']}</strong>",
                        v["Peran"],
                        f"<code>{v['Domain']}</code>",
                        v["Keterangan"],
                    ],
                    "",
                )
                for v in VARIABLE_SPECS
            ]
            render_table(
                headers=[
                    ("Variabel", False),
                    ("Peran dalam Sistem", False),
                    ("Domain", False),
                    ("Penjelasan", False),
                ],
                rows=var_rows,
            )

        with st.expander("Lihat 5 Sampel Referensi Manual (S1 - S5)", expanded=False):
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
            st.markdown("#### Unggah Dataset CSV Kustom (Opsional)")
            up_col, btn_col = st.columns([2.2, 1], gap="medium")
            with up_col:
                uploaded = st.file_uploader(
                    "Pilih file CSV (wajib memuat kolom ph, Hardness, dan Turbidity; minimal 15 baris valid)",
                    type=["csv"],
                )
            with btn_col:
                st.write("")
                st.write("")
                if st.button("Reset ke Dataset Default (600 Baris)", width="stretch"):
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
                    st.success(
                        f"Dataset {uploaded.name} ({len(df_up)} baris) berhasil dimuat dan skor Fuzzy Mamdani sudah dihitung."
                    )
                except Exception as exc:
                    st.error(f"Gagal memproses CSV: {exc}")

        st.markdown(f"**Sumber Data Aktif:** `{st.session_state['dataset_source_name']}`")
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

        st.subheader("Statistik Deskriptif Dataset (Presisi 4 Desimal)")
        num_cols = [
            c
            for c in ["ph", "Hardness", "Turbidity", "Solids", "Chloramines", "Conductivity", "fuzzy_quality_score"]
            if c in df_active.columns
        ]
        desc_df = df_active[num_cols].describe().T.round(4)
        st.dataframe(desc_df.style.format("{:.4f}"), width="stretch")

        st.subheader("Tahapan Preprocessing & Pembentukan Fitur")
        render_html(
            """
            <div class="atlas-card">
                <ol style="margin: 0; padding-left: 1.25rem;">
                    <li><strong>Dataset Mentah Kaggle:</strong> Mengimpor <code>data/raw/water_potability.csv</code> (3.276 baris, 10 kolom) dari <em>Kaggle Water Quality and Potability</em>.</li>
                    <li><strong>Pembersihan & Filter Domain:</strong> Menghapus nilai kosong (<code>NaN</code>) dan memfilter data ke domain kurva keanggotaan: <code>ph &isin; [0.0, 14.0]</code>, <code>Hardness &isin; [60.0, 300.0] mg/L</code>, dan <code>Turbidity &isin; [1.0, 6.0] NTU</code>.</li>
                    <li><strong>Ekstraksi Skor Fuzzy:</strong> Menghitung fitur baru <code>fuzzy_quality_score &isin; [0, 100]</code> menggunakan Fuzzy Mamdani 27 aturan dan Centroid Analitik.</li>
                    <li><strong>Pembagian Seimbang 80:20:</strong> Menyusun 600 sampel seimbang (300 Potable, 300 Not Potable) dibagi menjadi 480 data latih dan 120 data uji tanpa kebocoran skala.</li>
                </ol>
            </div>
            """
        )

    render_next_step_bar(
        summary="Bedah langkah demi langkah bagaimana sampel aktif dihitung mulai dari kurva keanggotaan, 27 aturan, integral Centroid, hingga jarak tetangga KNN.",
        button_label="Lanjut ke 03 · Bedah Perhitungan ->",
        target_page_id="whitebox",
        button_key="next_from_input",
    )
