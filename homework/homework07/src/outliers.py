import pandas as pd
import numpy as np

def detect_outliers_iqr(series: pd.Series, k: float = 1.5) -> pd.Series:
    """Detect outliers using the Interquartile Range (IQR) method.
    
    Assumptions: Quartiles robustly capture distribution spread; k controls strictness.
    """
    if k <= 0:
        raise ValueError("Parameter k must be positive.")
    if series.empty:
        return pd.Series(dtype=bool, index=series.index)
        
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - k * iqr
    upper = q3 + k * iqr
    return (series < lower) | (series > upper)

def detect_outliers_zscore(series: pd.Series, threshold: float = 3.0, ddof: int = 1) -> pd.Series:
    """Detect outliers where standard score |z| > threshold.
    
    Assumptions: Distribution is roughly Gaussian; uses sample std (ddof=1) by default.
    """
    if threshold <= 0:
        raise ValueError("Threshold must be positive.")
    if series.empty:
        return pd.Series(dtype=bool, index=series.index)
        
    mu = series.mean()
    sigma = series.std(ddof=ddof)
    if sigma == 0 or pd.isna(sigma):
        return pd.Series(False, index=series.index)
        
    z = (series - mu) / sigma
    return z.abs() > threshold

def winsorize_series(series: pd.Series, lower: float = 0.05, upper: float = 0.95) -> pd.Series:
    """Cap values below lower quantile and above upper quantile."""
    if not (0 <= lower < upper <= 1):
        raise ValueError("Quantiles must satisfy 0 <= lower < upper <= 1.")
        
    lo = series.quantile(lower)
    hi = series.quantile(upper)
    return series.clip(lower=lo, upper=hi)