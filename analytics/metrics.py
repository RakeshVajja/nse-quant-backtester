import numpy as np
import pandas as pd


class PerformanceAnalyzer:

    def __init__(self, trades, initial_capital=100000):
        self.trades = trades
        self.initial_capital = initial_capital

        if len(trades) == 0:
            raise ValueError("No trades to analyze.")

        self.df = pd.DataFrame(trades)

    def win_rate(self):
        wins = (self.df["outcome"] == "WIN").sum()
        return wins / len(self.df)

    def profit_factor(self):
        gross_profit = self.df[self.df["pnl"] > 0]["pnl"].sum()
        gross_loss = abs(self.df[self.df["pnl"] < 0]["pnl"].sum())

        if gross_loss == 0:
            return np.inf

        return gross_profit / gross_loss

    def expectancy(self):
        return self.df["pnl"].mean()

    def equity_curve(self):
        equity = [self.initial_capital]
        for pnl in self.df["pnl"]:
            equity.append(equity[-1] + pnl)

        return pd.Series(equity)

    def max_drawdown(self):
        equity = self.equity_curve()
        peak = equity.cummax()
        drawdown = (equity - peak) / peak
        return drawdown.min()

    def sharpe_ratio(self):
        returns = self.df["pnl"] / self.initial_capital
        if returns.std() == 0:
            return 0
        return returns.mean() / returns.std() * np.sqrt(252)