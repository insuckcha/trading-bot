# 🦾 Trading Bot with Polygon.io + Alpaca + Streamlit UI

A Python-based trading bot that uses real-time market data from [Polygon.io](https://polygon.io) and places simulated trades via [Alpaca](https://alpaca.markets). Includes a Streamlit chart UI that visualizes candles and EMAs.

---

## 📈 Strategy

Implements a **Triple EMA Crossover Strategy**:

- Buy signal when: **EMA10 > EMA20 > EMA50**
- Symbol: **AAPL**
- Quantity: **1 share**
- Prevents repeat buys if already in position

Strategies are modular — you can add more in the `strategies/` folder.

---

## 🧪 Requirements

- Python 3.8 or higher
- Polygon.io API key (free or paid)
- Alpaca Paper Trading account

---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/trading-bot.git
cd trading-bot
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔐 Configure API Keys

Create a `.env` file in the project root:

```env
# Polygon.io
POLYGON_API_KEY=your_polygon_key_here

# Alpaca
ALPACA_API_KEY=your_alpaca_key_here
ALPACA_SECRET_KEY=your_alpaca_secret_here
ALPACA_BASE_URL=https://paper-api.alpaca.markets
```

> ⚠️ Do NOT commit `.env` to version control.

---

## 🚀 Run the Bot

```bash
make run-bot
```

Or manually:

```bash
python bot.py
```

---

## 📊 Run the Streamlit Chart UI

```bash
make run-ui
```

Or manually:

```bash
streamlit run ui/visualize.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🗂 Project Structure

```
trading-bot/
├── strategies/              # Trading strategies
│   ├── ema_triple_crossover.py
│   └── sma_crossover.py
├── utils/                   # Test scripts
│   ├── check_alpaca_account.py
│   └── check_polygon.py
├── ui/                      # Streamlit dashboard
│   └── visualize.py
├── bot.py                   # Main trading logic
├── .env                     # API keys (excluded from Git)
├── requirements.txt
├── Makefile
└── README.md
```

---

## 📌 Notes

- Uses **paper trading** only (safe for testing)
- Modular strategy support
- Easily expandable (logging, alerts, sell logic, backtesting)

---

## 📜 License

MIT License
