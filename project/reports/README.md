# Stakeholder deliverables

The primary audience is a portfolio risk manager deciding whether next-day SPY volatility warrants additional human review. Markdown is used because it renders directly in GitHub, keeps assumptions beside charts, and remains easy to version and reproduce.

- `final_report.md`: decision-facing report generated from verified outputs.
- `images/`: self-contained charts used in the report.
- `model_metrics.json`: baseline test metrics.
- `bootstrap_roc_auc.json`: 600-resample uncertainty interval.
- `scenario_results.csv`: target-definition sensitivity.
- `subgroup_results.csv`: trend-regime diagnostics.
- `feature_coefficients.csv`: standardized association summary.
