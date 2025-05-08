def should_buy(df):
    """Return True if SMA10 just crossed above SMA30"""
    df["sma10"] = df["close"].rolling(10).mean()
    df["sma30"] = df["close"].rolling(30).mean()

    if len(df.dropna()) < 2:
        return False

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    return prev["sma10"] < prev["sma30"] and curr["sma10"] > curr["sma30"]
