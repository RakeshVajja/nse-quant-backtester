import pandas as pd


def calculate_ema(df: pd.DataFrame, period: int, column: str = "close") -> pd.Series:
    """
    Calculate Exponential Moving Average.
    """
    return df[column].ewm(span=period, adjust=False).mean()