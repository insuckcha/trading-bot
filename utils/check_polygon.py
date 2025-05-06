import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("POLYGON_API_KEY")

def check_polygon_api():
    url = f"https://api.polygon.io/v2/aggs/ticker/AAPL/prev"
    params = {
        "adjusted": "true",
        "apiKey": key
    }

    res = requests.get(url, params=params)
    if res.status_code == 200:
        data = res.json()
        results = data.get("results", [])
        if results:
            price = results[0]["c"]  # closing price
            print(f"✅ Polygon working. AAPL previous close: ${price}")
        else:
            print("❗️No results returned.")
    else:
        print(f"❌ Error {res.status_code}: {res.text}")

if __name__ == "__main__":
    check_polygon_api()
