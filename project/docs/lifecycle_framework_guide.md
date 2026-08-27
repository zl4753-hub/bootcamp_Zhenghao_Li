# Lifecycle framework guide

| Stage | Project location | Decision made |
|---|---|---|
| 1. Problem framing | `README.md`, `docs/problem_framing.md` | Predict next-day high-volatility risk for a portfolio risk manager, not return direction. |
| 2. Tooling | `.env.example`, `requirements.txt`, project folders | Use a reproducible Python layout with environment-driven paths. |
| 3. Python fundamentals | `notebooks/python_fundamentals_summary.ipynb`, `src/utils.py` | Move reusable naming and JSON helpers out of notebooks. |
| 4. Acquisition | `src/ingestion.py`, `data/raw/spy_daily.csv` | Use public Yahoo chart data and commit a reproducible snapshot. |
| 5. Storage | `src/storage.py`, `data/raw/`, `data/processed/` | Preserve raw data and overwrite deterministic processed checkpoints. |
| 6. Preprocessing | `src/cleaning.py`, `data/processed/spy_clean.csv` | Reject invalid OHLC records while preserving legitimate market moves. |
| 7. Outliers | `src/outliers.py`, `docs/outlier_policy.md` | Flag extreme returns but retain them in the baseline. |
| 8. EDA | `src/eda.py`, `reports/eda_summary.csv`, pipeline notebook | Use distributions, missingness, price, volatility, and regime views. |
| 9. Feature engineering | `src/features.py`, `docs/feature_dictionary.json` | Build 11 end-of-day lag, momentum, volatility, range, volume, trend, and drawdown features. |
| 10. Modeling | `src/modeling.py`, `model/model.pkl` | Use chronological 80/20 logistic classification with class balancing. |
| 11. Evaluation | `src/evaluation.py`, evaluation tables and charts | Report ROC-AUC/F1, 600-resample CI, threshold sensitivity, and trend subgroups. |
| 12. Delivery | `reports/final_report.md`, `reports/images/` | Give the risk manager decision implications beside self-contained charts. |
| 13. Productization | `app.py`, model bundle, API evidence in pipeline notebook | Load one saved model at startup and validate named/list feature payloads. |
| 14. Monitoring | `docs/monitoring_plan.md`, `docs/handoff_plan.md` | Monitor data, model, system, and business thresholds with named owners. |
| 15. Orchestration | `docs/orchestration_plan.md`, `src/run_step.py` | Decompose seven tasks and make cleaning CLI-callable and idempotent. |
| 16. Lifecycle review | This guide, `docs/project_summary.md`, `README.md` | Map every stage to real files and verify the full pipeline top to bottom. |
