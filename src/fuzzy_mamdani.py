"""Implementasi sistem inferensi Fuzzy Mamdani menggunakan NumPy."""

from typing import Dict, List, Tuple, Any
import numpy as np


def triangular_mf(x: float, a: float, b: float, c: float) -> float:
    """Menghitung derajat keanggotaan kurva segitiga dengan dukungan sisi siku-siku kiri dan kanan."""
    x = float(x)
    # Puncak di tepi kiri (a == b)
    if a == b:
        if x <= a:
            return 1.0 if x >= a else 0.0
        elif x >= c:
            return 0.0
        else:
            return (c - x) / (c - b)

    # Puncak di tepi kanan (b == c)
    if b == c:
        if x >= c:
            return 1.0 if x <= c else 0.0
        elif x <= a:
            return 0.0
        else:
            return (x - a) / (b - a)

    # Segitiga normal (a < b < c)
    if x <= a or x >= c:
        return 0.0
    elif x == b:
        return 1.0
    elif a < x < b:
        return (x - a) / (b - a)
    else:  # b < x < c
        return (c - x) / (c - b)


def triangular_mf_array(x_arr: np.ndarray, a: float, b: float, c: float) -> np.ndarray:
    """Versi vektorisasi dari triangular_mf untuk array NumPy."""
    return np.array([triangular_mf(val, a, b, c) for val in x_arr], dtype=float)


# Parameter kurva segitiga simetris untuk setiap variabel input dan output
MF_PARAMS = {
    "ph": {  # X1: Tingkat Keasaman Air (pH), Domain [0, 14]
        "domain": (0.0, 14.0),
        "sets": {
            "Acidic": (0.0, 0.0, 7.0),
            "Neutral": (0.0, 7.0, 14.0),
            "Alkaline": (7.0, 14.0, 14.0),
        },
    },
    "Hardness": {  # X2: Kesadahan Air (mg/L), Domain [60, 300]
        "domain": (60.0, 300.0),
        "sets": {
            "Soft": (60.0, 60.0, 180.0),
            "Moderate": (60.0, 180.0, 300.0),
            "Hard": (180.0, 300.0, 300.0),
        },
    },
    "Turbidity": {  # X3: Kekeruhan Air (NTU), Domain [1, 6]
        "domain": (1.0, 6.0),
        "sets": {
            "Clear": (1.0, 1.0, 3.5),
            "Moderate": (1.0, 3.5, 6.0),
            "Turbid": (3.5, 6.0, 6.0),
        },
    },
    "water_quality_score": {  # Y: Skor Kualitas Air Fuzzy, Domain [0, 100]
        "domain": (0.0, 100.0),
        "sets": {
            "Poor": (0.0, 0.0, 50.0),
            "Moderate": (0.0, 50.0, 100.0),
            "Good": (50.0, 100.0, 100.0),
        },
    },
}


def build_rule_base() -> List[Dict[str, Any]]:
    """Membangun 27 aturan kombinasi fuzzy (3x3x3) berdasarkan kondisi pH, kesadahan, dan kekeruhan air."""
    x1_sets = ["Acidic", "Neutral", "Alkaline"]
    x2_sets = ["Soft", "Moderate", "Hard"]
    x3_sets = ["Clear", "Moderate", "Turbid"]

    rules = []
    rule_id = 1
    for s1 in x1_sets:
        for i2, s2 in enumerate(x2_sets):
            for i3, s3 in enumerate(x3_sets):
                if s1 == "Neutral":
                    if (i2 <= 1 and i3 == 0) or (i2 == 0 and i3 == 1):
                        out = "Good"
                    elif i2 + i3 <= 2:
                        out = "Moderate"
                    else:
                        out = "Poor"
                else:  # Acidic atau Alkaline
                    if i2 + i3 <= 1:
                        out = "Moderate"
                    else:
                        out = "Poor"

                rules.append(
                    {
                        "rule_id": f"R{rule_id:02d}",
                        "rule_num": rule_id,
                        "ph": s1,
                        "Hardness": s2,
                        "Turbidity": s3,
                        "water_quality_score": out,
                        "description": (
                            f"IF ph = {s1} AND Hardness = {s2} "
                            f"AND Turbidity = {s3} THEN Water Quality = {out}"
                        ),
                    }
                )
                rule_id += 1
    return rules


RULES_27 = build_rule_base()


