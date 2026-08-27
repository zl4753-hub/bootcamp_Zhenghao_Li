"""Exploratory summaries for the processed market dataset."""

import pandas as pd


def eda_summary(frame: pd.DataFrame) -> pd.DataFrame:
    """Return stakeholder-useful distribution and missingness statistics."""
    numeric = frame.select_dtypes("number")
    summary = numeric.describe().T
    summary["median"] = numeric.median()
    summary["skew"] = numeric.skew()
    summary["missing"] = numeric.isna().sum()
    return summary[["count", "mean", "median", "std", "min", "max", "skew", "missing"]]
