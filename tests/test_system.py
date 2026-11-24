"""
Unit Tests untuk Water Quality & Potability Decision Support System
Kelompok 1 - Teknologi Logika Fuzzy, Informatika Universitas Udayana
"""

import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.fuzzy_mamdani import (
    triangular_mf,
    RULES_27,
    fuzzify_inputs,
    compute_fuzzy_mamdani,
    batch_fuzzy_quality_scores,
)
from src.knn_model import (
    CLASS_ORDER,
    MinMaxScalerScratch,
    ZScoreScalerScratch,
    KNNClassifierScratch,
    compute_classification_metrics,
    run_head_to_head_evaluation,
)


def test_triangular_mf_boundary_and_midpoints():
    # ph: Acidic (0, 0, 7), Neutral (0, 7, 14), Alkaline (7, 14, 14)
    assert triangular_mf(0.0, 0.0, 0.0, 7.0) == 1.0
    assert abs(triangular_mf(3.5, 0.0, 0.0, 7.0) - 0.5) < 1e-9
    assert triangular_mf(7.0, 0.0, 0.0, 7.0) == 0.0

    assert triangular_mf(0.0, 0.0, 7.0, 14.0) == 0.0
    assert abs(triangular_mf(3.5, 0.0, 7.0, 14.0) - 0.5) < 1e-9
    assert triangular_mf(7.0, 0.0, 7.0, 14.0) == 1.0
    assert abs(triangular_mf(10.5, 0.0, 7.0, 14.0) - 0.5) < 1e-9
    assert triangular_mf(14.0, 0.0, 7.0, 14.0) == 0.0

    assert triangular_mf(7.0, 7.0, 14.0, 14.0) == 0.0
    assert abs(triangular_mf(10.5, 7.0, 14.0, 14.0) - 0.5) < 1e-9
    assert triangular_mf(14.0, 7.0, 14.0, 14.0) == 1.0


def test_symmetric_partition_sum_to_one():
    for ph in [0.0, 1.75, 3.5, 5.25, 7.0, 10.5, 14.0]:
        for h in [60.0, 120.0, 150.0, 180.0, 240.0, 300.0]:
            for t in [1.0, 2.25, 3.5, 4.75, 6.0]:
                fuz = fuzzify_inputs(ph, h, t)
                assert abs(sum(fuz["ph"].values()) - 1.0) < 1e-9
                assert abs(sum(fuz["Hardness"].values()) - 1.0) < 1e-9
                assert abs(sum(fuz["Turbidity"].values()) - 1.0) < 1e-9


def test_rule_base_completeness():
    assert len(RULES_27) == 27
    rule_ids = [r["rule_id"] for r in RULES_27]
    assert rule_ids[0] == "R01"
    assert rule_ids[-1] == "R27"


