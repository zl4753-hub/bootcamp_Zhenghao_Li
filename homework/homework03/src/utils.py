import pandas as pd

def get_summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """返回数据集的描述性统计摘要"""
    return df.describe()
