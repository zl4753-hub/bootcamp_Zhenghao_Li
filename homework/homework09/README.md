# Homework 09: Feature Engineering

## Summary
Created 3 domain-driven features based on findings from Stage 08 EDA:
1. `spend_income_ratio`: Ratio of monthly spending relative to income to measure spending proportion.
2. `rolling_spend_mean`: 3-period rolling average of spend to smooth short-term monthly volatility.
3. `region_freq`: Frequency encoding for categorical region values to preserve category weight without expanding feature space.

## Directory Structure
- `src/features.py`: Module exporting `create_features()`.
- `homework09_feature-engineering_submission.ipynb`: Execution notebook containing feature calculations, Stage 08 rationales, and target correlation checks.