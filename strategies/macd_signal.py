import pandas as pd

def compute_macd(df, short_span=12, long_span=26, signal_span=9):
    df = df.copy()
    df["EMA12"] = df["close"].ewm(span=short_span, adjust=False).mean()
    df["EMA26"] = df["close"].ewm(span=long_span, adjust=False).mean()
    df["MACD"] = df["EMA12"] - df["EMA26"]
    df["MACD_Signal"] = df["MACD"].ewm(span=signal_span, adjust=False).mean()
    df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]
    return df

def find_macd_signals(df):
    df = compute_macd(df)
    buy_signals, sell_signals = [], []

    for i in range(1, len(df)):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]
        if prev["MACD"] < prev["MACD_Signal"] and curr["MACD"] > curr["MACD_Signal"]:
            buy_signals.append((curr["Time"], curr["close"]))
        elif prev["MACD"] > prev["MACD_Signal"] and curr["MACD"] < curr["MACD_Signal"]:
            sell_signals.append((curr["Time"], curr["close"]))

    return buy_signals, sell_signals, df

