
from flask import Flask, request, jsonify
import joblib

# Loaded ONCE at startup, not inside either request route.
from pathlib import Path
import math
MODEL_PATH = Path(__file__).resolve().parent / 'model' / 'model.pkl'
model = joblib.load(MODEL_PATH)
app = Flask(__name__)


def predict_values(features):
    if not isinstance(features, (list, tuple)) or len(features) != 2:
        return None, 'features must be a list containing exactly 2 numbers'
    try:
        values = [float(value) for value in features]
    except (TypeError, ValueError):
        return None, 'features must contain only numbers'
    if not all(math.isfinite(value) for value in values):
        return None, 'features must contain only finite numbers'
    prediction = float(model.predict([values])[0])
    return prediction, None


@app.route('/predict', methods=['POST'])
def predict_post():
    data = request.get_json(silent=True) or {}
    features = data.get('features')
    prediction, error = predict_values(features)
    if error:
        return jsonify({'error': error}), 400
    return jsonify({'prediction': prediction})


@app.route('/predict/<f1>/<f2>', methods=['GET'])
def predict_get(f1, f2):
    prediction, error = predict_values([f1, f2])
    if error:
        return jsonify({'error': error}), 400
    return jsonify({'prediction': prediction})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
