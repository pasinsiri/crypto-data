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
SUPABASE_PROJECT_ID = os.environ.get("SUPABASE_PROJECT_ID")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
TICKERS_URL = f"https://{SUPABASE_PROJECT_ID}.supabase.co/rest/v1/crypto_alt_tickers"
TARGET_TABLE_URL = f"https://{SUPABASE_PROJECT_ID}.supabase.co/rest/v1/crypto_alt_data"