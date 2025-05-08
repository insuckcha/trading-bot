import streamlit as st
import plotly.graph_objs as go
import pandas as pd
from config.constants import SMA_SPANS

def find_sma_signals(df):
    buy_signals, sell_signals = [], []
    last_signal = None

    for i in range(1, len(df)):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]

        if pd.notnull(prev.get("SMA10")) and pd.notnull(prev.get("SMA30")):
            crossed_up = prev["SMA10"] < prev["SMA30"] and curr["SMA10"] > curr["SMA30"]
            crossed_down = prev["SMA10"] > prev["SMA30"] and curr["SMA10"] < curr["SMA30"]

            if crossed_up and last_signal != "buy":
                buy_signals.append((curr["Time"], curr["c"]))
                last_signal = "buy"
            elif crossed_down and last_signal != "sell":
                sell_signals.append((curr["Time"], curr["c"]))
                last_signal = "sell"

    return buy_signals, sell_signals

def render_sma_chart(df, chart_type):
    st.subheader("📈 SMA Crossover Strategy")
    fig = go.Figure()

    if chart_type == "Candlestick":
        fig.add_trace(go.Candlestick(
            x=df["Time"],
            open=df["o"],
            high=df["h"],
            low=df["l"],
            close=df["c"],
            name="Candles"
        ))
    else:
        fig.add_trace(go.Scatter(x=df["Time"], y=df["c"], mode="lines", name="Price"))

    for span in SMA_SPANS:
        col = f"SMA{span}"
        if col in df.columns:
            fig.add_trace(go.Scatter(
                x=df["Time"], y=df[col], name=col, line=dict(width=1, dash="dot")
            ))

    buys, sells = find_sma_signals(df)
    if buys:
        fig.add_trace(go.Scatter(
            x=[t for t, _ in buys],
            y=[p for _, p in buys],
            mode="markers",
            marker=dict(color="black", size=8, symbol="triangle-up"),
            name="Buy Signal"
        ))
    if sells:
        fig.add_trace(go.Scatter(
            x=[t for t, _ in sells],
            y=[p for _, p in sells],
            mode="markers",
            marker=dict(color="black", size=8, symbol="triangle-down"),
            name="Sell Signal"
        ))

    fig.update_layout(
        yaxis_title="Price",
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig, use_container_width=True)
