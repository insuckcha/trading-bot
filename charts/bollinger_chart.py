import streamlit as st
import plotly.graph_objs as go
from strategies.bollinger_signal import find_bollinger_signals

def render_bollinger_chart(df):
    st.subheader("📊 Bollinger Bands")
    buy_signals, sell_signals, df = find_bollinger_signals(df)

    fig = go.Figure()

    # Price line
    fig.add_trace(go.Scatter(x=df["Time"], y=df["close"], name="Price", line=dict(color="black")))

    # Bands
    fig.add_trace(go.Scatter(x=df["Time"], y=df["UpperBand"], name="Upper Band", line=dict(color="red", dash="dot")))
    fig.add_trace(go.Scatter(x=df["Time"], y=df["SMA"], name="SMA", line=dict(color="blue", dash="dash")))
    fig.add_trace(go.Scatter(x=df["Time"], y=df["LowerBand"], name="Lower Band", line=dict(color="green", dash="dot")))

    # Buy signals
    if buy_signals:
        fig.add_trace(go.Scatter(
            x=[x for x, _ in buy_signals],
            y=[y for _, y in buy_signals],
            mode="markers",
            marker=dict(color="black", size=8, symbol="triangle-up"),
            name="Buy Signal"
        ))

    # Sell signals
    if sell_signals:
        fig.add_trace(go.Scatter(
            x=[x for x, _ in sell_signals],
            y=[y for _, y in sell_signals],
            mode="markers",
            marker=dict(color="black", size=8, symbol="triangle-down"),
            name="Sell Signal"
        ))

    fig.update_layout(
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

