#!/usr/bin/env python3
import requests
import time
import json
import os
import pytz
from dotenv import load_dotenv
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

load_dotenv()

# * CoinGecko parameters (for public API)
TOKEN_LIST_PATH = './keys/token_info.json'
BASE_URL = "https://api.coingecko.com/api/v3/simple/price"

# * Supabase credentials
TABLE_NAME = "crypto_price_usd"
SUPABASE_PROJECT_ID = os.environ.get("SUPABASE_PROJECT_ID")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_URL = f"https://{SUPABASE_PROJECT_ID}.supabase.co/rest/v1/{TABLE_NAME}"

