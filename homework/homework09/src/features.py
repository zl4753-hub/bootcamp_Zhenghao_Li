import pandas as pd
import numpy as np

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Creates engineered features for financial default modeling:
    1. spend_income_ratio (Ratio/Interaction)
    2. rolling_spend_mean (Temporal Windowing)
    3. region_freq (Categorical Frequency Encoding)
    """
    df = df.copy()
    
    # 1. Spend-to-income ratio
    df['spend_income_ratio'] = df['monthly_spend'] / df['income']
    
    # 2. 3-period rolling average spend
    df['rolling_spend_mean'] = df['monthly_spend'].rolling(window=3, min_periods=1).mean()
    
    # 3. Frequency encoding for region
    region_freq = df['region'].value_counts(normalize=True)
    df['region_freq'] = df['region'].map(region_freq)
    
    return df
