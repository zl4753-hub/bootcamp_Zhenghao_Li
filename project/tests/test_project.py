"""Fast checks for leakage-sensitive project behavior."""

import pandas as pd

from src.cleaning import clean_ohlcv
from src.features import FEATURE_COLUMNS, build_features


def test_cleaning_sorts_and_deduplicates():
    frame = pd.DataFrame(
        {
            "date": ["2026-01-02", "2026-01-01", "2026-01-01"],
            "open": [101, 100, 100], "high": [102, 101, 101], "low": [100, 99, 99],
            "close": [101, 100, 100], "adjusted_close": [101, 100, 100], "volume": [10, 11, 11],
        }
    )
    clean = clean_ohlcv(frame)
    assert len(clean) == 2
    assert clean["date"].is_monotonic_increasing


def test_features_exist_and_target_is_binary():
    dates = pd.bdate_range("2024-01-01", periods=400)
    price = pd.Series(range(100, 500), dtype=float)
    frame = pd.DataFrame(
        {"date": dates, "open": price, "high": price + 1, "low": price - 1,
         "close": price, "adjusted_close": price, "volume": 1_000_000}
    )
    featured = build_features(frame)
    assert set(FEATURE_COLUMNS).issubset(featured.columns)
    assert set(featured["target_high_vol_next"].unique()).issubset({0.0, 1.0})
