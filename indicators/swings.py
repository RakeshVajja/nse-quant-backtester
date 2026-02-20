import pandas as pd


def detect_swing_lows(df: pd.DataFrame) -> pd.Series:
    """
    Detect confirmed swing lows using 2-candle confirmation.
    """

    swing_low = (
        (df["low"] < df["low"].shift(1)) &
        (df["low"] < df["low"].shift(2)) &
        (df["low"] < df["low"].shift(-1)) &
        (df["low"] < df["low"].shift(-2))
    )

    return swing_low


def detect_swing_highs(df: pd.DataFrame) -> pd.Series:
    """
    Detect confirmed swing highs using 2-candle confirmation.
    """

    swing_high = (
        (df["high"] > df["high"].shift(1)) &
        (df["high"] > df["high"].shift(2)) &
        (df["high"] > df["high"].shift(-1)) &
        (df["high"] > df["high"].shift(-2))
    )

    return swing_high