def fuzzify_inputs(
    ph: float, hardness: float, turbidity: float
) -> Dict[str, Dict[str, float]]:
    """Mengubah nilai input crisp menjadi derajat keanggotaan fuzzy pada masing-masing domain."""
    x1 = float(np.clip(ph, 0.0, 14.0))
    x2 = float(np.clip(hardness, 60.0, 300.0))
    x3 = float(np.clip(turbidity, 1.0, 6.0))

    mu_x1 = {
        name: triangular_mf(x1, *params)
        for name, params in MF_PARAMS["ph"]["sets"].items()
    }
    mu_x2 = {
        name: triangular_mf(x2, *params)
        for name, params in MF_PARAMS["Hardness"]["sets"].items()
    }
    mu_x3 = {
        name: triangular_mf(x3, *params)
        for name, params in MF_PARAMS["Turbidity"]["sets"].items()
    }

    return {
        "ph": mu_x1,
        "Hardness": mu_x2,
        "Turbidity": mu_x3,
    }


def evaluate_rules(
    fuzzified: Dict[str, Dict[str, float]],
) -> Tuple[List[Dict[str, Any]], Dict[str, float]]:
    """Mengevaluasi 27 aturan dengan operator MIN dan mengagregasi alpha tiap himpunan output dengan MAX."""
    evaluated_rules = []
    aggregated_alpha = {"Poor": 0.0, "Moderate": 0.0, "Good": 0.0}

    for r in RULES_27:
        mu1 = fuzzified["ph"][r["ph"]]
        mu2 = fuzzified["Hardness"][r["Hardness"]]
        mu3 = fuzzified["Turbidity"][r["Turbidity"]]
        alpha = min(mu1, mu2, mu3)

        out_set = r["water_quality_score"]
        if alpha > aggregated_alpha[out_set]:
            aggregated_alpha[out_set] = alpha

        evaluated_rules.append(
            {
                **r,
                "mu_ph": mu1,
                "mu_hardness": mu2,
                "mu_turbidity": mu3,
                "alpha": alpha,
                "is_active": alpha > 0.0,
            }
        )

    return evaluated_rules, aggregated_alpha


def aggregated_membership_at(z: float, aggregated_alpha: Dict[str, float]) -> float:
    """Menghitung nilai keanggotaan kurva agregasi Mamdani pada titik z dalam [0, 100]."""
    out_sets = MF_PARAMS["water_quality_score"]["sets"]
    m_poor = min(aggregated_alpha["Poor"], triangular_mf(z, *out_sets["Poor"]))
    m_mod = min(aggregated_alpha["Moderate"], triangular_mf(z, *out_sets["Moderate"]))
    m_good = min(aggregated_alpha["Good"], triangular_mf(z, *out_sets["Good"]))
    return max(m_poor, m_mod, m_good)


def defuzzify_centroid_analytic(
    aggregated_alpha: Dict[str, float],
) -> Dict[str, Any]:
    """Menghitung centroid secara analitik melalui integral luas dan momen per segmen linear."""
    a_p = float(aggregated_alpha.get("Poor", 0.0))
    a_m = float(aggregated_alpha.get("Moderate", 0.0))
    a_g = float(aggregated_alpha.get("Good", 0.0))

    if a_p == 0.0 and a_m == 0.0 and a_g == 0.0:
        return {
            "centroid": 0.0,
            "total_moment": 0.0,
            "total_area": 0.0,
            "segments": [],
        }

    candidate_knots = [
        0.0,
        25.0,
        50.0,
        75.0,
        100.0,
        50.0 * (1.0 - a_p),
        50.0 * a_p,
        50.0 * (1.0 - a_m),
        50.0 * a_m,
        50.0 * (2.0 - a_m),
        50.0 * (1.0 + a_m),
        50.0 * (1.0 + a_g),
        50.0 * (2.0 - a_g),
    ]
    knots = sorted(
        list(set(round(float(np.clip(k, 0.0, 100.0)), 8) for k in candidate_knots))
    )

    raw_segments = []
    for i in range(len(knots) - 1):
        z0, z1 = knots[i], knots[i + 1]
        if z1 - z0 < 1e-8:
            continue
        y0 = aggregated_membership_at(z0, aggregated_alpha)
        y1 = aggregated_membership_at(z1, aggregated_alpha)
        slope = (y1 - y0) / (z1 - z0)
        raw_segments.append({"z0": z0, "z1": z1, "y0": y0, "y1": y1, "slope": slope})

    # Gabungkan segmen bersebelahan yang memiliki kemiringan (slope) identik
    merged_segments = []
    for seg in raw_segments:
        if not merged_segments:
            merged_segments.append(seg)
        else:
            prev = merged_segments[-1]
            if abs(prev["slope"] - seg["slope"]) < 1e-7:
                prev["z1"] = seg["z1"]
                prev["y1"] = seg["y1"]
            else:
                merged_segments.append(seg)

    segments_info = []
    total_area = 0.0
    total_moment = 0.0

    for idx, seg in enumerate(merged_segments, start=1):
        z0, z1 = seg["z0"], seg["z1"]
        y0, y1 = seg["y0"], seg["y1"]
        dz = z1 - z0
        area = 0.5 * dz * (y0 + y1)
        moment = (dz / 6.0) * (y0 * (2.0 * z0 + z1) + y1 * (z0 + 2.0 * z1))
        slope = seg["slope"]
        intercept = y0 - slope * z0

        if area > 1e-12:
            total_area += area
            total_moment += moment

        if abs(slope) < 1e-7:
            eq_str = f"μ(z) = {y0:.4f}"
        else:
            sign = "+" if intercept >= 0 else "-"
            if abs(intercept) < 1e-7:
                eq_str = f"μ(z) = {slope:.4f}z"
            else:
                eq_str = f"μ(z) = {slope:.4f}z {sign} {abs(intercept):.4f}"

        segments_info.append(
            {
                "segment_id": idx,
                "z_start": z0,
                "z_end": z1,
                "mu_start": y0,
                "mu_end": y1,
                "slope": slope,
                "intercept": intercept,
                "equation": eq_str,
                "area": area,
                "moment": moment,
            }
        )

    centroid = total_moment / total_area if total_area > 0 else 0.0
    return {
        "centroid": float(centroid),
        "total_moment": float(total_moment),
        "total_area": float(total_area),
        "segments": segments_info,
    }


