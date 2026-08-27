"""Acquire and parse public SPY daily data from Yahoo Finance's chart endpoint."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import time

import pandas as pd
import requests


YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
USER_AGENT = "Mozilla/5.0"


def parse_chart_payload(payload: dict) -> pd.DataFrame:
    """Convert a Yahoo chart JSON payload into a date-indexed OHLCV table."""
    chart = payload.get("chart", {})
    if chart.get("error"):
        raise ValueError(f"Provider error: {chart['error']}")
    results = chart.get("result") or []
    if not results:
        raise ValueError("Chart payload contains no result")
    result = results[0]
    quote = result["indicators"]["quote"][0]
    adjusted = result.get("indicators", {}).get("adjclose", [{}])[0].get("adjclose")
    frame = pd.DataFrame(
        {
            "date": pd.to_datetime(result["timestamp"], unit="s", utc=True).tz_convert(None),
            "open": quote.get("open"),
            "high": quote.get("high"),
            "low": quote.get("low"),
            "close": quote.get("close"),
            "adjusted_close": adjusted if adjusted is not None else quote.get("close"),
            "volume": quote.get("volume"),
        }
    )
    return frame.sort_values("date").drop_duplicates("date").reset_index(drop=True)


def fetch_spy_history(
    output_path: Path,
    symbol: str = "SPY",
    years: int = 10,
    timeout: int = 30,
) -> pd.DataFrame:
    """Download roughly ``years`` of daily SPY data and save a raw CSV snapshot."""
    period2 = int(time.time())
    period1 = period2 - int(years * 365.25 * 24 * 60 * 60)
    response = requests.get(
        YAHOO_CHART_URL.format(symbol=symbol),
        params={
            "period1": period1,
            "period2": period2,
            "interval": "1d",
            "events": "history",
            "includeAdjustedClose": "true",
        },
        headers={"User-Agent": USER_AGENT},
        timeout=timeout,
    )
    response.raise_for_status()
    frame = parse_chart_payload(response.json())
    if len(frame) < 500:
        raise ValueError(f"Expected at least 500 daily rows, received {len(frame)}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output_path, index=False)
    return frame


def load_or_fetch(output_path: Path, refresh: bool = False) -> pd.DataFrame:
    """Use the committed raw snapshot unless a refresh is explicitly requested."""
    if output_path.exists() and not refresh:
        return pd.read_csv(output_path, parse_dates=["date"])
    return fetch_spy_history(output_path)
