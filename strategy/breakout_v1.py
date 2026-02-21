import pandas as pd

class BreakoutStrategyV1:
    """
    Implements:
    - 15m EMA bias
    - VWAP filter
    - 5m 20-candle breakout (close confirmation)
    """

    def __init__(self):
        pass

    def check_long_signal(self, df_5m: pd.DataFrame, df_15m: pd.DataFrame, current_time) -> bool:
        """
        Returns True if LONG entry conditions are met at current_time.
        """

        # Ensure enough history
        if len(df_5m) < 25:
            return False

        # --- 1. Time filter ---
        if not self._within_trading_window(current_time):
            return False

        # --- 2. Get latest 15m candle before current time ---
        df_15m_filtered = df_15m[df_15m.index <= current_time]

        if df_15m_filtered.empty:
            return False

        latest_15m = df_15m_filtered.iloc[-1]

        # --- 3. Bias check ---
        if latest_15m["ema20"] <= latest_15m["ema50"]:
            return False

        # --- 4. VWAP alignment ---
        latest_5m = df_5m.loc[current_time]

        if latest_5m["close"] <= latest_5m["vwap"]:
            return False
        
        # --- 5. Volatility contraction filter ---
        latest_5m = df_5m.loc[current_time]

        if latest_5m["atr"] >= latest_5m["atr_mean"]:
            return False

        # --- 6. Breakout condition ---
        previous_20 = df_5m[df_5m.index < current_time].iloc[-20:]

        highest_high = previous_20["high"].max()

        if latest_5m["close"] <= highest_high:
            return False

        return True

    def _within_trading_window(self, timestamp):
        """
        Allow trading between 9:45 and 14:45.
        """
        hour = timestamp.hour
        minute = timestamp.minute

        total_minutes = hour * 60 + minute
        start = 9 * 60 + 45
        end = 14 * 60 + 45

        return start <= total_minutes <= end