# Problem framing and scope

## Stakeholder-centered question

A portfolio risk manager needs a repeatable end-of-day signal answering: **How likely is SPY to experience an unusually large absolute return during the next trading session?** The signal is intended to prioritize human review of equity exposure, hedges, and operational readiness. It is not an autonomous trading instruction and does not forecast return direction.

## Scope

- Instrument: SPDR S&P 500 ETF Trust (`SPY`).
- Observation frequency: daily OHLCV data.
- Decision time: after the current session closes.
- Target: next-day absolute return above the trailing 252-session 75th percentile known at the current close.
- Modeling track: time-aware binary classification.
- Primary metrics: ROC-AUC, recall, precision, and F1; accuracy is reported but not privileged because high-risk days are the minority class.

## Constraints and assumptions

The project uses a public Yahoo Finance chart endpoint and a committed snapshot for reproducibility. Historical relationships may fail under structural breaks. End-of-day data cannot support intraday intervention. The analysis excludes trading costs, taxes, liquidity, position-level exposures, and causal claims.

## Deliverable mapping

The pipeline notebook demonstrates the full lifecycle; `src/` contains reusable production-oriented functions; `reports/final_report.md` is the risk-manager deliverable; `app.py` serves the saved model; monitoring and orchestration plans describe how the system would operate after handoff.