def test_fuzzy_mamdani_manual_calculation_identity_s4_and_qstar():
    r"""
    Memastikan perhitungan Fuzzy Mamdani analitik 100% identik (selisih 0.0000)
    dengan hitungan integral kalkulus manual per segmen:
    1) Kasus S4: ph = 7.0, Hardness = 120.0, Turbidity = 2.25
       - ph: Neutral = 1.0
       - Hardness: Soft = 0.5, Moderate = 0.5
       - Turbidity: Clear = 0.5, Moderate = 0.5
       - 4 rule aktif: R10 (0.5 -> Good), R11 (0.5 -> Good), R13 (0.5 -> Good), R14 (0.5 -> Moderate)
       - Agregasi MAX: Poor = 0.0, Moderate = 0.5, Good = 0.5
       - Segmen 1 [0, 25]: A1 = 6.25, M1 = 104.16666667
       - Segmen 2 [25, 100]: A2 = 37.50, M2 = 2343.75
       - Total Area = 43.75, Total Moment = 2447.91666667 -> Centroid = 1175 / 21 = 55.95238095
    2) Kasus Q*: ph = 5.25, Hardness = 150.0, Turbidity = 2.25
       - ph: Acidic = 0.25, Neutral = 0.75
       - Hardness: Soft = 0.25, Moderate = 0.75
       - Turbidity: Clear = 0.50, Moderate = 0.50
       - Agregasi MAX: Poor = 0.25, Moderate = 0.50, Good = 0.50
       - Segmen 1 [0, 12.5]: A1 = 3.125, M1 = 19.53125
       - Segmen 2 [12.5, 25]: A2 = 4.6875, M2 = 91.14583333
       - Segmen 3 [25, 100]: A3 = 37.50, M3 = 2343.75
       - Total Area = 45.3125, Total Moment = 2454.42708333 -> Centroid = 650 / 12 = 54.16666667
    """
    res_s4 = compute_fuzzy_mamdani(7.0, 120.0, 2.25, method="analytic")
    assert abs(res_s4["fuzzified"]["ph"]["Neutral"] - 1.0) < 1e-9
    assert abs(res_s4["fuzzified"]["Hardness"]["Soft"] - 0.5) < 1e-9
    assert abs(res_s4["fuzzified"]["Hardness"]["Moderate"] - 0.5) < 1e-9
    assert abs(res_s4["fuzzified"]["Turbidity"]["Clear"] - 0.5) < 1e-9
    assert abs(res_s4["fuzzified"]["Turbidity"]["Moderate"] - 0.5) < 1e-9
    assert len(res_s4["active_rules"]) == 4
    assert abs(res_s4["analytic"]["total_area"] - 43.75) < 1e-9
    assert abs(res_s4["analytic"]["total_moment"] - (104.16666666666667 + 2343.75)) < 1e-7
    assert abs(res_s4["water_quality_score"] - (1175.0 / 21.0)) < 1e-7

    res_q = compute_fuzzy_mamdani(5.25, 150.0, 2.25, method="analytic")
    assert abs(res_q["fuzzified"]["ph"]["Acidic"] - 0.25) < 1e-9
    assert abs(res_q["fuzzified"]["ph"]["Neutral"] - 0.75) < 1e-9
    assert abs(res_q["fuzzified"]["Hardness"]["Soft"] - 0.25) < 1e-9
    assert abs(res_q["fuzzified"]["Hardness"]["Moderate"] - 0.75) < 1e-9
    assert len(res_q["active_rules"]) == 8
    assert abs(res_q["analytic"]["total_area"] - 45.3125) < 1e-9
    assert abs(res_q["water_quality_score"] - (650.0 / 12.0)) < 1e-7


def test_knn_scratch_manual_distance_and_head_to_head():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    manual_df = pd.read_csv(os.path.join(base_dir, "data", "processed", "manual_calc_sample.csv"))
    clean_df = pd.read_csv(os.path.join(base_dir, "data", "processed", "water_potability_clean.csv"))

    X_train_raw = manual_df[["ph", "Hardness", "Turbidity", "fuzzy_quality_score"]].values
    y_train = manual_df["potability_label"].values
    ids_train = manual_df["sample_code"].values

    scaler = MinMaxScalerScratch().fit(X_train_raw)
    X_train_scaled = scaler.transform(X_train_raw)

    knn = KNNClassifierScratch(k=3).fit(
        X_train_scaled, y_train, X_train_raw=X_train_raw, train_ids=ids_train
    )
    x_query_raw = np.array([5.25, 150.0, 2.25, 54.1667])
    x_query_scaled = scaler.transform(x_query_raw.reshape(1, -1))[0]

    detail = knn.predict_single_detailed(x_query_scaled, x_query_raw=x_query_raw)
    assert detail["predicted_class"] == "Potable"
    assert detail["vote_counts"]["Potable"] == 2
    assert detail["vote_counts"]["Not Potable"] == 1
    assert detail["neighbors"][0]["sample_id"] == "S4"
    assert abs(detail["neighbors"][0]["distance"] - 0.3317) < 1e-3

    # Verify Head-to-Head Model B > Model A on all K = 3, 5, 7, 9, 11
    eval_res = run_head_to_head_evaluation(
        clean_df, k_values=[3, 5, 7, 9, 11], scaler_type="minmax", split_strategy="stratified_ordered"
    )
    for k in [3, 5, 7, 9, 11]:
        rk = eval_res["results_by_k"][k]
        assert rk["delta_accuracy"] > 0.0
        assert rk["delta_f1_macro"] > 0.0
        assert rk["sklearn_agreement_b"] == 1.0
