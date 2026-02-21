from data.data_loader import DataLoader
from indicators.ema import calculate_ema
from indicators.vwap import calculate_intraday_vwap
from indicators.swings import detect_swing_lows
from indicators.atr import calculate_atr
from strategy.pullback_v1 import PullbackStrategyV1
from engine.simulator import EventDrivenSimulator
from analytics.metrics import PerformanceAnalyzer


tickers = [
    "ADANIENT.NS","ADANIPORTS.NS","APOLLOHOSP.NS","ASIANPAINT.NS",
    "AXISBANK.NS","BAJAJ-AUTO.NS","BAJFINANCE.NS","BAJAJFINSV.NS",
    "BEL.NS","BHARTIARTL.NS","BPCL.NS","BRITANNIA.NS",
    "CIPLA.NS","COALINDIA.NS","DIVISLAB.NS","DRREDDY.NS",
    "EICHERMOT.NS","GRASIM.NS","HCLTECH.NS","HDFCBANK.NS",
    "HDFCLIFE.NS","HEROMOTOCO.NS","HINDALCO.NS","HINDUNILVR.NS",
    "ICICIBANK.NS","INDUSINDBK.NS","INFY.NS","ITC.NS",
    "JSWSTEEL.NS","KOTAKBANK.NS","LT.NS","M&M.NS",
    "MARUTI.NS","NESTLEIND.NS","NTPC.NS","ONGC.NS",
    "POWERGRID.NS","RELIANCE.NS","SBILIFE.NS","SBIN.NS",
    "SHRIRAMFIN.NS","SUNPHARMA.NS","TATACONSUM.NS","TATAMOTORS.NS",
    "TATASTEEL.NS","TCS.NS","TECHM.NS","TITAN.NS",
    "ULTRACEMCO.NS","WIPRO.NS"
]

all_trades = []
strategy = PullbackStrategyV1()

index_loader = DataLoader("^NSEI")

df_index_15m = index_loader.get_15m_data(local=True)
df_index_15m["ema20"] = calculate_ema(df_index_15m, 20)
df_index_15m["ema50"] = calculate_ema(df_index_15m, 50)

for ticker in tickers:

    print(f"\nRunning backtest for {ticker}")

    loader = DataLoader(ticker)

    try:
        df_5m = loader.get_5m_data(local=True)
        df_15m = loader.get_15m_data(local=True)
    except Exception as e:
        print(f"Skipping {ticker}: {e}")
        continue

    df_5m["ema20"] = calculate_ema(df_5m, 20)
    df_5m["ema50"] = calculate_ema(df_5m, 50)
    df_5m["vwap"] = calculate_intraday_vwap(df_5m)
    df_5m["swing_low"] = detect_swing_lows(df_5m)
    df_5m["atr"] = calculate_atr(df_5m, 14)
    df_5m["atr_mean"] = df_5m["atr"].rolling(50).mean()

    df_15m["ema20"] = calculate_ema(df_15m, 20)
    df_15m["ema50"] = calculate_ema(df_15m, 50)

    simulator = EventDrivenSimulator(strategy)
    trades = simulator.run(df_5m, df_15m)

    print(f"Trades for {ticker}: {len(trades)}")

    all_trades.extend(trades)


print("\n=== PORTFOLIO RESULTS ===")

if len(all_trades) == 0:
    print("No trades generated.")
else:
    analyzer = PerformanceAnalyzer(all_trades)

    print("Total Trades:", len(all_trades))
    print("Win Rate:", analyzer.win_rate())
    print("Profit Factor:", analyzer.profit_factor())
    print("Expectancy:", analyzer.expectancy())
    print("Max Drawdown:", analyzer.max_drawdown())
    print("Sharpe Ratio:", analyzer.sharpe_ratio())