import os
import sys
import requests
import pandas as pd
from dotenv import load_dotenv

# Allow access to project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.date_utils import parse_interval
from config.constants import EMA_SPANS, SMA_SPANS

load_dotenv()
API_KEY = os.getenv("POLYGON_API_KEY")


def get_data(symbol, date_from, date_to, limit, interval):
    multiplier, timespan = parse_interval(interval)
    base_url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{date_from}/{date_to}"
    params = {"adjusted": "true", "sort": "asc", "limit": 5000, "apiKey": API_KEY}

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
    df["Time"] = pd.to_datetime(df["t"], unit="ms")
    df = df.sort_values("Time").tail(limit)
    df["close"] = df["c"]

    for span in EMA_SPANS:
        df[f"EMA{span}"] = df["close"].ewm(span=span, adjust=False).mean()
    for span in SMA_SPANS:
        df[f"SMA{span}"] = df["close"].rolling(span).mean()

    return df
