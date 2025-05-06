# 🦾 Trading Bot with Polygon.io + Alpaca

A Python-based trading bot that uses real-time market data from [Polygon.io](https://polygon.io) and places simulated trades via [Alpaca](https://alpaca.markets) paper trading API.

## 📈 Strategy

This bot implements a **Simple Moving Average (SMA) crossover strategy**:
- **Buy** signal when SMA(10) crosses above SMA(30)
- Trades **AAPL** with 1 share on each signal
- Trades only if no existing position is held

## ⚙️ Features

- 🔄 Fetches 1-minute candles from Polygon.io
- 💡 Computes SMA(10) and SMA(30)
- 🛒 Places market orders via Alpaca (paper)
- 🧠 Prevents duplicate buys if already holding the stock
- ⏱ Runs every minute using `schedule`

## 🧪 Requirements

- Python 3.8+
- [Polygon.io account](https://polygon.io)
- [Alpaca paper trading account](https://alpaca.markets)

## 📦 Installation

```bash
git clone https://github.com/yourusername/trading-bot.git
cd trading-bot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
