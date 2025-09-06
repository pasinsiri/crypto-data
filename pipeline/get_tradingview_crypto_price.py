import requests
import numpy as np
import pandas as pd
import datetime as dt
import os
import tradingview_screener as tvs
from tradingview_screener import Query, Column, And, Or, col
from dotenv import load_dotenv

load_dotenv()

# * load tickers from Supabase
TABLE_NAME = "crypto_tickers"
SUPABASE_PROJECT_ID = os.environ.get("SUPABASE_PROJECT_ID")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_URL = f"https://{SUPABASE_PROJECT_ID}.supabase.co/rest/v1/{TABLE_NAME}"