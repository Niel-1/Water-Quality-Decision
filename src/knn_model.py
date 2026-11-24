"""Implementasi klasifikasi K-Nearest Neighbor (KNN) dan evaluasi model."""

from typing import Dict, List, Tuple, Optional, Any
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)


CLASS_ORDER = ["Not Potable", "Potable"]
CLASS_RANK = {"Not Potable": 0, "Potable": 1}


class MinMaxScalerScratch:
    """Normalisasi fitur ke rentang [0, 1] berdasarkan nilai minimum dan maksimum data latih."""

    def __init__(self):
        self.min_: Optional[np.ndarray] = None
        self.max_: Optional[np.ndarray] = None
        self.range_: Optional[np.ndarray] = None

    def fit(self, X: np.ndarray) -> "MinMaxScalerScratch":
        X_arr = np.asarray(X, dtype=float)
        self.min_ = np.min(X_arr, axis=0)
        self.max_ = np.max(X_arr, axis=0)
        diff = self.max_ - self.min_
        diff[diff == 0.0] = 1.0
        self.range_ = diff
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        if self.min_ is None or self.range_ is None:
            raise ValueError("Scaler belum di-fit dengan data latih.")
        X_arr = np.asarray(X, dtype=float)
        return (X_arr - self.min_) / self.range_

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        return self.fit(X).transform(X)


class ZScoreScalerScratch:
    """Normalisasi fitur menggunakan rata-rata dan standar deviasi data latih."""

    def __init__(self):
        self.mean_: Optional[np.ndarray] = None
        self.std_: Optional[np.ndarray] = None

    def fit(self, X: np.ndarray) -> "ZScoreScalerScratch":
        X_arr = np.asarray(X, dtype=float)
        self.mean_ = np.mean(X_arr, axis=0)
        std = np.std(X_arr, axis=0, ddof=0)
        std[std == 0.0] = 1.0
        self.std_ = std
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        if self.mean_ is None or self.std_ is None:
            raise ValueError("Scaler belum di-fit dengan data latih.")
        X_arr = np.asarray(X, dtype=float)
        return (X_arr - self.mean_) / self.std_

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        return self.fit(X).transform(X)


