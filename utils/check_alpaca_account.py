from alpaca_trade_api.rest import REST
import os
from dotenv import load_dotenv

load_dotenv()

api = REST(
    os.getenv("ALPACA_API_KEY"),
    os.getenv("ALPACA_SECRET_KEY"),
    os.getenv("ALPACA_BASE_URL"),
)

account = api.get_account()
print(f"Account status: {account.status}")
print(f"Buying power: ${account.buying_power}")
