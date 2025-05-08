import pandas as pd

def compute_bollinger_bands(df, period=20, deviation=2):
    df = df.copy()
    df["SMA"] = df["close"].rolling(window=period).mean()
    df["STD"] = df["close"].rolling(window=period).std()
    df["UpperBand"] = df["SMA"] + (deviation * df["STD"])
    df["LowerBand"] = df["SMA"] - (deviation * df["STD"])
    return df

def find_bollinger_signals(df):
    df = compute_bollinger_bands(df)
    buy_signals, sell_signals = [], []

    for i in range(1, len(df)):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]

        # Buy when price crosses below lower band
        if prev["close"] > prev["LowerBand"] and curr["close"] < curr["LowerBand"]:
            buy_signals.append((curr["Time"], curr["close"]))

        # Sell when price crosses above upper band
        elif prev["close"] < prev["UpperBand"] and curr["close"] > curr["UpperBand"]:
            sell_signals.append((curr["Time"], curr["close"]))

    return buy_signals, sell_signals, df

