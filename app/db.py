import logging
from supabase import create_client
from app import config

# Create Supabase client
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

    try:
        response = supabase.table("exchange_rates").upsert(
            rows,
            on_conflict="date,base_currency,target_currency"
        ).execute()

        if hasattr(response, "error") and response.error:
            logging.error(f"Supabase insert error: {response.error}")
        else:
            logging.info(f"Inserted/updated {len(rows)} rows into exchange_rates.")

        return response

    except Exception as e:
        logging.error(f"Failed to insert exchange rates: {e}", exc_info=True)
        raise
