import streamlit as st
import plotly.graph_objs as go
import pandas as pd
from config.constants import EMA_SPANS

def find_ema_signals(df):
    buy_signals, sell_signals = [], []
    prev_state = "neutral"

    for i in range(len(df)):
        row = df.iloc[i]
        if all(pd.notnull([row.get("EMA10"), row.get("EMA20"), row.get("EMA50")])):
            if row["EMA10"] > row["EMA20"] > row["EMA50"]:
                if prev_state != "buy":
                    buy_signals.append((row["Time"], row["c"]))
                    prev_state = "buy"
            elif row["EMA10"] < row["EMA20"] < row["EMA50"]:
                if prev_state != "sell":
                    sell_signals.append((row["Time"], row["c"]))
                    prev_state = "sell"
            else:
                prev_state = "neutral"
        else:
            prev_state = "neutral"

    return buy_signals, sell_signals

def render_ema_chart(df, chart_type):
    st.subheader("📉 EMA Alignment Strategy")
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

    for span in EMA_SPANS:
        col = f"EMA{span}"
        if col in df.columns:
            fig.add_trace(go.Scatter(
                x=df["Time"], y=df[col], name=col, line=dict(width=1)
            ))

    buys, sells = find_ema_signals(df)
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
