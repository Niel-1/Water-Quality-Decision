"""Cached dataset loaders, model evaluation cache, and single-sample inference helpers."""

from typing import Any, Dict, Tuple
import numpy as np
import pandas as pd
import streamlit as st

from src.fuzzy_mamdani import batch_fuzzy_quality_scores, compute_fuzzy_mamdani
from src.knn_model import (
    KNNClassifierScratch,
    MinMaxScalerScratch,
    run_head_to_head_evaluation,
)
from src.ui.constants import CLEAN_CSV_PATH, MANUAL_CSV_PATH


@st.cache_data(show_spinner=False)
def load_default_datasets() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load the cleaned 600-row Kaggle dataset and 5-row manual reference dataset."""
    df_clean = pd.read_csv(CLEAN_CSV_PATH)
    df_manual = pd.read_csv(MANUAL_CSV_PATH)
    return df_clean, df_manual


@st.cache_data(show_spinner=False)
def get_cached_evaluation(
    df: pd.DataFrame, scaler_type: str = "minmax", split_strategy: str = "stratified_ordered"
) -> Dict[str, Any]:
    """Run and cache the head-to-head Model A vs Model B evaluation across K=3..11."""
    return run_head_to_head_evaluation(
        df,
        k_values=[3, 5, 7, 9, 11],
        scaler_type=scaler_type,
        split_strategy=split_strategy,
    )


def evaluate_single_sample(
    ph: float,
    hardness: float,
    turbidity: float,
    k_neighbors: int,
    reference_mode: str,
    df_active: pd.DataFrame,
    df_manual: pd.DataFrame,
) -> Dict[str, Any]:
    """Run complete Fuzzy Mamdani + KNN single-sample inference for live simulator & white-box trace."""
    fuzzy_res = compute_fuzzy_mamdani(ph, hardness, turbidity, method="analytic")
    z_star = fuzzy_res["water_quality_score"]

    if reference_mode == "manual_5":
        X_tr_raw = df_manual[["ph", "Hardness", "Turbidity", "fuzzy_quality_score"]].values
        y_tr = df_manual["potability_label"].values
        ids_tr = df_manual["sample_code"].astype(str).values
        k_eff = min(int(k_neighbors), len(df_manual))
        max_rows = len(df_manual)
    else:
        eval_res = get_cached_evaluation(df_active, "minmax", "stratified_ordered")
        tr_df = eval_res["train_df"]
        X_tr_raw = tr_df[["ph", "Hardness", "Turbidity", "fuzzy_quality_score"]].values
        y_tr = tr_df["potability_label"].values
        ids_tr = tr_df["sample_id"].astype(str).values
        k_eff = int(k_neighbors)
        max_rows = k_eff

    scaler = MinMaxScalerScratch().fit(X_tr_raw)
    X_tr_scaled = scaler.transform(X_tr_raw)

    q_raw = np.array([ph, hardness, turbidity, round(z_star, 4)], dtype=float)
    q_scaled = scaler.transform(q_raw.reshape(1, -1))[0]

    knn_model = KNNClassifierScratch(k=k_eff).fit(
        X_tr_scaled, y_tr, X_train_raw=X_tr_raw, train_ids=ids_tr
    )
    knn_detail = knn_model.predict_single_detailed(q_scaled, x_query_raw=q_raw)

    knn_display = KNNClassifierScratch(k=max_rows).fit(
        X_tr_scaled, y_tr, X_train_raw=X_tr_raw, train_ids=ids_tr
    )
    neighbors_table = knn_display.predict_single_detailed(q_scaled, x_query_raw=q_raw)["neighbors"]

    return {
        "fuzzy": fuzzy_res,
        "scaler": scaler,
        "query_raw": q_raw,
        "query_scaled": q_scaled,
        "k_eff": k_eff,
        "knn_detail": knn_detail,
        "neighbors_table": neighbors_table,
    }


def process_uploaded_csv(uploaded_file) -> Tuple[pd.DataFrame, str]:
    """Validate and enrich a user-uploaded CSV with Fuzzy Mamdani scores."""
    df_up = pd.read_csv(uploaded_file)
    req_cols = ["ph", "Hardness", "Turbidity"]
    missing = sorted(set(req_cols) - set(df_up.columns))
    if missing:
        raise ValueError(
            f"Kolom wajib tidak ditemukan pada file CSV: {', '.join(missing)}. "
            "Pastikan header memuat ph, Hardness, dan Turbidity."
        )

    for col in req_cols:
        df_up[col] = pd.to_numeric(df_up[col], errors="coerce")

    df_up = df_up.dropna(subset=req_cols).reset_index(drop=True)
    if len(df_up) < 15:
        raise ValueError(
            f"Hanya ditemukan {len(df_up)} baris numerik valid. "
            "Minimal 15 baris valid diperlukan agar split 80:20 mendukung evaluasi KNN hingga K=11."
        )

    df_up["ph"] = df_up["ph"].astype(float).clip(0.0, 14.0)
    df_up["Hardness"] = df_up["Hardness"].astype(float).clip(60.0, 300.0)
    df_up["Turbidity"] = df_up["Turbidity"].astype(float).clip(1.0, 6.0)

    if "fuzzy_quality_score" not in df_up.columns:
        X_u = df_up[req_cols].values
        df_up["fuzzy_quality_score"] = np.round(batch_fuzzy_quality_scores(X_u), 4)
    else:
        scores = pd.to_numeric(df_up["fuzzy_quality_score"], errors="coerce")
        if scores.isna().any():
            computed = np.round(batch_fuzzy_quality_scores(df_up[req_cols].values), 4)
            scores = scores.fillna(pd.Series(computed, index=df_up.index))
        df_up["fuzzy_quality_score"] = scores.astype(float).clip(0.0, 100.0)

    if "sample_id" not in df_up.columns:
        df_up["sample_id"] = [f"WQP-{i + 1:04d}" for i in range(len(df_up))]
    else:
        df_up["sample_id"] = df_up["sample_id"].astype(str)

    if "Potability" not in df_up.columns:
        df_up["Potability"] = np.where(df_up["fuzzy_quality_score"] >= 47.2, 1, 0)
    else:
        pot_num = pd.to_numeric(df_up["Potability"], errors="coerce")
        fallback_pot = np.where(df_up["fuzzy_quality_score"] >= 47.2, 1, 0)
        df_up["Potability"] = np.where(pot_num.isin([0, 1]), pot_num.fillna(0).astype(int), fallback_pot)

    df_up["potability_label"] = df_up["Potability"].map({0: "Not Potable", 1: "Potable"})

    source_label = f"Uploaded CSV ({uploaded_file.name} · {len(df_up)} baris)"
    return df_up, source_label
