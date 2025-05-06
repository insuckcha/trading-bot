import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import plotly.graph_objs as go

# Load API key
load_dotenv()
API_KEY = os.getenv("POLYGON_API_KEY")

# --- Sidebar Controls ---
st.sidebar.title("Chart Settings")
SYMBOL = st.sidebar.text_input("Stock Symbol", value="AAPL").upper()
INTERVAL = st.sidebar.selectbox("Time Interval", options=["1min", "5min", "15min", "1hour", "1day"], index=0)
LIMIT = st.sidebar.selectbox("Number of candles", options=[150, 300, 500], index=0)
CHART_TYPE = st.sidebar.selectbox("Chart Type", options=["Candlestick", "Line"], index=0)

EMA_SPANS = [10, 20, 50]
SMA_SPANS = [10, 30]

def parse_interval(interval_str):
    if interval_str.endswith("min"):
        return int(interval_str[:-3]), "minute"
    elif interval_str.endswith("hour"):
        return int(interval_str[:-4]), "hour"
    elif interval_str.endswith("day"):
        return int(interval_str[:-3]), "day"
    else:
        return 1, "minute"

def get_date_range(limit, interval):
    today = datetime.today()
    if interval.endswith("min"):
        start = today
    elif interval.endswith("hour"):
        trading_days_needed = int(limit / 6.5) + 1
        calendar_days = int(trading_days_needed * 1.4)
        start = today - timedelta(days=calendar_days)
    elif interval.endswith("day"):
        calendar_days = int(limit / 0.7)
        start = today - timedelta(days=calendar_days)
    elif interval.endswith("week"):
        start = today - timedelta(weeks=limit + 2)
    else:
        start = today
    return start.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")

def get_data(symbol, date_from, date_to, limit, interval):
    multiplier, timespan = parse_interval(interval)
    base_url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{date_from}/{date_to}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": 5000,
        "apiKey": API_KEY
    }

    all_results = []
    url = base_url
    while url:
        res = requests.get(url, params=params if url == base_url else {})
        if res.status_code != 200:
            break
        json_data = res.json()
        results = json_data.get("results", [])
        all_results.extend(results)
        url = json_data.get("next_url")

    if not all_results:
        return pd.DataFrame()

    df = pd.DataFrame(all_results)
    df['Time'] = pd.to_datetime(df['t'], unit='ms')
    df = df.sort_values("Time").tail(limit)
    df['close'] = df['c']

    for span in EMA_SPANS:
        df[f'EMA{span}'] = df['close'].ewm(span=span, adjust=False).mean()
    for span in SMA_SPANS:
        df[f'SMA{span}'] = df['close'].rolling(span).mean()

    return df

def find_sma_signals(df):
    buy_signals, sell_signals = [], []
    for i in range(1, len(df)):
        prev, curr = df.iloc[i - 1], df.iloc[i]
        if pd.notnull(prev['SMA10']) and pd.notnull(prev['SMA30']):
            if prev['SMA10'] < prev['SMA30'] and curr['SMA10'] > curr['SMA30']:
                buy_signals.append((curr['Time'], curr['close']))
            elif prev['SMA10'] > prev['SMA30'] and curr['SMA10'] < curr['SMA30']:
                sell_signals.append((curr['Time'], curr['close']))
    return buy_signals, sell_signals

def find_ema_signals(df):
    buy_signals, sell_signals = [], []
    for i in range(len(df)):
        row = df.iloc[i]
        if all(pd.notnull([row['EMA10'], row['EMA20'], row['EMA50']])):
            if row['EMA10'] > row['EMA20'] > row['EMA50']:
                buy_signals.append((row['Time'], row['close']))
            elif row['EMA10'] < row['EMA20'] < row['EMA50']:
                sell_signals.append((row['Time'], row['close']))
    return buy_signals, sell_signals

# --- Streamlit Main ---
st.title(f"{SYMBOL} — {INTERVAL} Chart with Strategy Signals")
date_from, date_to = get_date_range(LIMIT, INTERVAL)
df = get_data(SYMBOL, date_from, date_to, LIMIT, INTERVAL)

if df.empty:
    st.warning("No data returned. Try increasing the date range or checking your symbol.")
else:
    # --- SMA Chart ---
    st.subheader("📈 SMA Crossover Strategy")
    fig_sma = go.Figure()

    if CHART_TYPE == "Candlestick":
        fig_sma.add_trace(go.Candlestick(x=df['Time'], open=df['o'], high=df['h'], low=df['l'], close=df['c'], name="Candles"))
    else:
        fig_sma.add_trace(go.Scatter(x=df['Time'], y=df['close'], mode='lines', name="Price"))

    for span in SMA_SPANS:
        fig_sma.add_trace(go.Scatter(x=df['Time'], y=df[f'SMA{span}'], name=f"SMA{span}", line=dict(width=1, dash="dot")))

    sma_buys, sma_sells = find_sma_signals(df)
    if sma_buys:
        fig_sma.add_trace(go.Scatter(x=[t for t, _ in sma_buys], y=[p for _, p in sma_buys], mode='markers',
                                     marker=dict(color='green', size=8, symbol='triangle-up'), name="Buy Signal"))
    if sma_sells:
        fig_sma.add_trace(go.Scatter(x=[t for t, _ in sma_sells], y=[p for _, p in sma_sells], mode='markers',
                                     marker=dict(color='red', size=8, symbol='triangle-down'), name="Sell Signal"))
    fig_sma.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig_sma, use_container_width=True)

    # --- EMA Chart ---
    st.subheader("📉 EMA Alignment Strategy")
    fig_ema = go.Figure()

    if CHART_TYPE == "Candlestick":
        fig_ema.add_trace(go.Candlestick(x=df['Time'], open=df['o'], high=df['h'], low=df['l'], close=df['c'], name="Candles"))
    else:
        fig_ema.add_trace(go.Scatter(x=df['Time'], y=df['close'], mode='lines', name="Price"))

    for span in EMA_SPANS:
        fig_ema.add_trace(go.Scatter(x=df['Time'], y=df[f'EMA{span}'], name=f"EMA{span}", line=dict(width=1)))

    ema_buys, ema_sells = find_ema_signals(df)
    if ema_buys:
        fig_ema.add_trace(go.Scatter(x=[t for t, _ in ema_buys], y=[p for _, p in ema_buys], mode='markers',
                                     marker=dict(color='green', size=8, symbol='triangle-up'), name="Buy Signal"))
    if ema_sells:
        fig_ema.add_trace(go.Scatter(x=[t for t, _ in ema_sells], y=[p for _, p in ema_sells], mode='markers',
                                     marker=dict(color='red', size=8, symbol='triangle-down'), name="Sell Signal"))
    fig_ema.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig_ema, use_container_width=True)
