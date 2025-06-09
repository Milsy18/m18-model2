import pandas as pd

def compute_total_score(df: pd.DataFrame) -> pd.Series:
    """
    Stub for total_score:
    Will compute trendScore, momScore, vtyScore, volScore
    and return their sum as a pandas Series named 'total_score'.
    """
    # TODO: replace with real implementation
    return pd.Series(0, index=df.index, name="total_score")
