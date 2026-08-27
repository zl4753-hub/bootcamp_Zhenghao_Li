import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def fill_missing_median(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """用中位数填充指定数值列的缺失值"""
    df_copy = df.copy()
    if columns is None:
        columns = df_copy.select_dtypes(include=np.number).columns
    for col in columns:
        df_copy[col] = df_copy[col].fillna(df_copy[col].median())
    return df_copy

def drop_missing(df: pd.DataFrame, columns: list = None, threshold: float = None) -> pd.DataFrame:
    """根据列名或有效值比例剔除缺失行"""
    df_copy = df.copy()
    if columns is not None:
        return df_copy.dropna(subset=columns)
    if threshold is not None:
        min_valid = int(threshold * df_copy.shape[1])
        return df_copy.dropna(thresh=min_valid)
    return df_copy.dropna()

def normalize_data(df: pd.DataFrame, columns: list = None, method: str = 'minmax') -> pd.DataFrame:
    """对数值列实施 MinMax 缩放或 StandardScaler 标准化"""
    df_copy = df.copy()
    if columns is None:
        columns = df_copy.select_dtypes(include=np.number).columns
    scaler = MinMaxScaler() if method == 'minmax' else StandardScaler()
    df_copy[columns] = scaler.fit_transform(df_copy[columns])
    return df_copy