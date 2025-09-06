import requests
import numpy as np
import pandas as pd
import datetime as dt
import os
import tradingview_screener as tvs
from tradingview_screener import Query, Column, And, Or, col
from dotenv import load_dotenv

load_dotenv()

# * Load cryptocurrency tickers from Supabase
# ? setup credentials
TABLE_NAME = "crypto_tickers"
SUPABASE_PROJECT_ID = os.environ.get("SUPABASE_PROJECT_ID")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_URL = f"https://{SUPABASE_PROJECT_ID}.supabase.co/rest/v1/{TABLE_NAME}"

# ? request data from Supabase
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}
response = requests.get(SUPABASE_URL, headers=headers)
assert response.status_code == 200, f'Supabase error: The GET request returns with status {response.status_code}'

tickers = [r['ticker'] for r in response.json()]