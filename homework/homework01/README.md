# Fed Rate Decisions & USD/CNY Exchange Rate Volatility

**Stage:** Problem Framing & Scoping (Stage 01)

## Problem Statement
Monetary policy divergence between the US Federal Reserve and the People's Bank of China (PBOC) creates significant volatility in the USD/CNY exchange rate. Shifts in the Federal Funds Rate alter yield differentials, driving cross-border capital flows that directly impact FX risk for international traders, multinational corporations, and global asset managers.

## Stakeholder & User
* **Primary Stakeholder:** Chief Risk Officer / Corporate Treasurer managing cross-border US-China operations, or an FX Portfolio Manager.
* **End User:** FX Analyst / Hedging Specialist responsible for executing dynamic currency hedges and evaluating quarterly exchange rate risks.

## Useful Answer & Decision
* **Type:** Causal & Predictive
* **Metric & Artifact:** Econometric sensitivity metrics (beta/elasticity) and predictive ML models paired with an interactive risk dashboard providing scenario analysis (e.g., sensitivity of USD/CNY to 25/50 bps Fed rate changes).

## Assumptions & Constraints
* **Assumptions:** Historical interest rate differentials (US 10-Yr Treasury vs. China 10-Yr CGB) serve as a primary proxy for monetary policy divergence.
* **Constraints:** Non-market factors (PBOC daily fixing counter-cyclical factors, capital controls, trade policies) introduce regime shifts that market-based models may miss.

## Known Unknowns / Risks
* **Central Bank Intervention:** PBOC policy intervention can temporarily decouple USD/CNY from interest rate parity.
* **Structural Breaks:** Geopolitical shifts or macroeconomic shocks can alter historical correlations between rates and exchange rates.

## Lifecycle Mapping
- **Goal:** Quantify Fed rate impact on USD/CNY → **Stage:** Problem Framing & Scoping (Stage 01) → **Deliverable:** Scoping README & Stakeholder Memo

## Repo Plan
- `data/`: Raw and processed interest rate / FX time series.
- `src/`: Data processing and analysis scripts.
- `notebooks/`: Exploratory data analysis and model building.
- `docs/`: Stakeholder briefs, memos, and project documentation.
