import pandas as pd


class EventDrivenSimulator:

    def __init__(self, strategy, initial_capital=100000, risk_percent=0.01):
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.risk_percent = risk_percent
        self.trades = []

    def run(self, df_5m: pd.DataFrame, df_15m: pd.DataFrame):
        trade_taken_dates = set()

        for i in range(20, len(df_5m) - 1):

            current_time = df_5m.index[i]
            current_date = current_time.date()

            # Skip if trade already taken today
            if current_date in trade_taken_dates:
                continue

            if self.strategy.check_long_signal(df_5m.iloc[:i+1], df_15m, current_time):

                entry_candle = df_5m.iloc[i + 1]
                entry_price = entry_candle["open"]

                # Determine stop using last confirmed swing low
                stop_price = self._find_recent_swing_low(df_5m.iloc[:i+1])

                if stop_price is None:
                    continue

                risk_per_share = entry_price - stop_price

                if risk_per_share <= 0:
                    continue

                risk_amount = self.initial_capital * self.risk_percent
                quantity = int(risk_amount / risk_per_share)

                if quantity <= 0:
                    continue

                target_price = entry_price + 2 * risk_per_share

                exit_price, outcome = self._simulate_trade(
                    df_5m.iloc[i+1:], entry_price, stop_price, target_price
                )

                pnl = (exit_price - entry_price) * quantity
                trade_value = entry_price * quantity
                slippage_cost = trade_value * 0.0005  # 0.05%
                brokerage = 40

                pnl -= (slippage_cost + brokerage)

                self.trades.append({
                    "date": current_date,
                    "entry": entry_price,
                    "stop": stop_price,
                    "target": target_price,
                    "exit": exit_price,
                    "pnl": pnl,
                    "outcome": outcome
                })

                trade_taken_dates.add(current_date)

        return self.trades

    def _find_recent_swing_low(self, df):
        recent = df[df["swing_low"] == True]

        if recent.empty:
            return None

        return recent.iloc[-1]["low"]

    def _simulate_trade(self, df_after_entry, entry, stop, target):

        for _, candle in df_after_entry.iterrows():

            if candle["low"] <= stop:
                return stop, "LOSS"

            if candle["high"] >= target:
                return target, "WIN"

        return entry, "NO_EXIT"