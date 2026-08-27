# Stage 06: Comprehensive Data Preprocessing Pipeline

## Overview
This repository implements a modular and reproducible data preprocessing pipeline designed to handle missing values, drop invalid records, and scale numerical features.

## Directory Structure
- `data/raw/`: Landing directory for immutable raw datasets (`sample_data.csv`).
- `data/processed/`: Storage directory for cleaned and normalized datasets (`sample_data_cleaned.csv`).
- `src/cleaning.py`: Python module containing custom reusable data cleaning functions.
- `homework06_preprocessing_submission.ipynb`: Jupyter Notebook demonstrating pipeline execution and data validation.

## Modular Cleaning Functions
The core transformation logic is encapsulated in `src/cleaning.py`:
1. **`drop_missing(df, columns, threshold)`**: Filters out rows or columns exceeding missingness thresholds.
2. **`fill_missing_median(df, columns)`**: Imputes missing numeric values using the column median.
3. **`normalize_data(df, columns, method)`**: Scales numerical attributes using `MinMaxScaler` or `StandardScaler`.

## Preprocessing Assumptions & Trade-offs
- **Missing Data Mechanism**: Imputing missing numerical values with the median assumes that missingness follows an MCAR (Missing Completely at Random) or MAR (Missing at Random) pattern. Median is chosen over mean to maintain robustness against skewed distributions and outliers.
- **Threshold Drops**: Features or rows missing more than 50% of their values are removed under the assumption that they provide insufficient analytical signal.
- **Feature Scaling**: Applying `MinMaxScaler` bounds features to $[0, 1]$, which preserves zero values and distance ratios for downstream algorithm input.

## Usage & Reproducibility
To execute the pipeline, activate the virtual environment and run the submission notebook:
```bash
source .venv/bin/activate
jupyter notebook homework/homework06/homework06_preprocessing_submission.ipynb