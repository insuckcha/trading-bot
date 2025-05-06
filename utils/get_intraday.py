import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("POLYGON_API_KEY")

# Set your ticker and today's date
symbol = "AAPL"
today = datetime.today().strftime("%Y-%m-%d")

def get_1min_bars(symbol, date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/minute/{date}/{date}"
    params = {
        "adjusted": "true",
        "sort": "desc",
        "limit": 10,
        "apiKey": API_KEY
    }

    res = requests.get(url, params=params)
    if res.status_code != 200:
        print(f"❌ Error {res.status_code}: {res.text}")
        return None

    data = res.json()
    if "results" not in data:
        print("❗️No candle data returned.")
        return None

    df = pd.DataFrame(data["results"])
    df['timestamp'] = pd.to_datetime(df['t'], unit='ms')
    df = df[['timestamp', 'o', 'h', 'l', 'c', 'v']]
    df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    return df.sort_values("Time")

if __name__ == "__main__":
    df = get_1min_bars(symbol, today)
    if df is not None:
        print(df.tail(10))  # show latest candles
