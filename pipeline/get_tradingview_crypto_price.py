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

# * Get price data from TradingView
q = Query() \
    .set_tickers(*[f'BINANCE:{t}' for t in tickers]) \
    .where(Column('type') == 'spot') \
    .select('name', 'open', 'high', 'low', 'close', 'volume') \
    .get_scanner_data()

# * Extract data, form table, and ingest to Supabase
raw_df = q[1].copy()
raw_df['market'] = raw_df['ticker'].apply(lambda x: x.split(':')[0])

# ? find timestamp to stamp in the Supabase table
dt_now = dt.datetime.now()
rounded_dt = dt_now.replace(minute=0, second=0, microsecond=0) + dt.timedelta(hours=1)
print(f'Timestamp = {rounded_dt}')
raw_df['timestamp'] = rounded_dt

# ? ingest to supabase
"""
The schema is:
    ticker varchar(20)
    name varchar(20)
    open float
    high
    low
    close
    volume
    market
    timestamp
"""