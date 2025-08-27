import logging
from datetime import date
from pathlib import Path
from currency_converter import CurrencyConverter, ECB_URL

from pathlib import Path
CACHE_DIR = Path("/app/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

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

    try:
        if not cache_file.exists():
            logging.info("Downloading fresh ECB data...")
            cc = CurrencyConverter(ECB_URL, fallback_on_missing_rate=True, fallback_on_wrong_date=True)
            if hasattr(cc, "source") and isinstance(cc.source, str) and cc.source.startswith("http"):
                pass
            logging.info("Fresh ECB data loaded.")
            return cc
        else:
            logging.info("Using cached ECB data for today.")
            return CurrencyConverter(str(cache_file), fallback_on_missing_rate=True, fallback_on_wrong_date=True)
    except Exception as e:
        logging.error(f"ECB data load failed: {e}. Trying previous cache...", exc_info=True)
        prev = sorted(CACHE_DIR.glob("ecb_*.xml"))
        if prev:
            logging.warning("Falling back to previous cached ECB file (rates may be stale).")
            return CurrencyConverter(str(prev[-1]), fallback_on_missing_rate=True, fallback_on_wrong_date=True)
        logging.warning("No local cache available; falling back to ECB_URL with converter defaults.")
        return CurrencyConverter(ECB_URL, fallback_on_missing_rate=True, fallback_on_wrong_date=True)