def defuzzify_centroid_discrete(
    aggregated_alpha: Dict[str, float], num_points: int = 10001
) -> Tuple[float, np.ndarray, np.ndarray]:
    """Menghitung centroid secara diskrit menggunakan grid titik pada domain [0, 100]."""
    z_grid = np.linspace(0.0, 100.0, num_points)
    mu_grid = np.array([aggregated_membership_at(z, aggregated_alpha) for z in z_grid])
    denom = np.sum(mu_grid)
    if denom == 0.0:
        return 0.0, z_grid, mu_grid
    centroid = float(np.sum(z_grid * mu_grid) / denom)
    return centroid, z_grid, mu_grid


def compute_fuzzy_mamdani(
    ph: float,
    hardness: float,
    turbidity: float,
    method: str = "analytic",
) -> Dict[str, Any]:
    """Menjalankan inferensi Fuzzy Mamdani lengkap untuk satu sampel air."""
    fuzzified = fuzzify_inputs(ph, hardness, turbidity)
    evaluated_rules, aggregated_alpha = evaluate_rules(fuzzified)
    analytic_res = defuzzify_centroid_analytic(aggregated_alpha)
    discrete_centroid, z_grid, mu_grid = defuzzify_centroid_discrete(
        aggregated_alpha, num_points=1001
    )

    quality_score = (
        analytic_res["centroid"] if method == "analytic" else discrete_centroid
    )

    out_mfs = {
        name: triangular_mf(quality_score, *params)
        for name, params in MF_PARAMS["water_quality_score"]["sets"].items()
    }
    dominant_label = max(out_mfs, key=out_mfs.get)

    return {
        "inputs": {
            "ph": float(ph),
            "Hardness": float(hardness),
            "Turbidity": float(turbidity),
        },
        "fuzzified": fuzzified,
        "rules": evaluated_rules,
        "active_rules": [r for r in evaluated_rules if r["is_active"]],
        "aggregated_alpha": aggregated_alpha,
        "analytic": analytic_res,
        "discrete_centroid": discrete_centroid,
        "water_quality_score": float(quality_score),
        "quality_linguistic": dominant_label,
        "z_grid": z_grid,
        "mu_grid": mu_grid,
    }


def batch_fuzzy_quality_scores(
    X_array: np.ndarray, method: str = "analytic"
) -> np.ndarray:
    """Menghitung skor kualitas air fuzzy secara batch untuk array 2D [ph, Hardness, Turbidity]."""
    scores = np.zeros(X_array.shape[0], dtype=float)
    for i in range(X_array.shape[0]):
        res = compute_fuzzy_mamdani(
            X_array[i, 0], X_array[i, 1], X_array[i, 2], method=method
        )
        scores[i] = res["water_quality_score"]
    return scores
