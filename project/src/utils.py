"""Small reusable utilities."""

from pathlib import Path
import json


def snake_case_columns(frame):
    """Return a copy with lower snake-case column names."""
    out = frame.copy()
    out.columns = [
        str(column).strip().lower().replace(" ", "_").replace("-", "_")
        for column in out.columns
    ]
    return out


def write_json(payload: dict, path: Path) -> None:
    """Write a JSON artifact with stable human-readable formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
