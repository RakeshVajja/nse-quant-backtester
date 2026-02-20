import pandas as pd


def calculate_intraday_vwap(df: pd.DataFrame) -> pd.Series:
    """
    Calculate intraday VWAP with daily reset.
    """

    df = df.copy()
    df["date"] = df.index.date

    vwap_series = []

    for date, group in df.groupby("date"):
        cumulative_pv = (group["close"] * group["volume"]).cumsum()
        cumulative_volume = group["volume"].cumsum()
        vwap = cumulative_pv / cumulative_volume
        vwap_series.append(vwap)

    return pd.concat(vwap_series)