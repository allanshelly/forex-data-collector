import logging
from supabase import create_client, Client
from app import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    force=True,
)

supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def test_connection() -> bool:
    """Test Supabase connection by fetching a single row."""
    try:
        logging.info("Testing Supabase connection...")
        response = supabase.table("exchange_rates").select("*").limit(1).execute()
        if hasattr(response, "error") and response.error:
            logging.error(f"Connection test failed: {response.error}")
            return False
        logging.info("Supabase connection successful!")
        logging.info(f"Sample row: {response.data if response.data else 'No rows yet.'}")
        return True
    except Exception as e:
        logging.error(f"Supabase connection test raised exception: {e}", exc_info=True)
        return False

def insert_exchange_rates(rows: list[dict]):
    """
    Insert or update exchange rate records into the database.
    Uses upsert with unique constraint on (date, base_currency, target_currency).
    """
    if not rows:
        logging.info("No rows to insert.")
        return

    if not test_connection():
        logging.error("Cannot insert rows because Supabase connection failed.")
        return

    try:
        response = (
            supabase.table("exchange_rates")
            .upsert(rows, on_conflict="date,base_currency,target_currency")
            .execute()
        )

        if hasattr(response, "error") and response.error:
            logging.error(f"Failed to upsert rows: {response.error}")
        else:
            logging.info(f"Upserted {len(rows)} rows into exchange_rates.")

        return response
    except Exception as e:
        logging.error(f"Failed to insert exchange rates: {e}", exc_info=True)
        raise
