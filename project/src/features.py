"""Leakage-aware features and next-day high-volatility target."""

import numpy as np
import pandas as pd


FEATURE_COLUMNS = [
    "return_1d",
    "return_lag_1",
    "momentum_5",
    "momentum_20",
    "volatility_5",
    "volatility_20",
    "volatility_60",
    "range_pct",
    "volume_change_5",
    "price_vs_sma20",
    "drawdown_60",
]


def build_features(
    frame: pd.DataFrame,
    target_quantile: float = 0.75,
    target_window: int = 252,
) -> pd.DataFrame:
    """Create features known at day t and a target for high volatility at t+1."""
    out = frame.copy().sort_values("date").reset_index(drop=True)
    price = out["adjusted_close"]
    returns = price.pct_change()
    out["return_1d"] = returns
    out["return_lag_1"] = returns.shift(1)
    out["momentum_5"] = price.pct_change(5)
    out["momentum_20"] = price.pct_change(20)
    out["volatility_5"] = returns.rolling(5).std()
    out["volatility_20"] = returns.rolling(20).std()
    out["volatility_60"] = returns.rolling(60).std()
    out["range_pct"] = (out["high"] - out["low"]) / out["close"]
    out["volume_change_5"] = out["volume"].replace(0, np.nan).pct_change(5)
    sma20 = price.rolling(20).mean()
    out["price_vs_sma20"] = price / sma20 - 1
    out["drawdown_60"] = price / price.rolling(60).max() - 1
    out["sma50"] = price.rolling(50).mean()
    out["market_regime"] = np.where(price >= out["sma50"], "Above 50-day trend", "Below 50-day trend")
    out["high_vol_threshold"] = returns.abs().rolling(target_window, min_periods=126).quantile(target_quantile)
    next_abs_return = returns.abs().shift(-1)
    out["target_high_vol_next"] = (next_abs_return > out["high_vol_threshold"]).astype(float)
    out.loc[next_abs_return.isna(), "target_high_vol_next"] = np.nan
    out = out.replace([np.inf, -np.inf], np.nan)
    return out.dropna(subset=FEATURE_COLUMNS + ["target_high_vol_next", "market_regime"]).reset_index(drop=True)


def feature_dictionary() -> dict:
    return {
        "return_1d": "Current close-to-close return available after day t closes.",
        "return_lag_1": "Previous day's return.",
        "momentum_5": "Five-session price change.",
        "momentum_20": "Twenty-session price change.",
        "volatility_5": "Five-session standard deviation of returns.",
        "volatility_20": "Twenty-session standard deviation of returns.",
        "volatility_60": "Sixty-session standard deviation of returns.",
        "range_pct": "Current high-low range divided by close.",
        "volume_change_5": "Five-session percentage change in volume.",
        "price_vs_sma20": "Distance of price from its 20-session average.",
        "drawdown_60": "Drawdown from the trailing 60-session high.",
    }
