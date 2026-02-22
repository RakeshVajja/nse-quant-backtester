def detect_patterns(df):

    priority_order = [
        "Bullish Engulfing",
        "Bearish Engulfing",
        "Hammer",
        "Shooting Star",
        "Doji"
    ]

    patterns = []

    for i in range(1, len(df)):

        prev = df.iloc[i - 1]
        curr = df.iloc[i]

        detected = []

        open_ = curr["open"]
        close = curr["close"]
        high = curr["high"]
        low = curr["low"]

        body = abs(close - open_)
        candle_range = high - low

        if candle_range == 0:
            continue

        upper_wick = high - max(open_, close)
        lower_wick = min(open_, close) - low

        # Bullish Engulfing
        if (
            prev["close"] < prev["open"] and
            close > open_ and
            close > prev["open"] and
            open_ < prev["close"]
        ):
            detected.append("Bullish Engulfing")

        # Bearish Engulfing
        if (
            prev["close"] > prev["open"] and
            close < open_ and
            open_ > prev["close"] and
            close < prev["open"]
        ):
            detected.append("Bearish Engulfing")

        # Doji
        if body <= candle_range * 0.1:
            detected.append("Doji")

        # Hammer
        if (
            lower_wick > body * 2 and
            upper_wick < body
        ):
            detected.append("Hammer")

        # Shooting Star
        if (
            upper_wick > body * 2 and
            lower_wick < body
        ):
            detected.append("Shooting Star")

        if detected:
            # Select highest priority pattern
            for p in priority_order:
                if p in detected:
                    patterns.append({
                        "index": i,
                        "pattern": p
                    })
                    break

    return patterns