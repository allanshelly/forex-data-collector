import logging
from datetime import date
from currency_converter import CurrencyConverter, ECB_URL
from app import config

supabase = None

def init_supabase(client):
    """Pass in supabase client from main so utils can use it."""
    global supabase
    supabase = client

def load_currency_converter() -> CurrencyConverter:
    today = date.today().isoformat()
    cache_file = config.CACHE_DIR / f"ecb_{today}.xml"
    if not cache_file.exists():
        logging.info("Downloading fresh ECB data...")
        return CurrencyConverter(ECB_URL, fallback_on_missing_rate=True, fallback_on_wrong_date=True)
    else:
        logging.info("Using cached ECB data...")
        return CurrencyConverter(str(cache_file), fallback_on_missing_rate=True, fallback_on_wrong_date=True)

def insert_exchange_rates(rows):
    if supabase is None:
        raise RuntimeError("Supabase client not initialized. Call init_supabase first.")

    try:
        response = supabase.table("exchange_rates").upsert(
            rows, on_conflict=["date", "base_currency", "target_currency"]
        ).execute()
        if hasattr(response, "error") and response.error:
            logging.error(f"Supabase insert error: {response.error}")
    except Exception as e:
        logging.error(f"Database insert failed: {e}", exc_info=True)

def deduplicate_rows(rows, keys=("date", "base_currency", "target_currency")):
    seen = {}
    for row in rows:
        key = tuple(row[k] for k in keys)
        seen[key] = row
    return list(seen.values())
