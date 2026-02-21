import pandas as pd


class PullbackStrategyV1:

    def __init__(self):
        pass

    def check_long_signal(self, df_5m: pd.DataFrame,
                          df_15m: pd.DataFrame,
                          current_time) -> bool:

        if len(df_5m) < 20:
            return False

        # ---- 1️⃣ Time filter ----
        if not self._within_trading_window(current_time):
            return False

        # ---- 2️⃣ 15m Trend Bias ----
        df_15m_filtered = df_15m[df_15m.index <= current_time]

        if df_15m_filtered.empty:
            return False

        latest_15m = df_15m_filtered.iloc[-1]

        if latest_15m["ema20"] <= latest_15m["ema50"]:
            return False

        # ---- 3️⃣ Pullback Condition ----
        latest_5m = df_5m.loc[current_time]

        # Must be near VWAP (within 0.2%)
        if abs(latest_5m["close"] - latest_5m["vwap"]) / latest_5m["vwap"] > 0.002:
            return False

        # ---- 4️⃣ Bullish Engulfing Trigger ----
        prev = df_5m.iloc[-2]
        curr = latest_5m

        if not (
            curr["close"] > curr["open"] and
            prev["close"] < prev["open"] and
            curr["close"] > prev["open"] and
            curr["open"] < prev["close"]
        ):
            return False

        return True

    def _within_trading_window(self, timestamp):

        hour = timestamp.hour
        minute = timestamp.minute

        total_minutes = hour * 60 + minute
        start = 9 * 60 + 45
        end = 14 * 60 + 45

        return start <= total_minutes <= end