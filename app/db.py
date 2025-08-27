import logging
from time import time
from supabase import create_client
from app import config

supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def test_connection():
    try:
        response = supabase.table("exchange_rates").select("*").limit(1).execute()
        if hasattr(response, "data"):
            logging.info("Supabase connection successful.")
            return True
        else:
            logging.warning("Supabase connection test returned no data.")
            return False
    except Exception as e:
        logging.error(f"Supabase connection failed: {e}", exc_info=True)
        return False

def insert_exchange_rates(rows: list[dict]):
    if not rows:
        logging.warning("No rows to insert.")
        return
    def _do():
        return supabase.table("exchange_rates").upsert(
            rows,
            on_conflict="date,base_currency,target_currency"
        ).execute()
    response = _retry(_do, tries=3, base_delay=1.0)
    if getattr(response, "error", None):
        logging.error(f"Supabase insert error: {response.error}")
    else:
        logging.info(f"Inserted/updated {len(rows)} rows into exchange_rates.")
    return response

def has_rates_for_date(target_date):
    try:
        response = supabase.table("exchange_rates") \
            .select("date") \
            .eq("date", str(target_date)) \
            .limit(1) \
            .execute()

        if hasattr(response, "data") and response.data:
            return True
        return False

    except Exception as e:
        logging.error(f"Failed to check rates for {target_date}: {e}", exc_info=True)
        return False

def _retry(op, tries=3, base_delay=1.0, *args, **kwargs):
    for i in range(tries):
        try:
            return op(*args, **kwargs)
        except Exception as e:
            if i == tries - 1:
                logging.error(f"Operation failed after {tries} attempts: {e}", exc_info=True)
                raise
            delay = base_delay * (2 ** i)
            logging.warning(f"Operation failed (attempt {i+1}/{tries}): {e}. Retrying in {delay:.1f}s...")
            time.sleep(delay)