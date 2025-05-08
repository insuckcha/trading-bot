import streamlit as st
import plotly.graph_objs as go
import pandas as pd

def render_rsi_chart(df, buy_signals=None, sell_signals=None):
    st.subheader("📊 RSI Indicator + Signals")
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Time"],
        y=df["RSI"],
        mode="lines",
        name="RSI",
        line=dict(color="blue")
    ))

    fig.add_shape(type="line", x0=df["Time"].min(), x1=df["Time"].max(), y0=70, y1=70,
                  line=dict(dash="dash", color="black"))
    fig.add_shape(type="line", x0=df["Time"].min(), x1=df["Time"].max(), y0=30, y1=30,
                  line=dict(dash="dash", color="black"))

    if buy_signals:
        fig.add_trace(go.Scatter(
            x=[t for t, _ in buy_signals],
            y=[p for _, p in buy_signals],
            mode="markers",
            marker=dict(color="black", size=8, symbol="triangle-up"),
            name="Buy Signal"
        ))

    if sell_signals:
        fig.add_trace(go.Scatter(
            x=[t for t, _ in sell_signals],
            y=[p for _, p in sell_signals],
            mode="markers",
            marker=dict(color="black", size=8, symbol="triangle-down"),
            name="Sell Signal"
        ))

    fig.update_layout(
        yaxis_title="RSI",
        height=400,
        showlegend=True,
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig, use_container_width=True)
