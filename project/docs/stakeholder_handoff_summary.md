# Stakeholder handoff summary

## Overview and purpose

This project estimates the probability that SPY will experience an unusually large absolute return on the next trading day. It supports an end-of-day portfolio risk review; it does not recommend direction, position size, or automatic trades.

## Findings and recommendation

The chronological test achieves ROC-AUC 0.716 with a 600-resample 95% interval of 0.661–0.768. F1 is 0.478. Accuracy is below the majority-class benchmark, reinforcing that risk ranking, recall, and false-alert tradeoffs matter more than headline accuracy. Use probability above 50% to trigger human review, not an automatic exposure change.

## Assumptions, limitations, and risks

The signal assumes historical end-of-day SPY behavior remains informative. It depends on a rolling 75th-percentile definition of high volatility and can deteriorate during structural breaks. Performance is weaker above the 50-day trend than below it. Provider schema changes, stale data, correlated rolling features, and delayed labels are material risks.

## Using the deliverables

Run `notebooks/project_pipeline.ipynb` top to bottom to recreate data products, model, evaluation tables, charts, and report. Read `reports/final_report.md` for the decision-facing result. Start `python app.py` and call `/metadata`, `/health`, then `/predict` for model serving. Use `docs/monitoring_plan.md` and `docs/orchestration_plan.md` for operations.

## Suggested next steps

Validate against an independent data source, evaluate probability calibration, incorporate VIX or realized-range features, and test explicit decision costs. Collect at least one additional market regime before changing the 50% review threshold.
