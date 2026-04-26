import requests
import pandas as pd
from app.config import API_KEY

def get_stock_data(ticker: str):
    # Placeholder: replace with real API call
    # Example structure expected: OHLCV data

    url = f"https://fake-api.com/{ticker}?apikey={API_KEY}"

    # MOCK DATA for now (so repo runs immediately)
    data = {
        "close": [10, 10.5, 10.2, 9.8, 9.5, 9.3, 9.0],
    }

    return pd.DataFrame(data)

def get_short_interest(ticker: str):
    # Replace with real API source
    return {
        "short_interest": 0.28,   # 28%
        "days_to_cover": 6.2
    }
