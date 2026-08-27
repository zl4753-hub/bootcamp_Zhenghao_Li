"""Reusable evaluation helpers for Homework 11."""

import numpy as np


def mean_impute(a: np.ndarray) -> np.ndarray:
    out = np.asarray(a, dtype=float).copy()
    out[np.isnan(out)] = np.nanmean(out)
    return out


def median_impute(a: np.ndarray) -> np.ndarray:
    out = np.asarray(a, dtype=float).copy()
    out[np.isnan(out)] = np.nanmedian(out)
    return out


class SimpleLinReg:
    """One-feature ordinary least-squares regression."""

    def fit(self, X, y):
        X1 = np.c_[np.ones(len(X)), np.asarray(X).ravel()]
        beta = np.linalg.pinv(X1) @ np.asarray(y)
        self.intercept_ = float(beta[0])
        self.coef_ = np.array([float(beta[1])])
        return self

    def predict(self, X):
        return self.intercept_ + self.coef_[0] * np.asarray(X).ravel()


def mae(y_true, y_pred) -> float:
    return float(np.mean(np.abs(np.asarray(y_true) - np.asarray(y_pred))))


def bootstrap_metric(y_true, y_pred, fn=mae, n_boot=600, seed=111, alpha=0.05):
    """Pairs-bootstrap a metric computed from fixed out-of-sample-like predictions."""
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    rng = np.random.default_rng(seed)
    idx = np.arange(len(y_true))
    stats = np.empty(n_boot)
    for i in range(n_boot):
        sample = rng.choice(idx, size=len(idx), replace=True)
        stats[i] = fn(y_true[sample], y_pred[sample])
    lo, hi = np.percentile(stats, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return {
        "estimate": fn(y_true, y_pred),
        "mean": float(np.mean(stats)),
        "lo": float(lo),
        "hi": float(hi),
        "samples": stats,
    }


def bootstrap_predictions(X, y, x_grid, n_boot=600, seed=111, alpha=0.05):
    """Pairs-bootstrap linear-model mean predictions over a fixed grid."""
    X = np.asarray(X).ravel()
    y = np.asarray(y)
    rng = np.random.default_rng(seed)
    idx = np.arange(len(y))
    predictions = np.empty((n_boot, len(x_grid)))
    for i in range(n_boot):
        sample = rng.choice(idx, size=len(idx), replace=True)
        model = SimpleLinReg().fit(X[sample].reshape(-1, 1), y[sample])
        predictions[i] = model.predict(x_grid)
    q = [100 * alpha / 2, 100 * (1 - alpha / 2)]
    return predictions.mean(axis=0), *np.percentile(predictions, q, axis=0)
