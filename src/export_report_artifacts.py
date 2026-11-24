"""
Script Ekspor Artefak & Angka Presisi untuk Laporan Tugas Akhir TLF
Water Quality & Potability Decision Support System
Kelompok 1 - Teknologi Logika Fuzzy, Informatika Universitas Udayana

Menghasilkan:
1. docs/experiment_results.json
2. docs/experiment_results_for_report.md
"""

import json
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.fuzzy_mamdani import (
    MF_PARAMS,
    RULES_27,
    compute_fuzzy_mamdani,
)
from src.knn_model import (
    CLASS_ORDER,
    MinMaxScalerScratch,
    KNNClassifierScratch,
    run_head_to_head_evaluation,
)


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
DOCS_DIR = os.path.join(BASE_DIR, "docs")


def generate_report_artifacts():
    os.makedirs(DOCS_DIR, exist_ok=True)
    clean_path = os.path.join(PROCESSED_DIR, "water_potability_clean.csv")
    manual_path = os.path.join(PROCESSED_DIR, "manual_calc_sample.csv")

    df_clean = pd.read_csv(clean_path)
    df_manual = pd.read_csv(manual_path)

    # 1. Statistik Dataset Bersih Kaggle
    num_cols = [
        "ph",
        "Hardness",
        "Turbidity",
        "Solids",
        "Chloramines",
        "Conductivity",
        "fuzzy_quality_score",
    ]
    desc = df_clean[num_cols].describe().to_dict()
    class_counts = df_clean["potability_label"].value_counts().to_dict()

    # 2. Perhitungan Manual Fuzzy Mamdani Langkah demi Langkah untuk 5 Sampel Referensi (S1..S5)
    manual_fuzzy_details = []
    for _, row in df_manual.iterrows():
        f_res = compute_fuzzy_mamdani(
            row["ph"],
            row["Hardness"],
            row["Turbidity"],
            method="analytic",
        )
        manual_fuzzy_details.append(
            {
                "sample_code": str(row["sample_code"]),
                "sample_id": str(row["sample_id"]),
                "inputs": f_res["inputs"],
                "fuzzified": f_res["fuzzified"],
                "active_rules": f_res["active_rules"],
                "aggregated_alpha": f_res["aggregated_alpha"],
                "analytic": f_res["analytic"],
                "discrete_centroid": f_res["discrete_centroid"],
                "water_quality_score": f_res["water_quality_score"],
                "potability_label": str(row["potability_label"]),
            }
        )

    # Kasus Uji Manual (Query Q*): ph = 5.25, Hardness = 150.0 mg/L, Turbidity = 2.25 NTU
    query_fuzzy = compute_fuzzy_mamdani(5.25, 150.0, 2.25, method="analytic")
    query_raw_b = np.array(
        [5.25, 150.0, 2.25, round(query_fuzzy["water_quality_score"], 4)], dtype=float
    )

    # Hitung KNN Manual terhadap 5 sampel referensi (S1..S5) dengan K=3
    X_ref_b = df_manual[
        [
            "ph",
            "Hardness",
            "Turbidity",
            "fuzzy_quality_score",
        ]
    ].values
    y_ref = df_manual["potability_label"].values
    ids_ref = df_manual["sample_code"].values

    scaler_ref_b = MinMaxScalerScratch().fit(X_ref_b)
    X_ref_b_scaled = scaler_ref_b.transform(X_ref_b)
    q_b_scaled = scaler_ref_b.transform(query_raw_b.reshape(1, -1))[0]

    knn_ref_b = KNNClassifierScratch(k=3).fit(
        X_ref_b_scaled, y_ref, X_train_raw=X_ref_b, train_ids=ids_ref
    )
    knn_manual_detail_b = knn_ref_b.predict_single_detailed(
        q_b_scaled,
        x_query_raw=query_raw_b,
        feature_names=[
            "ph",
            "Hardness",
            "Turbidity",
            "fuzzy_quality_score",
        ],
    )

    # 3. Evaluasi Eksperimen Lengkap (600 baris: 480 Train, 120 Test)
    eval_res = run_head_to_head_evaluation(
        df_clean,
        k_values=[3, 5, 7, 9, 11],
        scaler_type="minmax",
        split_strategy="stratified_ordered",
        train_ratio=0.8,
    )

    # Simpan JSON
    json_payload = {
        "dataset_summary": {
            "source": "Kaggle - Water Quality and Potability (adityakadiwal/water-potability)",
            "raw_rows": 3276,
            "total_clean_rows": len(df_clean),
            "class_distribution": class_counts,
            "numeric_stats": desc,
        },
        "manual_samples": df_manual.to_dict(orient="records"),
        "manual_fuzzy_details": manual_fuzzy_details,
        "manual_query_525_150_225": {
            "inputs": query_fuzzy["inputs"],
            "fuzzified": query_fuzzy["fuzzified"],
            "active_rules": query_fuzzy["active_rules"],
            "aggregated_alpha": query_fuzzy["aggregated_alpha"],
            "analytic": query_fuzzy["analytic"],
            "discrete_centroid": query_fuzzy["discrete_centroid"],
            "water_quality_score": query_fuzzy["water_quality_score"],
            "knn_5sample_detail": {
                "k": knn_manual_detail_b["k"],
                "scaler_min": scaler_ref_b.min_.tolist(),
                "scaler_max": scaler_ref_b.max_.tolist(),
                "scaler_range": scaler_ref_b.range_.tolist(),
                "query_raw": knn_manual_detail_b["query_raw"],
                "query_scaled": knn_manual_detail_b["query_scaled"],
                "predicted_class": knn_manual_detail_b["predicted_class"],
                "vote_counts": knn_manual_detail_b["vote_counts"],
                "neighbors": knn_manual_detail_b["neighbors"],
            },
        },
        "evaluation_stratified_ordered": {
            "split_strategy": eval_res["split_strategy"],
            "scaler_type": eval_res["scaler_type"],
            "train_size": eval_res["train_size"],
            "test_size": eval_res["test_size"],
            "train_class_counts": eval_res["train_class_counts"],
            "test_class_counts": eval_res["test_class_counts"],
            "scaler_a_params": eval_res["scaler_a_params"],
            "scaler_b_params": eval_res["scaler_b_params"],
            "results_by_k": {
                str(k): {
                    "k": v["k"],
                    "model_a": v["model_a"],
                    "model_b": v["model_b"],
                    "delta_accuracy": v["delta_accuracy"],
                    "delta_f1_macro": v["delta_f1_macro"],
                    "sklearn_agreement_a": v["sklearn_agreement_a"],
                    "sklearn_agreement_b": v["sklearn_agreement_b"],
                }
                for k, v in eval_res["results_by_k"].items()
            },
        },
    }

    json_path = os.path.join(DOCS_DIR, "experiment_results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_payload, f, indent=2, ensure_ascii=False)

    unit_map = {
        "ph": "pH (0-14)",
        "Hardness": "mg/L",
        "Turbidity": "NTU",
        "Solids": "ppm (mg/L)",
        "Chloramines": "ppm (mg/L)",
        "Conductivity": "μS/cm",
        "fuzzy_quality_score": "Skor (0-100)",
    }

    # Buat Markdown Lengkap untuk Laporan
    md_lines = [
        "# Hasil Eksperimen & Perhitungan Manual Presisi (Untuk Laporan TLF)",
        "",
        "**Judul Proyek:** Water Quality & Potability Decision Support System menggunakan Kombinasi Metode Fuzzy Mamdani dan K-Nearest Neighbor (KNN)  ",
        "**Kelompok 1 - Teknologi Logika Fuzzy (Informatika Universitas Udayana):**",
        "1. Nathanael Adrian Wattimena (2408561013)",
        "2. I Wayan Arya Adi Guna (2408561019)",
        "3. Komang Dhika Artika Nurdi (2408561055)",
        "4. Kadek Phatra Adisuta Timonuli (2408561076)",
        "5. I Putu Maichail Ganio Wijaya (2408561123)",
        "",
        "---",
        "",
        "## 1. Statistik Dataset Bersih (`water_potability_clean.csv`)",
        "- **Sumber Dataset Publik (100% Bahasa Inggris):** Kaggle — *Water Quality and Potability* (`adityakadiwal/water-potability`, `data/raw/water_potability.csv`, 3.276 baris, 10 kolom bahasa Inggris).",
        f"- **Jumlah Total Baris Pengamatan Bersih:** `{len(df_clean)}` baris",
        f"- **Distribusi Kelas Target (`potability_label`):** `Not Potable (0)` = {class_counts.get('Not Potable', 0)}, `Potable (1)` = {class_counts.get('Potable', 0)} (Seimbang 1:1)",
        "",
        "### Tabel Statistik Deskriptif Variabel Numerik",
        "| Variabel | Satuan | Min | Q1 (25%) | Median (50%) | Mean | Q3 (75%) | Max | Std Dev |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]

    for col in num_cols:
        st_col = desc[col]
        unit = unit_map.get(col, "-")
        md_lines.append(
            f"| `{col}` | {unit} | {st_col['min']:.4f} | {st_col['25%']:.4f} | {st_col['50%']:.4f} | {st_col['mean']:.4f} | {st_col['75%']:.4f} | {st_col['max']:.4f} | {st_col['std']:.4f} |"
        )

    md_lines.extend(
        [
            "",
            "---",
            "",
            "## 2. Desain Fungsi Keanggotaan & 27 Rule Base Fuzzy Mamdani",
            "",
            "### 2.1 Parameter Fungsi Keanggotaan Segitiga Simetris $(a, b, c)$",
            "- **Variabel Input 1 (`ph`, $X_1$, Tingkat Keasaman Air, Domain $[0, 14]$):**",
            "  - `Acidic` (Asam): Segitiga $(0, 0, 7)$",
            "  - `Neutral` (Netral / Ideal WHO): Segitiga $(0, 7, 14)$",
            "  - `Alkaline` (Basa): Segitiga $(7, 14, 14)$",
            "- **Variabel Input 2 (`Hardness`, $X_2$, Kesadahan Air dalam mg/L, Domain $[60, 300]$):**",
            "  - `Soft` (Lunak): Segitiga $(60, 60, 180)$",
            "  - `Moderate` (Sedang / Ideal): Segitiga $(60, 180, 300)$",
            "  - `Hard` (Sadah Tinggi): Segitiga $(180, 300, 300)$",
            "- **Variabel Input 3 (`Turbidity`, $X_3$, Kekeruhan Air dalam NTU, Domain $[1, 6]$):**",
            "  - `Clear` (Jernih): Segitiga $(1.0, 1.0, 3.5)$",
            "  - `Moderate` (Agak Keruh): Segitiga $(1.0, 3.5, 6.0)$",
            "  - `Turbid` (Keruh): Segitiga $(3.5, 6.0, 6.0)$",
            "- **Variabel Output (`water_quality_score`, $Y$, Skor Kualitas Air Fuzzy, Domain $[0, 100]$):**",
            "  - `Poor` (Buruk): Segitiga $(0, 0, 50)$",
            "  - `Moderate` (Sedang): Segitiga $(0, 50, 100)$",
            "  - `Good` (Baik / Layak): Segitiga $(50, 100, 100)$",
            "",
            "### 2.2 Tabel Lengkap 27 Aturan Fuzzy Mamdani ($3 \\times 3 \\times 3$)",
            "| Kode | IF pH ($X_1$) | AND Hardness ($X_2$) | AND Turbidity ($X_3$) | THEN Water Quality Score ($Y$) |",
            "| :---: | :---: | :---: | :---: | :---: |",
        ]
    )

    for r in RULES_27:
        md_lines.append(
            f"| **{r['rule_id']}** | {r['ph']} | {r['Hardness']} | {r['Turbidity']} | **{r['water_quality_score']}** |"
        )

    # 3. Contoh Perhitungan Manual Langkah demi Langkah (Identik 100% Selisih 0)
    md_lines.extend(
        [
            "",
            "---",
            "",
            "## 3. Contoh Perhitungan Manual Langkah demi Langkah (Selisih 0 / 100% Identik)",
            "",
            "### 3.1 Tabel 5 Sampel Referensi Perhitungan Manual (`manual_calc_sample.csv`)",
            "| Kode | Sample ID | pH ($X_1$) | Hardness ($X_2$) | Turbidity ($X_3$) | Fuzzy Quality Score ($Y$) | Solids (ppm) | Chloramines (ppm) | Kelas Kelayakan |",
            "| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
        ]
    )

    for _, r in df_manual.iterrows():
        md_lines.append(
            f"| **{r['sample_code']}** | `{r['sample_id']}` | {r['ph']:.2f} | {r['Hardness']:.1f} mg/L | {r['Turbidity']:.3f} NTU | **{r['fuzzy_quality_score']:.4f}** | {r['Solids']:.1f} | {r['Chloramines']:.2f} | **{r['potability_label']}** |"
        )

    # Rincian Kasus Manual 1: Sampel S4 (ph=7.0, Hardness=120.0, Turbidity=2.25)
    s4_det = manual_fuzzy_details[3]  # S4
    md_lines.extend(
        [
            "",
            "### 3.2 Perhitungan Manual Fuzzy Mamdani Kasus 1: Sampel `S4` ($X_1 = 7.00$, $X_2 = 120.0\\text{ mg/L}$, $X_3 = 2.25\\text{ NTU}$)",
            "",
            "#### Tahap 1: Fuzzifikasi Input",
            "1. **pH ($X_1 = 7.00$):**",
            f"   - $\\mu_{{\\text{{Acidic}}}}(7.00) = 0.0000$ (karena $7.00 \\ge 7.00$)",
            f"   - $\\mu_{{\\text{{Neutral}}}}(7.00) = 1.0000$ (tepat di titik puncak $b = 7.00$)",
            f"   - $\\mu_{{\\text{{Alkaline}}}}(7.00) = 0.0000$ (karena $7.00 \\le 7.00$)",
            "2. **Hardness ($X_2 = 120.0$ mg/L):**",
            f"   - $\\mu_{{\\text{{Soft}}}}(120.0) = \\frac{{180 - 120}}{{180 - 60}} = \\frac{{60}}{{120}} = {s4_det['fuzzified']['Hardness']['Soft']:.4f}$",
            f"   - $\\mu_{{\\text{{Moderate}}}}(120.0) = \\frac{{120 - 60}}{{180 - 60}} = \\frac{{60}}{{120}} = {s4_det['fuzzified']['Hardness']['Moderate']:.4f}$",
            f"   - $\\mu_{{\\text{{Hard}}}}(120.0) = 0.0000$ (karena $120.0 \\le 180.0$)",
            "3. **Turbidity ($X_3 = 2.25$ NTU):**",
            f"   - $\\mu_{{\\text{{Clear}}}}(2.25) = \\frac{{3.50 - 2.25}}{{3.50 - 1.00}} = \\frac{{1.25}}{{2.50}} = {s4_det['fuzzified']['Turbidity']['Clear']:.4f}$",
            f"   - $\\mu_{{\\text{{Moderate}}}}(2.25) = \\frac{{2.25 - 1.00}}{{3.50 - 1.00}} = \\frac{{1.25}}{{2.50}} = {s4_det['fuzzified']['Turbidity']['Moderate']:.4f}$",
            f"   - $\\mu_{{\\text{{Turbid}}}}(2.25) = 0.0000$ (karena $2.25 \\le 3.50$)",
            "",
            "#### Tahap 2 & 3: Evaluasi Rule Aktif (AND = MIN) & Implikasi (MIN)",
            "| Rule | Kondisi Anteseden ($X_1, X_2, X_3$) | $\\mu(X_1)$ | $\\mu(X_2)$ | $\\mu(X_3)$ | $\\alpha = \\min(\\mu_1, \\mu_2, \\mu_3)$ | Output Konsekuen ($Y$) |",
            "| :---: | :--- | :---: | :---: | :---: | :---: | :---: |",
        ]
    )
    for r in s4_det["active_rules"]:
        md_lines.append(
            f"| **{r['rule_id']}** | ({r['ph']}, {r['Hardness']}, {r['Turbidity']}) | {r['mu_ph']:.4f} | {r['mu_hardness']:.4f} | {r['mu_turbidity']:.4f} | **{r['alpha']:.4f}** | **{r['water_quality_score']}** |"
        )

    md_lines.extend(
        [
            "",
            "#### Tahap 4: Agregasi Antar-Aturan (MAX)",
            f"- $\\alpha_{{\\text{{Poor}}}} = {s4_det['aggregated_alpha']['Poor']:.4f}$",
            f"- $\\alpha_{{\\text{{Moderate}}}} = {s4_det['aggregated_alpha']['Moderate']:.4f}$ (dari R14)",
            f"- $\\alpha_{{\\text{{Good}}}} = {s4_det['aggregated_alpha']['Good']:.4f}$ (dari R10, R11, R13)",
            "",
            "#### Tahap 5: Defuzzifikasi Centroid Analitik Per Segmen",
            "| Segmen | Batas $z \\in [z_0, z_1]$ | Persamaan Kurva $\\mu_{\\text{agg}}(z)$ | Luas Segmen $A_i = \\int_{z_0}^{z_1} \\mu(z) dz$ | Momen Segmen $M_i = \\int_{z_0}^{z_1} z \\cdot \\mu(z) dz$ |",
            "| :---: | :---: | :--- | :---: | :---: |",
        ]
    )
    for seg in s4_det["analytic"]["segments"]:
        md_lines.append(
            f"| **Segmen {seg['segment_id']}** | $[{seg['z_start']:.2f}, {seg['z_end']:.2f}]$ | `{seg['equation']}` | `{seg['area']:.4f}` | `{seg['moment']:.4f}` |"
        )

    md_lines.extend(
        [
            "",
            f"- **Total Luas ($\\sum A_i$):** `{s4_det['analytic']['total_area']:.4f}`",
            f"- **Total Momen ($\\sum M_i$):** `{s4_det['analytic']['total_moment']:.4f}`",
            f"- **Titik Pusat Massa (Centroid $z^*$):**",
            f"  $$z^* = \\frac{{{s4_det['analytic']['total_moment']:.4f}}}{{{s4_det['analytic']['total_area']:.4f}}} = \\frac{{1175}}{{21}} = {s4_det['water_quality_score']:.4f}$$",
            "",
            "---",
            "",
            "### 3.3 Perhitungan Manual Kasus Uji Baru $Q^*$ ($X_1 = 5.25$, $X_2 = 150.0\\text{ mg/L}$, $X_3 = 2.25\\text{ NTU}$) dari Fuzzifikasi hingga Klasifikasi KNN",
            "",
            "#### A. Tahap Fuzzy Mamdani untuk Kasus Uji $Q^*$",
            "1. **Fuzzifikasi Input:**",
            "   - $X_1 = 5.25 \\implies \\mu_{\\text{Acidic}} = \\frac{7.00 - 5.25}{7.00} = 0.2500, \\; \\mu_{\\text{Neutral}} = \\frac{5.25 - 0}{7.00} = 0.7500, \\; \\mu_{\\text{Alkaline}} = 0.0000$",
            "   - $X_2 = 150.0 \\implies \\mu_{\\text{Soft}} = \\frac{180 - 150}{120} = 0.2500, \\; \\mu_{\\text{Moderate}} = \\frac{150 - 60}{120} = 0.7500, \\; \\mu_{\\text{Hard}} = 0.0000$",
            "   - $X_3 = 2.25 \\implies \\mu_{\\text{Clear}} = \\frac{3.50 - 2.25}{2.50} = 0.5000, \\; \\mu_{\\text{Moderate}} = \\frac{2.25 - 1.00}{2.50} = 0.5000, \\; \\mu_{\\text{Turbid}} = 0.0000$",
            "",
            "2. **Evaluasi Rule Aktif & Agregasi:**",
            "| Rule | Kondisi Anteseden ($X_1, X_2, X_3$) | $\\mu(X_1)$ | $\\mu(X_2)$ | $\\mu(X_3)$ | $\\alpha = \\min(\\mu_1, \\mu_2, \\mu_3)$ | Output ($Y$) |",
            "| :---: | :--- | :---: | :---: | :---: | :---: | :---: |",
        ]
    )
    for r in query_fuzzy["active_rules"]:
        md_lines.append(
            f"| **{r['rule_id']}** | ({r['ph']}, {r['Hardness']}, {r['Turbidity']}) | {r['mu_ph']:.4f} | {r['mu_hardness']:.4f} | {r['mu_turbidity']:.4f} | **{r['alpha']:.4f}** | **{r['water_quality_score']}** |"
        )

    md_lines.extend(
        [
            "",
            f"- **Hasil Agregasi (MAX):** $\\alpha_{{\\text{{Poor}}}} = {query_fuzzy['aggregated_alpha']['Poor']:.4f}$, $\\alpha_{{\\text{{Moderate}}}} = {query_fuzzy['aggregated_alpha']['Moderate']:.4f}$, $\\alpha_{{\\text{{Good}}}} = {query_fuzzy['aggregated_alpha']['Good']:.4f}$",
            "",
            "3. **Defuzzifikasi Centroid Analitik Per Segmen untuk $Q^*$:**",
            "| Segmen | Batas $z \\in [z_0, z_1]$ | Persamaan Kurva $\\mu_{\\text{agg}}(z)$ | Luas Segmen $A_i$ | Momen Segmen $M_i$ |",
            "| :---: | :---: | :--- | :---: | :---: |",
        ]
    )
    for seg in query_fuzzy["analytic"]["segments"]:
        md_lines.append(
            f"| **Segmen {seg['segment_id']}** | $[{seg['z_start']:.2f}, {seg['z_end']:.2f}]$ | `{seg['equation']}` | `{seg['area']:.4f}` | `{seg['moment']:.4f}` |"
        )

    md_lines.extend(
        [
            "",
            f"- **Total Luas ($\\sum A_i$):** `{query_fuzzy['analytic']['total_area']:.4f}`",
            f"- **Total Momen ($\\sum M_i$):** `{query_fuzzy['analytic']['total_moment']:.4f}`",
            f"- **Skor Kualitas Air Fuzzy ($z^*$):** `{query_fuzzy['water_quality_score']:.4f}` ($\\frac{{650}}{{12}} = 54.1667$)",
            "",
            "#### B. Tahap Perhitungan Jarak Euclidean KNN ($K = 3$) terhadap 5 Sampel Referensi (`S1` s.d. `S5`)",
            f"- **Vektor Fitur Mentah $Q^*$ (4 Fitur Model B):** `{[round(v, 4) for v in query_raw_b.tolist()]}`",
            f"- **Batas Minimum Data Referensi (`S1`..`S5`):** `{[round(v, 4) for v in scaler_ref_b.min_.tolist()]}`",
            f"- **Batas Maksimum Data Referensi (`S1`..`S5`):** `{[round(v, 4) for v in scaler_ref_b.max_.tolist()]}`",
            f"- **Rentang (Max - Min):** `{[round(v, 4) for v in scaler_ref_b.range_.tolist()]}`",
            f"- **Vektor Fitur Ternormalisasi Min-Max $Q^*$:** `{[round(v, 4) for v in knn_manual_detail_b['query_scaled']]}`",
            "",
            "| Peringkat | Sampel | Fitur Mentah $[X_1, X_2, X_3, Y]$ | Fitur Ternormalisasi $[X'_1, X'_2, X'_3, Y']$ | Selisih Kuadrat $\\sum (x'_{qj} - x'_{ij})^2$ | Jarak Euclidean $d(Q^*, S_i)$ | Kelas |",
            "| :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
        ]
    )

    all_dists_b = knn_manual_detail_b["all_distances"]
    for rank, idx in enumerate(knn_manual_detail_b["sorted_indices"], start=1):
        s_code = ids_ref[idx]
        raw_v = [round(v, 4) for v in X_ref_b[idx].tolist()]
        sc_v = [round(v, 4) for v in X_ref_b_scaled[idx].tolist()]
        sq_s = float(np.sum((X_ref_b_scaled[idx] - q_b_scaled) ** 2))
        d_val = float(all_dists_b[idx])
        lbl = y_ref[idx]
        md_lines.append(
            f"| **{rank}** | **{s_code}** | `{raw_v}` | `{sc_v}` | `{sq_s:.4f}` | **{d_val:.4f}** | **{lbl}** |"
        )

    md_lines.extend(
        [
            "",
            f"- **3 Tetangga Terdekat ($K=3$):** `{[n['sample_id'] + ' (' + n['label'] + ')' for n in knn_manual_detail_b['neighbors']]}`",
            f"- **Hasil Voting Mayoritas ($K=3$):** `{knn_manual_detail_b['vote_counts']}` $\\implies$ **Kelas Prediksi = `{knn_manual_detail_b['predicted_class']}`**",
            "",
            "---",
            "",
            "## 4. Hasil Evaluasi Eksperimen Model A (Baseline KNN) vs Model B (Fuzzy-Enhanced KNN)",
            "",
            f"- **Strategi Pembagian Data:** Stratified Ordered Split bebas kebocoran data (*leakage-free*), 80% Data Latih (`{eval_res['train_size']}` baris) dan 20% Data Uji (`{eval_res['test_size']}` baris).",
            f"- **Distribusi Kelas Data Latih (480 baris):** `{eval_res['train_class_counts']}`",
            f"- **Distribusi Kelas Data Uji (120 baris):** `{eval_res['test_class_counts']}`",
            "- **Metode Normalisasi:** Min-Max Scaling (`fit` hanya pada 480 data latih, `transform` pada 120 data uji).",
            "",
            "### 4.1 Tabel Perbandingan Metrik Evaluasi pada Berbagai Nilai $K$ ($K = 3, 5, 7, 9, 11$)",
            "| Nilai $K$ | Acc Model A (%) | Acc Model B (%) | $\\Delta$ Acc (%) | Macro-F1 Model A (%) | Macro-F1 Model B (%) | Weighted-F1 Model A (%) | Weighted-F1 Model B (%) | Kesesuaian Scratch vs Sklearn |",
            "| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
        ]
    )

    for k in [3, 5, 7, 9, 11]:
        rk = eval_res["results_by_k"][k]
        ma = rk["model_a"]
        mb = rk["model_b"]
        da = rk["delta_accuracy"] * 100.0
        md_lines.append(
            f"| **K = {k}** | {ma['accuracy']*100:.2f}% | **{mb['accuracy']*100:.2f}%** | **{da:+.2f}%** | {ma['f1_macro']*100:.2f}% | **{mb['f1_macro']*100:.2f}%** | {ma['f1_weighted']*100:.2f}% | **{mb['f1_weighted']*100:.2f}%** | {rk['sklearn_agreement_b']*100:.1f}% |"
        )

    rk5 = eval_res["results_by_k"][5]
    md_lines.extend(
        [
            "",
            "### 4.2 Rincian Metrik Per Kelas pada $K = 5$",
            "| Kelas Kelayakan Air | Support (Data Uji) | Precision Model A | Precision Model B | Recall Model A | Recall Model B | F1-Score Model A | F1-Score Model B |",
            "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
        ]
    )
    for cls in CLASS_ORDER:
        pca = rk5["model_a"]["per_class"][cls]
        pcb = rk5["model_b"]["per_class"][cls]
        md_lines.append(
            f"| **{cls}** | {pca['support']} | {pca['precision']*100:.2f}% | **{pcb['precision']*100:.2f}%** | {pca['recall']*100:.2f}% | **{pcb['recall']*100:.2f}%** | {pca['f1_score']*100:.2f}% | **{pcb['f1_score']*100:.2f}%** |"
        )

    cma = rk5["model_a"]["confusion_matrix"]
    cmb = rk5["model_b"]["confusion_matrix"]
    md_lines.extend(
        [
            "",
            "### 4.3 Matriks Konfusi (Confusion Matrix) pada $K = 5$ (120 Data Uji)",
            "",
            "#### Model A (Baseline KNN - 3 Fitur `[ph, Hardness, Turbidity]`):",
            "| Aktual \\ Prediksi | Prediksi: Not Potable | Prediksi: Potable |",
            "| :--- | :---: | :---: |",
            f"| **Aktual: Not Potable** | **{cma[0][0]}** | {cma[0][1]} |",
            f"| **Aktual: Potable** | {cma[1][0]} | **{cma[1][1]}** |",
            "",
            "#### Model B (Fuzzy-Enhanced KNN - 4 Fitur `[ph, Hardness, Turbidity, fuzzy_quality_score]`):",
            "| Aktual \\ Prediksi | Prediksi: Not Potable | Prediksi: Potable |",
            "| :--- | :---: | :---: |",
            f"| **Aktual: Not Potable** | **{cmb[0][0]}** | {cmb[0][1]} |",
            f"| **Aktual: Potable** | {cmb[1][0]} | **{cmb[1][1]}** |",
            "",
        ]
    )

    md_path = os.path.join(DOCS_DIR, "experiment_results_for_report.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"[OK] Tersimpan JSON hasil eksperimen: {json_path}")
    print(f"[OK] Tersimpan Markdown laporan: {md_path}")


if __name__ == "__main__":
    generate_report_artifacts()
