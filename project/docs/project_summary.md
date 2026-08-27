# SPY Next-Day High-Volatility Risk Monitor

## The problem

Portfolio risk managers do not only care whether the equity market will rise or fall. They also need to know when the size of the next move may be unusually large. A large move in either direction can create hedge slippage, limit breaches, liquidity needs, and difficult conversations with stakeholders. This project builds an end-of-day warning signal for that narrower and more defensible question: given information available after today's close, how likely is SPY to experience a high-volatility return tomorrow?

“High volatility” is defined relative to recent history. A day is labeled high risk when the following session's absolute close-to-close return exceeds the 75th percentile of absolute returns observed over the trailing 252 sessions. This definition adapts to changing market conditions and avoids using a fixed percentage that could become irrelevant. It is also a policy choice, not a natural law, so the project explicitly tests 70th-, 75th-, and 80th-percentile alternatives.

## What was built

The project follows the full financial-engineering lifecycle. A reproducible ingestion module downloads daily SPY open, high, low, close, adjusted close, and volume data from Yahoo Finance. A committed raw snapshot covers August 2016 through August 2026 so the analysis can run without depending on live network access. Cleaning code validates dates and prices, removes duplicates and invalid records, and records a cleaning summary. Extreme returns are flagged using a robust median/MAD statistic but retained because crisis observations are the events the monitor should learn from.

Feature engineering produces eleven variables known at the current close: current and lagged returns, five- and twenty-session momentum, volatility over five, twenty, and sixty sessions, the daily high-low range, five-session volume change, distance from the twenty-day average, and drawdown from the sixty-day high. The target uses the next session, while its threshold uses only current and past returns. This separation is essential: using tomorrow's information in today's features would create leakage and unrealistic performance.

A chronological split assigns the earliest 80% of rows to training and the latest 20% to testing. No random shuffling is used. A scikit-learn Pipeline standardizes features using training data and fits a class-balanced logistic regression. Logistic regression was selected because its probability output is useful for escalation, its coefficients are inspectable, and its complexity is appropriate for the course and dataset. The saved joblib bundle contains the model, feature order, decision threshold, training date, and target definition.

## What was found

On 491 out-of-sample sessions, ROC-AUC is 0.716. A 600-resample bootstrap gives a 95% interval of 0.661 to 0.768, so the model appears to rank risk better than chance, although the uncertainty is material. F1 is 0.478, precision 0.469, and recall 0.488. Accuracy is 0.733, slightly below the 0.749 majority-class benchmark. That result is not a contradiction: predicting only the common normal-volatility class can produce high accuracy while failing to identify high-risk days. The model should therefore be judged by ranking ability, recall, precision, and decision costs rather than accuracy alone.

The confusion matrix contains 60 correctly identified high-risk days, 63 missed high-risk days, 68 false alerts, and 300 correctly identified normal days. At the default 50% probability cutoff, roughly half of realized high-risk days are detected. This is not adequate for autonomous action, but it can be useful as one signal in a human review process if the cost of review is low and the risk manager understands the miss rate.

Sensitivity analysis shows that results depend on the risk definition. At the 70th-percentile threshold, ROC-AUC is 0.706 and F1 0.480. At 75%, they are 0.716 and 0.478. At 80%, ROC-AUC rises to 0.750 and F1 to 0.493, while positive cases become rarer. The model's qualitative ranking ability survives these choices, but operational alert frequency and precision/recall do not. The risk manager must therefore own the target definition and cutoff.

Subgroup analysis reveals the most important hidden weakness. During periods below the 50-day moving average, F1 is 0.662 and ROC-AUC 0.621. During periods above the trend, F1 falls to 0.214 even though ROC-AUC is 0.648. High-volatility events are much more common below trend, so the model and threshold behave differently across regimes. Aggregate metrics conceal this difference. Monitoring should report both regimes and treat above-trend false negatives as a specific model risk.

## What should not be relied on

The signal is not a forecast of direction, a causal model, or a complete portfolio risk system. It uses SPY only and does not measure position-level sensitivities, options exposures, correlations, liquidity, leverage, or overnight gaps directly. Coefficients represent conditional associations among correlated engineered features; they should not be interpreted as causal drivers. Historical performance may fail during a structural break, provider data can change, and end-of-day signals arrive too late for intraday protection.

The 50% alert cutoff has not been optimized against a formal cost matrix. False alerts consume analyst attention, while missed events may be far more expensive. The current evaluation treats each day equally and omits trading costs, hedge costs, taxes, and downstream business outcomes. The committed data snapshot supports reproducibility but should not be confused with independent validation.

## Recommended use and next steps

Use the probability as an input to an end-of-day risk review. A score above 50% should prompt a human to inspect equity exposure, volatility, drawdown, scheduled events, and hedge capacity. It should not automatically change positions. Every displayed score should include the data date, model training date, target definition, and stale-data status.

Operationally, monitor daily freshness and schema, feature null rates, alert frequency, rolling recall and ROC-AUC, API latency, and the number of missed high-risk days. Pause scoring when data are stale or invalid. Review performance weekly, retrain quarterly, and require two consecutive threshold breaches before initiating unscheduled retraining. Risk Analytics owns the model, Data Engineering owns ingestion, Platform owns service health, and the portfolio risk manager owns the business cutoff.

Future work should validate the pipeline against an independent price source, add VIX and overnight-gap information, assess probability calibration, and build an explicit cost-weighted threshold analysis. A rolling or expanding-window backtest across more regimes would give stronger evidence than one holdout period. Only after those checks should the signal be considered for integration with a live portfolio process.
