# Orchestration and system design

## Task boundaries

| Task | Inputs | Outputs | Depends on | Idempotent? |
|---|---|---|---|---|
| 1. Ingest | Yahoo chart endpoint or committed snapshot | `data/raw/spy_daily.csv` | None | Yes for a fixed provider response; refresh overwrites the snapshot |
| 2. Clean | `data/raw/spy_daily.csv` | `data/processed/spy_clean.csv`, cleaning summary | Ingest | Yes; deterministic validation and sorting |
| 3. Feature | Clean CSV | `data/processed/spy_features.csv`, feature dictionary | Clean | Yes; rolling functions are deterministic |
| 4. Train and score | Feature CSV | `model/model.pkl`, test predictions, model metrics | Feature | Yes for fixed data, split, and seed |
| 5. Evaluate | Predictions and clean data | bootstrap, scenario, subgroup, coefficient tables | Train | Yes with fixed bootstrap seed |
| 6. Report | Evaluation tables and featured data | charts and `reports/final_report.md` | Evaluate | Yes; artifacts are overwritten atomically by path |
| 7. Serve | `model/model.pkl` | Flask responses | Train | No persistent output; repeated requests are read-only |

## Dependency graph

```text
ingest → clean → feature → train → evaluate → report
                              └──────────────→ serve
```

After training, model serving and evaluation/reporting can operate independently. Within reporting, charts can be rendered in parallel once all evaluation tables exist.

## Logging and checkpoints

The raw CSV is the first recovery checkpoint; clean and feature CSVs are subsequent checkpoints. Model and report artifacts include data dates and metrics. CLI logs go to `logs/pipeline.log`, while interactive runs print concise summaries. Each task should log input path, row counts, output path, completion time, and exception type.

## Failure and retry policy

Network ingestion receives up to two retries with exponential delay; schema or validation errors receive no automatic retry because repeating bad input is unsafe. Deterministic local tasks receive one retry after checking disk space and file permissions. Model-evaluation failures stop downstream reporting. A failed refresh preserves the committed raw snapshot and must not overwrite it with partial data.

## Automation boundary

Automate daily ingestion, validation, feature creation, scoring, artifact checks, and alert publication. Keep threshold changes, retraining approval, report interpretation, and portfolio actions manual because they require accountability and business context. Airflow/Prefect is intentionally excluded; the course-scope CLI and scheduler are sufficient.

## Runnable refactor

`src/run_step.py` proves that cleaning can run outside the notebook:

```bash
python -m src.run_step \
  --input data/raw/spy_daily.csv \
  --output data/processed/spy_clean.csv
```

Running it repeatedly produces the same clean CSV for the same raw input.
