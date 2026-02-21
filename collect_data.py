import os
from data.collector import IntradayDataCollector

# Full NIFTY 50
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

for ticker in tickers:

    file_5m = f"data/{ticker}_5m.csv"
    file_15m = f"data/{ticker}_15m.csv"

    if os.path.exists(file_5m) and os.path.exists(file_15m):
        print(f"✔ {ticker} already downloaded. Skipping.")
        continue

    print(f"\nCollecting data for {ticker}")

    collector_5m = IntradayDataCollector(ticker, interval="5m")
    collector_5m.collect(months=2)   # 60-day max

    collector_15m = IntradayDataCollector(ticker, interval="15m")
    collector_15m.collect(months=2)