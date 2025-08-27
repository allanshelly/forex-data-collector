import logging
from collections import Counter
from datetime import date
from currency_converter import CurrencyConverter

from pathlib import Path
CACHE_DIR = Path("/app/cache")
CACHE_DIR.mkdir(exist_ok=True)

supabase = None

def init_supabase(client):
    global supabase
    supabase = client

def deduplicate_rows(rows, keys=("date", "base_currency", "target_currency")):
    seen = {}
    for row in rows:
        key = tuple(row[k] for k in keys)
        seen[key] = row
    return list(seen.values())

def load_currency_converter():
    today = date.today().isoformat()
    cache_file = CACHE_DIR / f"ecb_{today}.xml"
    if not cache_file.exists():
        logging.info("Downloading fresh ECB data...")
        return CurrencyConverter(ECB_URL, fallback_on_missing_rate=True)
    else:
        logging.info("Using cached ECB data...")
        return CurrencyConverter(str(cache_file), fallback_on_missing_rate=True)
