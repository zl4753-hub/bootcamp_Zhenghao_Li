"""Consistent CSV storage helpers."""

from pathlib import Path
import pandas as pd


def save_csv(frame: pd.DataFrame, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    return path


def load_csv(path: Path, date_columns=("date",)) -> pd.DataFrame:
    existing = [column for column in date_columns if column in pd.read_csv(path, nrows=0).columns]
    return pd.read_csv(path, parse_dates=existing)
