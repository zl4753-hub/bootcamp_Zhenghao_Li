# Outlier policy

Daily returns are flagged when their robust median/MAD z-score exceeds 5 in absolute value. The baseline pipeline **retains** these observations because large market moves are precisely the risk events the model is meant to recognize. Deleting them would make average diagnostics appear cleaner while weakening crisis relevance.

Winsorization is available only as a sensitivity tool in `src/outliers.py`. Any clipped scenario must be labeled and compared with the untouched baseline. Invalid OHLC records—nonpositive prices, missing dates, or high below low—are data-quality failures and are removed during cleaning; genuine extreme returns are not treated as bad data.
