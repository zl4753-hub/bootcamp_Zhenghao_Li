# Stage 07: Outliers & Risk Assumptions

## Overview
This module implements robust outlier detection (IQR & Z-score) and handling strategies (Filtering & Winsorization) alongside a sensitivity analysis measuring their impacts on linear regression modeling.

## Directory Structure
- `data/raw/outliers_homework.csv`: Generated synthetic return dataset with extreme shock events.
- `src/outliers.py`: Reusable python functions for IQR detection, Z-score detection, and Winsorization.
- `homework07_outliers-risk-assumptions_submission.ipynb`: Execution notebook containing detection pipeline, visualizations, and model sensitivity comparisons.

## Core Findings
1. **Outlier Influence**: Extreme shock values significantly inflate standard deviation and distort linear regression slope estimates.
2. **Trade-offs**: Filtering outliers improves baseline model $R^2$ and MAE, but risks ignoring real physical or economic tail events (e.g., financial black swan events).