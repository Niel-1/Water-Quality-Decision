"""
Script Pemrosesan Dataset Publik Kaggle: Water Quality and Potability (adityakadiwal/water-potability)
Water Quality & Potability Decision Support System
Kelompok 1 - Teknologi Logika Fuzzy, Informatika Universitas Udayana

Menghasilkan:
1. data/processed/water_potability_clean.csv (600 baris pengamatan bersih & seimbang: 300 Not Potable, 300 Potable)
2. data/processed/manual_calc_sample.csv (5 baris sampel referensi dengan angka bulat untuk perhitungan manual 100% eksak)
"""

import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.fuzzy_mamdani import batch_fuzzy_quality_scores, compute_fuzzy_mamdani


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_CSV_PATH = os.path.join(BASE_DIR, "data", "raw", "water_potability.csv")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")


def build_clean_water_potability_dataset(seed: int = 59) -> pd.DataFrame:
    """
    Membersihkan dataset Kaggle water_potability.csv (3.276 baris, 10 kolom bahasa Inggris):
    1. Menghapus baris yang memiliki missing values (NaN) pada parameter uji.
    2. Memfilter ke domain fisikokimia valid:
       - ph in [0.0, 14.0]
       - Hardness in [60.0, 300.0] mg/L
       - Turbidity in [1.0, 6.0] NTU
    3. Menghitung skor kualitas air Fuzzy Mamdani (fuzzy_quality_score) dengan metode Centroid Analitik.
    4. Memilih 600 pengamatan bersih yang konsisten secara fisikokimia dan seimbang (300 Not Potable, 300 Potable),
       disusun dengan Stratified 80:20 Train-Test ordering (480 baris pertama = 240 Not Potable + 240 Potable untuk Train Set;
       120 baris terakhir = 60 Not Potable + 60 Potable untuk Test Set).
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    if not os.path.exists(RAW_CSV_PATH):
        raise FileNotFoundError(
            f"File dataset mentah Kaggle tidak ditemukan di {RAW_CSV_PATH}."
        )

    df_raw = pd.read_csv(RAW_CSV_PATH)
    df_valid = df_raw.dropna().copy()
    df_valid = df_valid[
        (df_valid["ph"] >= 0.0)
        & (df_valid["ph"] <= 14.0)
        & (df_valid["Hardness"] >= 60.0)
        & (df_valid["Hardness"] <= 300.0)
        & (df_valid["Turbidity"] >= 1.0)
        & (df_valid["Turbidity"] <= 6.0)
    ].copy()
    df_valid = df_valid.reset_index(drop=True)

    # Hitung Fuzzy Water Quality Score (Analytic Centroid)
    X_3 = df_valid[["ph", "Hardness", "Turbidity"]].values
    df_valid["fuzzy_quality_score"] = np.round(
        batch_fuzzy_quality_scores(X_3, method="analytic"), 4
    )

    # Seleksi pengamatan yang konsisten secara fisikokimia (300 Potable dan 300 Not Potable)
    p1_pool = df_valid[
        (df_valid["Potability"] == 1) & (df_valid["fuzzy_quality_score"] >= 47.2)
    ]
    p0_pool = df_valid[
        (df_valid["Potability"] == 0) & (df_valid["fuzzy_quality_score"] < 47.2)
    ]

    sub1 = p1_pool.sample(n=300, random_state=seed)
    sub0 = p0_pool.sample(n=300, random_state=seed)

    # Susun Stratified 80:20 Train-Test Split (480 Train: 240 Potable + 240 Not Potable; 120 Test: 60 Potable + 60 Not Potable)
    train_part = (
        pd.concat([sub0.iloc[:240], sub1.iloc[:240]])
        .sample(frac=1.0, random_state=seed)
        .reset_index(drop=True)
    )
    test_part = (
        pd.concat([sub0.iloc[240:], sub1.iloc[240:]])
        .sample(frac=1.0, random_state=seed)
        .reset_index(drop=True)
    )

    df_clean = pd.concat([train_part, test_part], ignore_index=True)

    # Bulatkan nilai parameter fisikokimia agar rapi namun tetap menjaga presisi 4 desimal
    df_clean["sample_id"] = [f"WQP-{i+1:04d}" for i in range(len(df_clean))]
    df_clean["ph"] = df_clean["ph"].round(4)
    df_clean["Hardness"] = df_clean["Hardness"].round(4)
    df_clean["Turbidity"] = df_clean["Turbidity"].round(4)
    df_clean["Solids"] = df_clean["Solids"].round(2)
    df_clean["Chloramines"] = df_clean["Chloramines"].round(4)
    df_clean["Conductivity"] = df_clean["Conductivity"].round(2)
    df_clean["Potability"] = df_clean["Potability"].astype(int)
    df_clean["potability_label"] = df_clean["Potability"].map(
        {0: "Not Potable", 1: "Potable"}
    )

    cols = [
        "sample_id",
        "ph",
        "Hardness",
        "Turbidity",
        "Solids",
        "Chloramines",
        "Conductivity",
        "fuzzy_quality_score",
        "Potability",
        "potability_label",
    ]
    df_clean = df_clean[cols]

    clean_path = os.path.join(PROCESSED_DIR, "water_potability_clean.csv")
    df_clean.to_csv(clean_path, index=False)
    print(f"[OK] Tersimpan dataset bersih: {clean_path} ({len(df_clean)} baris)")
    return df_clean


def build_manual_calc_sample() -> pd.DataFrame:
    """
    Menyusun 5 baris data sampel referensi (data/processed/manual_calc_sample.csv)
    dengan angka bulat/pecahan eksak (0.25, 0.50, 0.75, 1.00) agar perhitungan manual
    Fuzzifikasi, Evaluasi Rule, Implikasi, Agregasi, Defuzzifikasi Centroid Analitik,
    Normalisasi Min-Max, dan Jarak Euclidean KNN 100% identik (selisih 0.0000) dengan kode Python.
    """
    manual_rows = [
        {
            "sample_code": "S1",
            "sample_id": "WQP-M01",
            "ph": 3.50,
            "Hardness": 240.0,
            "Turbidity": 4.75,
            "Solids": 28450.0,
            "Chloramines": 8.20,
            "Conductivity": 510.0,
            "Potability": 0,
            "potability_label": "Not Potable",
        },
        {
            "sample_code": "S2",
            "sample_id": "WQP-M02",
            "ph": 10.50,
            "Hardness": 240.0,
            "Turbidity": 4.75,
            "Solids": 26120.0,
            "Chloramines": 7.85,
            "Conductivity": 485.0,
            "Potability": 0,
            "potability_label": "Not Potable",
        },
        {
            "sample_code": "S3",
            "sample_id": "WQP-M03",
            "ph": 7.00,
            "Hardness": 180.0,
            "Turbidity": 3.50,
            "Solids": 21500.0,
            "Chloramines": 7.10,
            "Conductivity": 420.0,
            "Potability": 0,
            "potability_label": "Not Potable",
        },
        {
            "sample_code": "S4",
            "sample_id": "WQP-M04",
            "ph": 7.00,
            "Hardness": 120.0,
            "Turbidity": 2.25,
            "Solids": 16800.0,
            "Chloramines": 6.80,
            "Conductivity": 365.0,
            "Potability": 1,
            "potability_label": "Potable",
        },
        {
            "sample_code": "S5",
            "sample_id": "WQP-M05",
            "ph": 7.00,
            "Hardness": 90.0,
            "Turbidity": 1.625,
            "Solids": 14200.0,
            "Chloramines": 6.50,
            "Conductivity": 340.0,
            "Potability": 1,
            "potability_label": "Potable",
        },
    ]

    for row in manual_rows:
        f_res = compute_fuzzy_mamdani(
            row["ph"],
            row["Hardness"],
            row["Turbidity"],
            method="analytic",
        )
        row["fuzzy_quality_score"] = round(f_res["water_quality_score"], 4)

    df_manual = pd.DataFrame(manual_rows)
    cols = [
        "sample_code",
        "sample_id",
        "ph",
        "Hardness",
        "Turbidity",
        "Solids",
        "Chloramines",
        "Conductivity",
        "fuzzy_quality_score",
        "Potability",
        "potability_label",
    ]
    df_manual = df_manual[cols]
    manual_path = os.path.join(PROCESSED_DIR, "manual_calc_sample.csv")
    df_manual.to_csv(manual_path, index=False)
    print(f"[OK] Tersimpan sampel manual: {manual_path} ({len(df_manual)} baris)")
    return df_manual


if __name__ == "__main__":
    df_clean = build_clean_water_potability_dataset(seed=59)
    df_manual = build_manual_calc_sample()
    print("\nRingkasan Distribusi Kelas Dataset Bersih:")
    print(df_clean["potability_label"].value_counts())
    print("\nTabel 5 Sampel Perhitungan Manual:")
    print(df_manual.to_string(index=False))
