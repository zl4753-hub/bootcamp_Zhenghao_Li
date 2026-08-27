"""Time-aware model training and evaluation."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import warnings

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.features import FEATURE_COLUMNS


def chronological_split(frame: pd.DataFrame, train_fraction: float = 0.80):
    """Return an earliest-train/latest-test split with no shuffling."""
    cut = int(len(frame) * train_fraction)
    if cut < 100 or len(frame) - cut < 50:
        raise ValueError("Dataset is too small for the requested chronological split")
    return frame.iloc[:cut].copy(), frame.iloc[cut:].copy()


def classification_metrics(y_true, predictions, probabilities) -> dict:
    """Compute required classification metrics and a simple benchmark."""
    y_true = np.asarray(y_true, dtype=int)
    predictions = np.asarray(predictions, dtype=int)
    probabilities = np.asarray(probabilities, dtype=float)
    majority = max(float(y_true.mean()), 1.0 - float(y_true.mean()))
    return {
        "accuracy": float(accuracy_score(y_true, predictions)),
        "precision": float(precision_score(y_true, predictions, zero_division=0)),
        "recall": float(recall_score(y_true, predictions, zero_division=0)),
        "f1": float(f1_score(y_true, predictions, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_true, probabilities)),
        "majority_accuracy": majority,
        "positive_rate": float(y_true.mean()),
        "confusion_matrix": confusion_matrix(y_true, predictions).tolist(),
    }


def fit_risk_classifier(frame: pd.DataFrame, train_fraction: float = 0.80):
    """Fit a scaled, class-balanced logistic regression on a chronological split."""
    train, test = chronological_split(frame, train_fraction=train_fraction)
    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    solver="liblinear",
                    class_weight="balanced",
                    max_iter=2000,
                    random_state=42,
                ),
            ),
        ]
    )
    # Some macOS Accelerate builds emit spurious overflow warnings inside
    # sklearn's finite matrix multiplication even when all inputs/outputs are finite.
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning, module="sklearn.utils.extmath")
        pipeline.fit(train[FEATURE_COLUMNS], train["target_high_vol_next"].astype(int))
        probabilities = pipeline.predict_proba(test[FEATURE_COLUMNS])[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    metrics = classification_metrics(test["target_high_vol_next"], predictions, probabilities)
    scored = test[["date", "adjusted_close", "market_regime", "target_high_vol_next"]].copy()
    scored["predicted_probability"] = probabilities
    scored["predicted_class"] = predictions
    bundle = {
        "model": pipeline,
        "feature_columns": FEATURE_COLUMNS,
        "decision_threshold": 0.5,
        "target_definition": "Next-day absolute return exceeds trailing 252-session 75th percentile",
        "trained_through": train["date"].max().date().isoformat(),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    return bundle, train, test, scored, metrics


def save_model(bundle: dict, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, path)
    return path


def load_model(path: Path) -> dict:
    return joblib.load(path)


def coefficient_table(bundle: dict) -> pd.DataFrame:
    coefficients = bundle["model"].named_steps["classifier"].coef_[0]
    return pd.DataFrame(
        {"feature": bundle["feature_columns"], "standardized_coefficient": coefficients}
    ).sort_values("standardized_coefficient", key=np.abs, ascending=False)
