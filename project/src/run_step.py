"""CLI wrapper for one idempotent pipeline step: cleaning raw SPY data."""

import argparse
import logging
from pathlib import Path

from src.cleaning import clean_ohlcv
from src.config import PROJECT_ROOT
from src.storage import load_csv, save_csv


def run_clean_step(input_path: Path, output_path: Path) -> Path:
    """Load, validate, clean, and overwrite the deterministic processed CSV."""
    logging.info("Loading raw data from %s", input_path)
    raw = load_csv(input_path)
    clean = clean_ohlcv(raw)
    save_csv(clean, output_path)
    logging.info("Wrote %d clean rows to %s", len(clean), output_path)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the SPY data-cleaning pipeline step")
    parser.add_argument("--input", type=Path, default=PROJECT_ROOT / "data/raw/spy_daily.csv")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "data/processed/spy_clean.csv")
    args = parser.parse_args()
    log_path = PROJECT_ROOT / "logs/pipeline.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
    )
    run_clean_step(args.input, args.output)


if __name__ == "__main__":
    main()
