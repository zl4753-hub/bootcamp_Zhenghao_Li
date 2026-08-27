"""Risk-aware outlier flagging without silently deleting market shocks."""

import numpy as np
import pandas as pd


def robust_zscore(values: pd.Series) -> pd.Series:
    """Median/MAD z-score, robust to heavy-tailed returns."""
    median = values.median()
    mad = (values - median).abs().median()
    if mad == 0 or np.isnan(mad):
        return pd.Series(0.0, index=values.index)
    return 0.6745 * (values - median) / mad


def flag_return_outliers(frame: pd.DataFrame, threshold: float = 5.0) -> pd.DataFrame:
    """Flag extreme returns; retain them because crisis days carry risk information."""
    out = frame.copy()
    out["return_1d"] = out["adjusted_close"].pct_change()
    out["return_robust_z"] = robust_zscore(out["return_1d"])
    out["return_outlier"] = out["return_robust_z"].abs() > threshold
    return out


def winsorize_series(values: pd.Series, lower: float = 0.005, upper: float = 0.995) -> pd.Series:
    """Clip a series for sensitivity analysis while leaving the baseline untouched."""
    lo, hi = values.quantile([lower, upper])
    return values.clip(lo, hi)
