import os
import time
import requests
import schedule
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from alpaca_trade_api.rest import REST
# from strategies import ema_triple_crossover as strategy
from strategies import sma_crossover as strategy

# Load environment variables
load_dotenv()

# API Keys
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL")

# Constants
SYMBOL = "AAPL"
POSITION_SIZE = 1
alpaca = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, base_url=ALPACA_BASE_URL)

def fetch_1min_candles(symbol):
    today = datetime.today().strftime("%Y-%m-%d")
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/minute/{today}/{today}"
    params = {
        "adjusted": "true",
        "sort": "desc",
        "limit": 50,
        "apiKey": POLYGON_API_KEY
    }
    res = requests.get(url, params=params)
    if res.status_code != 200:
        print(f"❌ Polygon error: {res.status_code} - {res.text}")
        return None

    data = res.json()
    if "results" not in data:
        print("❗️No candle data.")
        return None

    df = pd.DataFrame(data["results"])
    df['timestamp'] = pd.to_datetime(df['t'], unit='ms')
    df = df[['timestamp', 'o', 'h', 'l', 'c', 'v']]
    df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    df.set_index("Time", inplace=True)
    df.rename(columns={"Close": "close"}, inplace=True)
    return df.sort_index()

def already_has_position():
    positions = alpaca.list_positions()
    return any(p.symbol == SYMBOL for p in positions)

def place_buy_order():
    try:
        alpaca.submit_order(
            symbol=SYMBOL,
            qty=POSITION_SIZE,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        print(f"✅ Buy order placed for {SYMBOL}")
    except Exception as e:
        print(f"❌ Order failed: {e}")

def run_strategy():
    df = fetch_1min_candles(SYMBOL)
    if df is None:
        return

    if strategy.should_buy(df):
        print("📈 SMA crossover buy signal")
        print("📈 EMA triple crossover buy signal")

        if not already_has_position():
            place_buy_order()
        else:
            print("💡 Already holding position.")
    else:
        print("🟡 No buy signal")

schedule.every(1).minutes.do(run_strategy)

if __name__ == "__main__":
    print("🚀 Bot started")
    run_strategy()
    while True:
        schedule.run_pending()
        time.sleep(1)
