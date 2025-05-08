import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from dotenv import load_dotenv

from utils.api import get_data
from utils.date_utils import get_date_range
from charts.sma_chart import render_sma_chart
from charts.ema_chart import render_ema_chart
from charts.rsi_chart import render_rsi_chart
from charts.macd_chart import render_macd_chart
from charts.bollinger_chart import render_bollinger_chart
from strategies.rsi_signal import find_rsi_signals

# Set wide layout
st.set_page_config(layout="wide")
load_dotenv()
API_KEY = os.getenv("POLYGON_API_KEY")

# --- Chart Settings ---
with st.expander("📊 Chart Settings", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        SYMBOL = st.text_input("Stock Symbol", value="AAPL").upper()
        INTERVAL = st.selectbox("Time Interval", options=["1min", "5min", "15min", "1hour", "1day"], index=0)
    with col2:
        LIMIT = st.selectbox("Number of candles", options=[150, 300, 500], index=0)
        CHART_TYPE = st.selectbox("Chart Type", options=["Candlestick", "Line"], index=0)

@st.cache_data(show_spinner="Loading chart data...")
def fetch_data(symbol, interval, limit):
    date_from, date_to = get_date_range(limit, interval)
    return get_data(symbol, date_from, date_to, limit, interval)

# --- Load Data ---
df = fetch_data(SYMBOL, INTERVAL, LIMIT)

st.header(f"{SYMBOL} — {INTERVAL} Chart with Strategy Signals")
if df.empty:
    st.warning("No data returned. Try increasing the date range or checking your symbol.")
else:
    # Charts only (no summary)
    render_sma_chart(df, CHART_TYPE)
    render_ema_chart(df, CHART_TYPE)
    buy_rsi, sell_rsi, df_rsi = find_rsi_signals(df)
    render_rsi_chart(df_rsi, buy_rsi, sell_rsi)
    render_macd_chart(df)
    render_bollinger_chart(df)