class KNNClassifierScratch:
    """Implementasi KNN berbasis jarak Euclidean dengan rincian perhitungan tiap tetangga terdekat."""

    def __init__(self, k: int = 5):
        self.k = int(k)
        self.X_train: Optional[np.ndarray] = None
        self.y_train: Optional[np.ndarray] = None
        self.train_ids: Optional[np.ndarray] = None
        self.X_train_raw: Optional[np.ndarray] = None

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_train_raw: Optional[np.ndarray] = None,
        train_ids: Optional[np.ndarray] = None,
    ) -> "KNNClassifierScratch":
        self.X_train = np.asarray(X_train, dtype=float)
        self.y_train = np.asarray(y_train, dtype=str)
        self.X_train_raw = (
            np.asarray(X_train_raw, dtype=float)
            if X_train_raw is not None
            else self.X_train
        )
        self.train_ids = (
            np.asarray(train_ids)
            if train_ids is not None
            else np.arange(len(self.X_train))
        )
        return self

    @staticmethod
    def euclidean_distances(x_query: np.ndarray, X_train: np.ndarray) -> np.ndarray:
        """Menghitung jarak Euclidean antara vektor uji dan seluruh data latih."""
        diff = X_train - x_query
        return np.sqrt(np.sum(diff ** 2, axis=1))

    def _vote(
        self, neighbor_labels: np.ndarray, neighbor_distances: np.ndarray
    ) -> Tuple[str, Dict[str, int]]:
        """Menentukan kelas prediksi lewat voting mayoritas dengan rata-rata jarak terkecil sebagai pemecah seri."""
        vote_counts = {c: 0 for c in CLASS_ORDER}
        for lbl in neighbor_labels:
            vote_counts[str(lbl)] = vote_counts.get(str(lbl), 0) + 1

        max_count = max(vote_counts.values())
        candidates = [c for c, cnt in vote_counts.items() if cnt == max_count]
        if len(candidates) == 1:
            return candidates[0], vote_counts

        best_cls = candidates[0]
        best_dist = float("inf")
        for c in candidates:
            mask = neighbor_labels == c
            mean_d = float(np.mean(neighbor_distances[mask]))
            if mean_d < best_dist:
                best_dist = mean_d
                best_cls = c
        return best_cls, vote_counts

    def predict_single_detailed(
        self,
        x_query_scaled: np.ndarray,
        x_query_raw: Optional[np.ndarray] = None,
        feature_names: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Memprediksi satu sampel uji beserta rincian jarak dan K tetangga terdekat."""
        if self.X_train is None or self.y_train is None:
            raise ValueError("Model KNN belum di-fit.")

        x_q = np.asarray(x_query_scaled, dtype=float).ravel()
        diffs = self.X_train - x_q
        sq_diffs = diffs ** 2
        sum_sq = np.sum(sq_diffs, axis=1)
        dists = np.sqrt(sum_sq)

        sorted_indices = np.argsort(dists, kind="mergesort")
        k_indices = sorted_indices[: self.k]

        k_labels = self.y_train[k_indices]
        k_dists = dists[k_indices]
        predicted_class, vote_counts = self._vote(k_labels, k_dists)

        neighbors_detail = []
        for rank, idx in enumerate(k_indices, start=1):
            item = {
                "rank": rank,
                "train_index": int(idx),
                "sample_id": str(self.train_ids[idx]),
                "raw_features": self.X_train_raw[idx].tolist(),
                "scaled_features": self.X_train[idx].tolist(),
                "feature_diffs": diffs[idx].tolist(),
                "feature_sq_diffs": sq_diffs[idx].tolist(),
                "sum_sq_diff": float(sum_sq[idx]),
                "distance": float(dists[idx]),
                "label": str(self.y_train[idx]),
            }
            neighbors_detail.append(item)

        return {
            "k": self.k,
            "query_raw": x_query_raw.tolist() if x_query_raw is not None else x_q.tolist(),
            "query_scaled": x_q.tolist(),
            "feature_names": feature_names or [f"X{i+1}" for i in range(len(x_q))],
            "predicted_class": predicted_class,
            "vote_counts": vote_counts,
            "neighbors": neighbors_detail,
            "all_distances": dists,
            "sorted_indices": sorted_indices,
        }

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        X_arr = np.asarray(X_test, dtype=float)
        preds = []
        for i in range(X_arr.shape[0]):
            res = self.predict_single_detailed(X_arr[i])
            preds.append(res["predicted_class"])
        return np.array(preds, dtype=str)


def compute_classification_metrics(
    y_true: np.ndarray, y_pred: np.ndarray
) -> Dict[str, Any]:
    """Menghitung metrik akurasi, precision, recall, F1-score, dan confusion matrix."""
    acc = float(accuracy_score(y_true, y_pred))
    prec_macro = float(
        precision_score(
            y_true, y_pred, labels=CLASS_ORDER, average="macro", zero_division=0
        )
    )
    rec_macro = float(
        recall_score(
            y_true, y_pred, labels=CLASS_ORDER, average="macro", zero_division=0
        )
    )
    f1_macro = float(
        f1_score(y_true, y_pred, labels=CLASS_ORDER, average="macro", zero_division=0)
    )

    prec_weighted = float(
        precision_score(
            y_true, y_pred, labels=CLASS_ORDER, average="weighted", zero_division=0
        )
    )
    rec_weighted = float(
        recall_score(
            y_true, y_pred, labels=CLASS_ORDER, average="weighted", zero_division=0
        )
    )
    f1_weighted = float(
        f1_score(
            y_true, y_pred, labels=CLASS_ORDER, average="weighted", zero_division=0
        )
    )

    cm = confusion_matrix(y_true, y_pred, labels=CLASS_ORDER)
    report_dict = classification_report(
        y_true, y_pred, labels=CLASS_ORDER, output_dict=True, zero_division=0
    )

    per_class = {}
    for cls in CLASS_ORDER:
        per_class[cls] = {
            "precision": float(report_dict[cls]["precision"]),
            "recall": float(report_dict[cls]["recall"]),
            "f1_score": float(report_dict[cls]["f1-score"]),
            "support": int(report_dict[cls]["support"]),
        }

    return {
        "accuracy": acc,
        "precision_macro": prec_macro,
        "recall_macro": rec_macro,
        "f1_macro": f1_macro,
        "precision_weighted": prec_weighted,
        "recall_weighted": rec_weighted,
        "f1_weighted": f1_weighted,
        "confusion_matrix": cm.tolist(),
        "class_labels": CLASS_ORDER,
        "per_class": per_class,
    }


def split_dataset_leakage_free(
    df: pd.DataFrame, split_strategy: str = "stratified_ordered", train_ratio: float = 0.8
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Membagi dataset menjadi data latih dan data uji sesuai strategi split dan rasio yang dipilih."""
    if split_strategy == "stratified_class":
        train_parts = []
        test_parts = []
        for cls in CLASS_ORDER:
            sub = df[df["potability_label"] == cls].reset_index(drop=True)
            idx = int(round(len(sub) * train_ratio))
            train_parts.append(sub.iloc[:idx])
            test_parts.append(sub.iloc[idx:])
        train_df = pd.concat(train_parts, ignore_index=True)
        test_df = pd.concat(test_parts, ignore_index=True)
        return train_df, test_df
    else:
        split_idx = int(round(len(df) * train_ratio))
        train_df = df.iloc[:split_idx].reset_index(drop=True)
        test_df = df.iloc[split_idx:].reset_index(drop=True)
        return train_df, test_df


def run_head_to_head_evaluation(
    df: pd.DataFrame,
    k_values: List[int] = [3, 5, 7, 9, 11],
    scaler_type: str = "minmax",
    split_strategy: str = "stratified_ordered",
    train_ratio: float = 0.8,
) -> Dict[str, Any]:
    """Membandingkan performa Baseline KNN (3 fitur) dan Fuzzy-Enhanced KNN (4 fitur) serta mengecek kesesuaian dengan scikit-learn."""
    train_df, test_df = split_dataset_leakage_free(
        df, split_strategy=split_strategy, train_ratio=train_ratio
    )

    features_a = ["ph", "Hardness", "Turbidity"]
    features_b = [
        "ph",
        "Hardness",
        "Turbidity",
        "fuzzy_quality_score",
    ]

    Xa_train_raw = train_df[features_a].values
    Xa_test_raw = test_df[features_a].values
    Xb_train_raw = train_df[features_b].values
    Xb_test_raw = test_df[features_b].values

    y_train = train_df["potability_label"].values
    y_test = test_df["potability_label"].values
    train_ids = (
        train_df["sample_id"].values
        if "sample_id" in train_df.columns
        else np.arange(len(train_df))
    )

    scaler_cls = MinMaxScalerScratch if scaler_type == "minmax" else ZScoreScalerScratch
    scaler_a = scaler_cls().fit(Xa_train_raw)
    scaler_b = scaler_cls().fit(Xb_train_raw)

    Xa_train = scaler_a.transform(Xa_train_raw)
    Xa_test = scaler_a.transform(Xa_test_raw)
    Xb_train = scaler_b.transform(Xb_train_raw)
    Xb_test = scaler_b.transform(Xb_test_raw)

    results_by_k = {}
    for k in k_values:
        # Model A (Scratch)
        knn_a_scratch = KNNClassifierScratch(k=k).fit(
            Xa_train,
            y_train,
            X_train_raw=Xa_train_raw,
            train_ids=train_ids,
        )
        pred_a_scratch = knn_a_scratch.predict(Xa_test)
        metrics_a = compute_classification_metrics(y_test, pred_a_scratch)

        # Model B (Scratch)
        knn_b_scratch = KNNClassifierScratch(k=k).fit(
            Xb_train,
            y_train,
            X_train_raw=Xb_train_raw,
            train_ids=train_ids,
        )
        pred_b_scratch = knn_b_scratch.predict(Xb_test)
        metrics_b = compute_classification_metrics(y_test, pred_b_scratch)

        # Pembanding Scikit-Learn
        knn_a_sk = KNeighborsClassifier(
            n_neighbors=k, metric="euclidean", algorithm="brute"
        ).fit(Xa_train, y_train)
        pred_a_sk = knn_a_sk.predict(Xa_test)
        knn_b_sk = KNeighborsClassifier(
            n_neighbors=k, metric="euclidean", algorithm="brute"
        ).fit(Xb_train, y_train)
        pred_b_sk = knn_b_sk.predict(Xb_test)

        agreement_a = float(np.mean(pred_a_scratch == pred_a_sk))
        agreement_b = float(np.mean(pred_b_scratch == pred_b_sk))

        results_by_k[k] = {
            "k": k,
            "model_a": metrics_a,
            "model_b": metrics_b,
            "delta_accuracy": metrics_b["accuracy"] - metrics_a["accuracy"],
            "delta_f1_macro": metrics_b["f1_macro"] - metrics_a["f1_macro"],
            "sklearn_agreement_a": agreement_a,
            "sklearn_agreement_b": agreement_b,
            "y_pred_a": pred_a_scratch.tolist(),
            "y_pred_b": pred_b_scratch.tolist(),
        }

    return {
        "split_strategy": split_strategy,
        "scaler_type": scaler_type,
        "train_size": len(train_df),
        "test_size": len(test_df),
        "train_class_counts": pd.Series(y_train).value_counts().to_dict(),
        "test_class_counts": pd.Series(y_test).value_counts().to_dict(),
        "scaler_a_params": {
            "min": scaler_a.min_.tolist()
            if hasattr(scaler_a, "min_")
            else scaler_a.mean_.tolist(),
            "max": scaler_a.max_.tolist()
            if hasattr(scaler_a, "max_")
            else scaler_a.std_.tolist(),
        },
        "scaler_b_params": {
            "min": scaler_b.min_.tolist()
            if hasattr(scaler_b, "min_")
            else scaler_b.mean_.tolist(),
            "max": scaler_b.max_.tolist()
            if hasattr(scaler_b, "max_")
            else scaler_b.std_.tolist(),
        },
        "results_by_k": results_by_k,
        "train_df": train_df,
        "test_df": test_df,
        "scaler_a": scaler_a,
        "scaler_b": scaler_b,
    }
