import yfinance as yf
import pandas as pd


class DataLoader:
    """
    Responsible ONLY for fetching and cleaning historical data.
    No strategy logic allowed here.
    """

    def __init__(self, ticker: str, period: str = "60d"):
        self.ticker = ticker
        self.period = period

    def get_5m_data(self) -> pd.DataFrame:
        """
        Fetch 5-minute historical data.
        """
        df = yf.download(
            self.ticker,
            period=self.period,
            interval="5m",
            auto_adjust=False,
            progress=False
        )

        return self._clean_data(df)

    def get_15m_data(self) -> pd.DataFrame:
        """
        Fetch 15-minute historical data.
        """
        df = yf.download(
            self.ticker,
            period=self.period,
            interval="15m",
            auto_adjust=False,
            progress=False
        )

        return self._clean_data(df)

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize and clean dataframe.
        """

        if df.empty:
            raise ValueError(f"No data returned for {self.ticker}")

        # Flatten MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Ensure datetime index
        df.index = pd.to_datetime(df.index)

        # Standardize column names
        df.columns = [str(col).lower() for col in df.columns]

        # Drop missing rows
        df = df.dropna()

        # Sort index
        df = df.sort_index()

        return df