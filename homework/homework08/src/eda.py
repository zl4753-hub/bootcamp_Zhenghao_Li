import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis

def eda_summary(df: pd.DataFrame, numeric_cols=None) -> dict:
    """Return dataset profiling stats and flag columns needing attention before modeling."""
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
    out = {
        'shape': df.shape,
        'dtypes': df.dtypes.to_dict(),
        'missing': df.isna().sum().to_dict(),
        'flags': []
    }
    
    # Numeric profile with skew and kurtosis
    profile = df[numeric_cols].describe().T
    profile['skew'] = [skew(df[c].dropna()) for c in profile.index]
    profile['kurtosis'] = [kurtosis(df[c].dropna()) for c in profile.index]
    out['numeric_profile'] = profile
    
    # Stretch Goal: Flag data hygiene issues
    for col in df.columns:
        # High missingness (>30%)
        missing_pct = df[col].isna().mean()
        if missing_pct > 0.3:
            out['flags'].append(f"High missingness in '{col}': {missing_pct:.1%}")
            
        # Zero variance (numeric)
        if col in numeric_cols:
            if df[col].std(ddof=1) == 0:
                out['flags'].append(f"Zero variance in numeric column '{col}'")
        # Dominating category (>90%)
        else:
            top_freq = df[col].value_counts(normalize=True).max() if not df[col].empty else 0
            if top_freq > 0.9:
                out['flags'].append(f"Dominating category in '{col}': {top_freq:.1%}")
                
    return out