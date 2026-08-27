"""Validation and cleaning for raw OHLCV market data."""

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = ["date", "open", "high", "low", "close", "adjusted_close", "volume"]


def clean_ohlcv(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate types, remove invalid rows, and return sorted unique observations."""
    missing = sorted(set(REQUIRED_COLUMNS) - set(frame.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    out = frame[REQUIRED_COLUMNS].copy()
    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    for column in REQUIRED_COLUMNS[1:]:
        out[column] = pd.to_numeric(out[column], errors="coerce")
    out = out.dropna(subset=["date", "open", "high", "low", "close", "adjusted_close"])
    out = out[(out[["open", "high", "low", "close", "adjusted_close"]] > 0).all(axis=1)]
    out = out[out["high"] >= out["low"]]
    out["volume"] = out["volume"].fillna(0).clip(lower=0).astype("int64")
    out = out.sort_values("date").drop_duplicates("date", keep="last").reset_index(drop=True)
    if not out["date"].is_monotonic_increasing:
        raise ValueError("Dates are not monotonic after cleaning")
    return out


def cleaning_summary(raw: pd.DataFrame, clean: pd.DataFrame) -> dict:
    return {
        "raw_rows": int(len(raw)),
        "clean_rows": int(len(clean)),
        "rows_removed": int(len(raw) - len(clean)),
        "start_date": clean["date"].min().date().isoformat(),
        "end_date": clean["date"].max().date().isoformat(),
        "duplicate_dates": int(clean["date"].duplicated().sum()),
        "remaining_nulls": int(clean.isna().sum().sum()),
    }
