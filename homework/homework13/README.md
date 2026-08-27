# Stage 13 Homework - Prediction API

This API serves predictions from a two-feature linear regression trained on a reproducible synthetic dataset. The model is saved with joblib and loaded once when Flask starts, so both routes reuse the same in-memory model.

## Running it

    python app.py

The server starts on http://127.0.0.1:5000 and loads model/model.pkl at startup.

## POST /predict

    curl -X POST http://127.0.0.1:5000/predict \
         -H "Content-Type: application/json" \
         -d "{\"features\": [0.1, 0.2]}"

Response: `{"prediction":23.58961171297328}`

## GET /predict/<f1>/<f2>

    curl http://127.0.0.1:5000/predict/0.1/0.2

Response: `{"prediction":23.58961171297328}`

## Bad input

Missing `features`, the wrong number of values, nonnumeric values, and non-finite values return HTTP 400 with a JSON `error` message. For example, `GET /predict/abc/0.2` returns `{"error":"features must contain only numbers"}`.
