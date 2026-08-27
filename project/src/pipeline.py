"""End-to-end SPY high-volatility risk pipeline."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.cleaning import clean_ohlcv, cleaning_summary
from src.config import PROJECT_ROOT, ensure_project_dirs
from src.eda import eda_summary
from src.evaluation import bootstrap_metric_ci, evaluate_target_scenarios, subgroup_metrics
from src.features import build_features, feature_dictionary
from src.ingestion import load_or_fetch
from src.modeling import coefficient_table, fit_risk_classifier, save_model
from src.outliers import flag_return_outliers
from src.reporting import create_figures
from src.storage import save_csv
from src.utils import write_json


def write_stakeholder_report(metrics, bootstrap, scenarios, subgroups, featured, path: Path) -> None:
    """Write a concise risk-manager report from verified pipeline outputs."""
    latest = featured.iloc[-1]
    scenario_lines = "\n".join(
        f"| {row.scenario} | {row.positive_rate:.1%} | {row.f1:.3f} | {row.roc_auc:.3f} |"
        for row in scenarios.itertuples()
    )
    subgroup_lines = "\n".join(
        f"| {row.market_regime} | {row.rows} | {row.positive_rate:.1%} | {row.f1:.3f} | {row.roc_auc:.3f} |"
        for row in subgroups.itertuples()
    )
    report = f"""# SPY Next-Day High-Volatility Risk Monitor

**Audience:** Portfolio risk manager
**Data through:** {latest['date'].date().isoformat()}

## Executive summary

- The out-of-sample model achieves **ROC-AUC {metrics['roc_auc']:.3f}** and **F1 {metrics['f1']:.3f}** when identifying next-day high-volatility regimes.
- The bootstrap 95% interval for ROC-AUC is **[{bootstrap['lo']:.3f}, {bootstrap['hi']:.3f}]**; this range should travel with the point estimate.
- Use the score as an escalation signal, not an automatic trading instruction. Review exposure when predicted probability exceeds 50%, especially when short- and medium-horizon volatility are both rising.

## Market context

![SPY price and volatility](images/price_and_volatility.png)

The model uses only information available after the current session closes. Rolling volatility and drawdown summarize the risk regime; jumps are retained because deleting crisis observations would hide the events the monitor is designed to flag.

## Out-of-sample performance

![Confusion matrix](images/confusion_matrix.png)

Accuracy is **{metrics['accuracy']:.3f}**, precision **{metrics['precision']:.3f}**, and recall **{metrics['recall']:.3f}**. The majority-class accuracy baseline is **{metrics['majority_accuracy']:.3f}**. A missed high-risk day is more costly than a false alert, so recall and probability calibration matter more than accuracy alone.

## Assumption sensitivity

![Scenario sensitivity](images/scenario_sensitivity.png)

| High-risk definition | Positive rate | F1 | ROC-AUC |
|---|---:|---:|---:|
{scenario_lines}

Changing the rolling threshold from the 70th to the 80th percentile changes both class balance and performance. The conclusion holds only if “high volatility” is defined consistently with the risk manager's escalation policy.

## Subgroup diagnostic

![Subgroup performance](images/subgroup_performance.png)

| Trend regime | Rows | Positive rate | F1 | ROC-AUC |
|---|---:|---:|---:|---:|
{subgroup_lines}

Performance differences across above- and below-trend periods reveal where aggregate metrics can conceal failure. Use the weaker regime's results when setting operational expectations.

## Feature interpretation

![Feature coefficients](images/feature_coefficients.png)

Coefficients describe conditional association after scaling; they do **not** establish causality. Highly correlated rolling-volatility features can redistribute coefficient weight without changing prediction quality.

## Assumptions and risks

- Historical SPY behavior is assumed to remain relevant; structural breaks can invalidate the relationship.
- Prices are end-of-day and the signal is not available before the close.
- The target is based on a trailing 252-session quantile, so its business meaning depends on that definition.
- Yahoo data availability, corporate-action adjustments, schema drift, and delayed labels can interrupt or distort the pipeline.
- The analysis excludes trading costs, taxes, liquidity, portfolio constraints, and the economic cost of false alerts.

## What this means for you

Use predicted probability as one input to a daily risk review. Escalate for human review above 50%; do not automatically trade. Monitor feature null rates, data freshness, alert frequency, rolling recall/AUC, and API latency. Retrain or pause the service if rolling ROC-AUC falls below 0.55, input nulls exceed 1%, or the daily file is more than one business day stale.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")


def run_full_pipeline(refresh: bool = False) -> dict:
    """Run ingestion through stakeholder delivery using committed project paths."""
    ensure_project_dirs()
    raw_path = PROJECT_ROOT / "data/raw/spy_daily.csv"
    raw = load_or_fetch(raw_path, refresh=refresh)
    clean = clean_ohlcv(raw)
    flagged = flag_return_outliers(clean)
    featured = build_features(flagged, target_quantile=0.75)

    save_csv(clean, PROJECT_ROOT / "data/processed/spy_clean.csv")
    save_csv(featured, PROJECT_ROOT / "data/processed/spy_features.csv")
    eda_summary(featured).to_csv(PROJECT_ROOT / "reports/eda_summary.csv")
    write_json(cleaning_summary(raw, clean), PROJECT_ROOT / "reports/cleaning_summary.json")
    write_json(feature_dictionary(), PROJECT_ROOT / "docs/feature_dictionary.json")

    bundle, train, test, scored, metrics = fit_risk_classifier(featured)
    save_model(bundle, PROJECT_ROOT / "model/model.pkl")
    save_csv(scored, PROJECT_ROOT / "data/processed/test_predictions.csv")
    write_json(metrics, PROJECT_ROOT / "reports/model_metrics.json")

    bootstrap = bootstrap_metric_ci(
        scored["target_high_vol_next"], scored["predicted_probability"], n_boot=600
    )
    write_json(
        {key: value for key, value in bootstrap.items() if key != "samples"},
        PROJECT_ROOT / "reports/bootstrap_roc_auc.json",
    )
    scenarios = evaluate_target_scenarios(clean)
    subgroups = subgroup_metrics(scored)
    coefficients = coefficient_table(bundle)
    save_csv(scenarios, PROJECT_ROOT / "reports/scenario_results.csv")
    save_csv(subgroups, PROJECT_ROOT / "reports/subgroup_results.csv")
    save_csv(coefficients, PROJECT_ROOT / "reports/feature_coefficients.csv")
    create_figures(featured, scored, scenarios, subgroups, coefficients, PROJECT_ROOT / "reports")
    write_stakeholder_report(
        metrics,
        bootstrap,
        scenarios,
        subgroups,
        featured,
        PROJECT_ROOT / "reports/final_report.md",
    )
    return {
        "raw_rows": len(raw),
        "featured_rows": len(featured),
        "train_rows": len(train),
        "test_rows": len(test),
        "data_start": featured["date"].min().date().isoformat(),
        "data_end": featured["date"].max().date().isoformat(),
        "metrics": metrics,
        "bootstrap_roc_auc": {key: value for key, value in bootstrap.items() if key != "samples"},
    }
