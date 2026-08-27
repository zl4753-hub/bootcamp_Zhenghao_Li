"""Environment-driven project configuration."""

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def get_data_dir() -> Path:
    """Return the configured data directory, resolved from the project root."""
    configured = Path(os.getenv("DATA_DIR", "data"))
    return configured if configured.is_absolute() else PROJECT_ROOT / configured


def ensure_project_dirs() -> None:
    """Create every runtime directory used by the pipeline."""
    for relative in [
        "data/raw",
        "data/processed",
        "docs",
        "logs",
        "model",
        "notebooks",
        "reports/images",
    ]:
        (PROJECT_ROOT / relative).mkdir(parents=True, exist_ok=True)
