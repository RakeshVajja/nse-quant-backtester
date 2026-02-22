from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd

from patterns import detect_patterns

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/stock/{symbol}")
def get_stock(symbol: str, interval: str = "5m"):

    try:
        raw_df = yf.download(
            symbol,
            period="60d",
            interval=interval,
            progress=False
        )

        if raw_df.empty:
            return {"error": "No data found for symbol."}

        # Create cleaned copy
        df = raw_df.copy().reset_index()

        # Flatten MultiIndex safely
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df.columns = [str(col).lower() for col in df.columns]

        patterns = detect_patterns(df)

        return {
            "symbol": symbol,
            "interval": interval,
            "data": df.to_dict(orient="records"),
            "patterns": patterns
        }

    except Exception as e:
        return {"error": str(e)}