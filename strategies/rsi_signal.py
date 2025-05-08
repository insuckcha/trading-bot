import pandas as pd

def compute_rsi(df, period=14):
    """Calculate the Relative Strength Index (RSI)."""
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def find_rsi_signals(df, period=14, oversold=30, overbought=70):
    """
    Generate RSI-based buy/sell signals.

    Buy signal: RSI crosses above `oversold` threshold.
    Sell signal: RSI crosses below `overbought` threshold.
    """
    df = df.copy()
    df["RSI"] = compute_rsi(df, period)
    df["RSI_prev"] = df["RSI"].shift(1)

    buy_signals = []
    sell_signals = []

    for i, row in df.iterrows():
        if pd.notnull(row["RSI"]) and pd.notnull(row["RSI_prev"]):
            if row["RSI_prev"] < oversold and row["RSI"] >= oversold:
                buy_signals.append((row["Time"], row["close"]))
            elif row["RSI_prev"] > overbought and row["RSI"] <= overbought:
                sell_signals.append((row["Time"], row["close"]))

    return buy_signals, sell_signals, df

