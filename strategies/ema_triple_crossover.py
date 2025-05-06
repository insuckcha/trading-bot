def should_buy(df):
    """Return True if EMA10 > EMA20 > EMA50 — bullish alignment"""
    df['ema10'] = df['close'].ewm(span=10, adjust=False).mean()
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()

    if len(df.dropna()) < 1:
        return False

    latest = df.iloc[-1]

    return (
        latest['ema10'] > latest['ema20'] and
        latest['ema20'] > latest['ema50']
    )
