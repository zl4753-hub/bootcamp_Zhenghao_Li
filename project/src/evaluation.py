"""Uncertainty, scenario sensitivity, and subgroup evaluation."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, roc_auc_score

from src.features import build_features
from src.modeling import fit_risk_classifier


def bootstrap_metric_ci(
    y_true,
    probabilities,
    metric: str = "roc_auc",
    n_boot: int = 600,
    seed: int = 42,
    alpha: float = 0.05,
) -> dict:
    """Pairs-bootstrap a test-set classification metric."""
    y_true = np.asarray(y_true, dtype=int)
    probabilities = np.asarray(probabilities, dtype=float)
    rng = np.random.default_rng(seed)
    values = []
    while len(values) < n_boot:
        sample = rng.integers(0, len(y_true), len(y_true))
        ys, ps = y_true[sample], probabilities[sample]
        if metric == "roc_auc":
            if len(np.unique(ys)) < 2:
                continue
            value = roc_auc_score(ys, ps)
        elif metric == "f1":
            value = f1_score(ys, ps >= 0.5, zero_division=0)
        else:
            raise ValueError(f"Unsupported metric: {metric}")
        values.append(float(value))
    values = np.asarray(values)
    lo, hi = np.quantile(values, [alpha / 2, 1 - alpha / 2])
    estimate = roc_auc_score(y_true, probabilities) if metric == "roc_auc" else f1_score(
        y_true, probabilities >= 0.5, zero_division=0
    )
    return {
        "metric": metric,
        "estimate": float(estimate),
        "mean": float(values.mean()),
        "lo": float(lo),
        "hi": float(hi),
        "n_boot": int(n_boot),
        "samples": values,
    }


def evaluate_target_scenarios(clean_frame: pd.DataFrame) -> pd.DataFrame:
    """Compare model results under three high-volatility label assumptions."""
    rows = []
    for quantile in [0.70, 0.75, 0.80]:
        featured = build_features(clean_frame, target_quantile=quantile)
        _, _, _, _, metrics = fit_risk_classifier(featured)
        rows.append(
            {
                "scenario": f"Trailing quantile {quantile:.0%}",
                "target_quantile": quantile,
                **{key: metrics[key] for key in ["accuracy", "precision", "recall", "f1", "roc_auc", "positive_rate"]},
            }
        )
    return pd.DataFrame(rows)


def subgroup_metrics(scored: pd.DataFrame) -> pd.DataFrame:
    """Measure hidden performance differences across trend regimes."""
    rows = []
    for regime, group in scored.groupby("market_regime"):
        y = group["target_high_vol_next"].astype(int)
        p = group["predicted_probability"]
        pred = group["predicted_class"].astype(int)
        rows.append(
            {
                "market_regime": regime,
                "rows": len(group),
                "positive_rate": float(y.mean()),
                "f1": float(f1_score(y, pred, zero_division=0)),
                "roc_auc": float(roc_auc_score(y, p)) if y.nunique() > 1 else np.nan,
            }
        )
    return pd.DataFrame(rows)
