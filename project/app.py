"""Flask API serving the saved SPY high-volatility risk model."""

from pathlib import Path
import math

from flask import Flask, jsonify, request
import joblib


ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "model/model.pkl"
bundle = joblib.load(MODEL_PATH)  # Loaded once when the service starts.
model = bundle["model"]
features = bundle["feature_columns"]
threshold = bundle["decision_threshold"]
app = Flask(__name__)


def validate_payload(payload):
    values = payload.get("features") if isinstance(payload, dict) else None
    if isinstance(values, dict):
        missing = [name for name in features if name not in values]
        if missing:
            return None, f"missing feature keys: {missing}"
        ordered = [values[name] for name in features]
    elif isinstance(values, list) and len(values) == len(features):
        ordered = values
    else:
        return None, f"features must be a mapping or a list of {len(features)} values"
    try:
        ordered = [float(value) for value in ordered]
    except (TypeError, ValueError):
        return None, "all feature values must be numeric"
    if not all(math.isfinite(value) for value in ordered):
        return None, "all feature values must be finite"
    return ordered, None


@app.get("/health")
def health():
    return jsonify({"status": "ok", "trained_through": bundle["trained_through"]})


@app.get("/metadata")
def metadata():
    return jsonify({"features": features, "target": bundle["target_definition"], "threshold": threshold})


@app.post("/predict")
def predict():
    values, error = validate_payload(request.get_json(silent=True) or {})
    if error:
        return jsonify({"error": error}), 400
    probability = float(model.predict_proba([values])[0, 1])
    return jsonify(
        {
            "high_volatility_probability": probability,
            "high_volatility_alert": bool(probability >= threshold),
            "decision_threshold": threshold,
        }
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
