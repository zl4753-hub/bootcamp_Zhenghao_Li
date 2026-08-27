# Stage 08: Exploratory Data Analysis (EDA)

## Overview
This directory contains a full exploratory data analysis (EDA) pipeline that profiles distributions, relationships, missingness, and time-series structure to inform downstream preprocessing and modeling.

## Directory Structure
- `data/`: Placeholder directory for raw and processed datasets.
- `src/eda.py`: Reusable module implementing `eda_summary()` with skew/kurtosis calculation and automated data issue flagging.
- `homework08_exploratory-data-analysis_submission.ipynb`: Complete execution notebook featuring univariate/bivariate visualizations, temporal trend analyses, and reflection notes.

## Summary of Results
- **Key Patterns**: High correlation detected between Income/Transactions and Spend.
- **Data Hygiene**: Flagged right-skewed columns and discrete outlier spikes requiring Log-transforms and Winsorization in Stage 09.