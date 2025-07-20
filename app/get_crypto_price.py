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

class RateLimitError(Exception):
    pass

with open(TOKEN_LIST_PATH, 'r') as f:
    token_list = json.load(f)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(RateLimitError))
def fetch_crypto_price(token_list, timestamp):
    params = {
        "vs_currencies": "usd",
        "ids": ",".join([token["id"] for token in token_list]),
        "include_24hr_vol": False,
        "precision": 6
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        print("Saving...")
        store_in_supabase(data, timestamp)
    elif response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 10))
        print(f"Rate limit hit. Waiting {retry_after}s")
        raise RateLimitError("Rate limit exceeded")
    else:
        raise Exception(f"API error: {response.status_code}")

def store_in_supabase(price_data, timestamp):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    # timestamp = datetime.now(pytz.timezone("Asia/Bangkok")).isoformat()
    data = [{
        "token_id": token,
        "price": price["usd"],
        "created_at": str(timestamp)
    } for token, price in price_data.items()]
    response = requests.post(SUPABASE_URL, json=data, headers=headers)
    if response.status_code != 201:
        print(f"Supabase error: {response.status_code}, {response.text}")

