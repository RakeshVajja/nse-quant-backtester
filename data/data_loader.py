import yfinance as yf
import pandas as pd


class DataLoader:

    def __init__(self, ticker: str, period: str = "60d"):
        self.ticker = ticker
        self.period = period

    def get_5m_data(self, local=False):

        if local:
            path = f"data/{self.ticker}_5m.csv"

            df = pd.read_csv(
                path,
                skiprows=3,        # skip Price, Ticker, Datetime rows
                header=None
            )

            df.columns = ["datetime", "close", "high", "low", "open", "volume"]
            df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
            df = df.dropna(subset=["datetime"])
            df = df.set_index("datetime")

            return self._clean_data(df)

        df = yf.download(
            self.ticker,
            period=self.period,
            interval="5m",
            auto_adjust=False,
            progress=False
        )

        return self._clean_data(df)

    def get_15m_data(self, local=False):

        if local:
            path = f"data/{self.ticker}_15m.csv"

            df = pd.read_csv(
                path,
                skiprows=3,
                header=None
            )

            df.columns = ["datetime", "close", "high", "low", "open", "volume"]
            df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
            df = df.dropna(subset=["datetime"])
            df = df.set_index("datetime")

            return self._clean_data(df)

        df = yf.download(
            self.ticker,
            period=self.period,
            interval="15m",
            auto_adjust=False,
            progress=False
        )

        return self._clean_data(df)

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:

        if df.empty:
            raise ValueError(f"No data returned for {self.ticker}")

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df.index = pd.to_datetime(df.index)
        df.columns = [str(col).lower() for col in df.columns]
        df = df.dropna()
        df = df.sort_index()

        return df