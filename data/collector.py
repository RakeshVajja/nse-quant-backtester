import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time


class IntradayDataCollector:
    """
    Collect rolling intraday data (5m or 15m) month by month.
    Saves cleaned CSV locally.
    """

    def __init__(self, ticker, interval="5m"):
        self.ticker = ticker
        self.interval = interval

    def collect(self, months=12):

        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        all_data = []

        for i in range(months):

            print(f"[{self.ticker}] Downloading {self.interval} "
                  f"{start_date.date()} → {end_date.date()}")

            df = yf.download(
                self.ticker,
                start=start_date,
                end=end_date,
                interval=self.interval,
                progress=False
            )

            if not df.empty:
                df.index = pd.to_datetime(df.index)
                all_data.append(df)

            # Move window backward
            end_date = start_date
            start_date = end_date - timedelta(days=30)

            time.sleep(1)  # avoid Yahoo throttling

        if not all_data:
            print(f"No data downloaded for {self.ticker}")
            return

        combined = pd.concat(all_data)
        combined = combined[~combined.index.duplicated(keep="first")]
        combined = combined.sort_index()

        filename = f"data/{self.ticker}_{self.interval}.csv"
        combined.to_csv(filename)

        print(f"Saved → {filename}")