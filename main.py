from data.data_loader import DataLoader
from indicators.ema import calculate_ema
from indicators.vwap import calculate_intraday_vwap
from indicators.swings import detect_swing_lows
from strategy.breakout_v1 import BreakoutStrategyV1
from engine.simulator import EventDrivenSimulator
from analytics.metrics import PerformanceAnalyzer

if __name__ == "__main__":
    loader = DataLoader("RELIANCE.NS", period="60d")

    df_5m = loader.get_5m_data()
    df_15m = loader.get_15m_data()

    # Add indicators
    df_5m["ema20"] = calculate_ema(df_5m, 20)
    df_5m["ema50"] = calculate_ema(df_5m, 50)
    df_5m["vwap"] = calculate_intraday_vwap(df_5m)
    df_5m["swing_low"] = detect_swing_lows(df_5m)

    df_15m["ema20"] = calculate_ema(df_15m, 20)
    df_15m["ema50"] = calculate_ema(df_15m, 50)

    strategy = BreakoutStrategyV1()

    sim = EventDrivenSimulator(strategy)

    for timestamp in df_5m.index:
        if strategy.check_long_signal(df_5m, df_15m, timestamp):
            print("Signal at:", timestamp)

    trades = sim.run(df_5m, df_15m)

    print(trades[:5])
    print("Total trades:", len(trades))

    analyzer = PerformanceAnalyzer(trades)

    print("Win Rate:", analyzer.win_rate())
    print("Profit Factor:", analyzer.profit_factor())
    print("Expectancy:", analyzer.expectancy())
    print("Max Drawdown:", analyzer.max_drawdown())
    print("Sharpe Ratio:", analyzer.sharpe_ratio())