from data.data_loader import DataLoader
from indicators.ema import calculate_ema
from indicators.vwap import calculate_intraday_vwap
from indicators.swings import detect_swing_lows

if __name__ == "__main__":
    loader = DataLoader("RELIANCE.NS", period="60d")
    df = loader.get_5m_data()

    df["ema20"] = calculate_ema(df, 20)
    df["vwap"] = calculate_intraday_vwap(df)
    df["swing_low"] = detect_swing_lows(df)

    print(df.tail())