# SPY Next-Day High-Volatility Risk Monitor

This end-to-end financial engineering project estimates whether SPY's next daily absolute return will exceed the trailing one-year 75th percentile. It is designed for a portfolio risk manager who needs an interpretable end-of-day escalation signal, not an automatic trade or return-direction forecast.

The committed data snapshot, reusable Python modules, chronological classifier, uncertainty analysis, stakeholder report, Flask API, monitoring plan, and orchestration CLI demonstrate the full lifecycle from raw data to technical handoff.

## Key result

The latest verified chronological test reports ROC-AUC **0.716** with a 600-resample 95% interval of **0.661–0.768**. F1 is **0.478**. Accuracy is below the majority-class benchmark, so the model is positioned as a ranking/review tool and not as a high-accuracy autonomous classifier. Read `reports/final_report.md` before using the result.

## Install

```bash
cd project
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Run from start to finish

Open `notebooks/project_pipeline.ipynb` and run every cell, or run:

```bash
python -c "from src.pipeline import run_full_pipeline; print(run_full_pipeline())"
```

The default uses the committed `data/raw/spy_daily.csv`. To request a live refresh:

```bash
python -c "from src.pipeline import run_full_pipeline; print(run_full_pipeline(refresh=True))"
```

## Run one orchestrated step

```bash
python -m src.run_step \
  --input data/raw/spy_daily.csv \
  --output data/processed/spy_clean.csv
```

The command is idempotent for a fixed raw file and logs to `logs/pipeline.log`.

## Serve the model

After running the pipeline:

```bash
python app.py
```

Inspect required features:

```bash
curl http://127.0.0.1:5001/metadata
```

Example prediction using an ordered list:

```bash
curl -X POST http://127.0.0.1:5001/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[0.001,0.0,0.01,0.03,0.008,0.012,0.014,0.009,0.05,0.02,-0.01]}'
```

Invalid lengths, missing keys, nonnumeric values, and non-finite values return HTTP 400 JSON errors. `/health` reports service status and model training date.

## Structure

```text
data/raw/          immutable provider snapshot
data/processed/    deterministic clean, feature, and prediction checkpoints
notebooks/         fundamentals, EDA, and full pipeline notebooks
src/               ingestion, cleaning, features, modeling, evaluation, reporting, CLI
model/             saved joblib model bundle
reports/           metrics, sensitivity tables, charts, stakeholder report
docs/              framing, risk, monitoring, handoff, orchestration, lifecycle summary
tests/             automated checks
```

## Lifecycle map

| Lifecycle stage | Location |
|---|---|
| Framing and scope | `docs/problem_framing.md` |
| Tooling and storage | `.env.example`, `requirements.txt`, `src/config.py`, `src/storage.py` |
| Acquisition and cleaning | `src/ingestion.py`, `src/cleaning.py`, `data/` |
| Outliers and EDA | `src/outliers.py`, `src/eda.py`, report summaries |
| Features and modeling | `src/features.py`, `src/modeling.py`, `model/model.pkl` |
| Evaluation and sensitivity | `src/evaluation.py`, evaluation artifacts in `reports/` |
| Stakeholder delivery | `reports/final_report.md` |
| Productization | `app.py` and API evidence in the pipeline notebook |
| Monitoring and handoff | `docs/monitoring_plan.md`, `docs/handoff_plan.md` |
| Orchestration | `docs/orchestration_plan.md`, `src/run_step.py` |
| Final lifecycle review | `docs/lifecycle_framework_guide.md`, `docs/project_summary.md` |

## Assumptions and next steps

The analysis assumes end-of-day SPY history remains relevant and that the rolling target definition matches the risk policy. It excludes portfolio holdings, trading/hedging costs, intraday information, and causal claims. Validate against another provider, add VIX/overnight features, evaluate calibration and decision costs, and collect more regimes before live use.
