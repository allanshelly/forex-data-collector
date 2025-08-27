import logging
from datetime import date
from app.collector import collect_rates
from app.db import insert_exchange_rates
from backfiller import backfill
from supabase import create_client
from app import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Supabase client for checking existing data
supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def has_rates_for_date(check_date: date) -> bool:
    """Return True if there is at least one record for the given date."""
    response = supabase.table("exchange_rates").select("date").eq("date", str(check_date)).limit(1).execute()
    return bool(response.data)

def main():
    today = date.today()
    start_backfill_date = date(2024, 1, 1)

    if not has_rates_for_date(start_backfill_date):
        logging.info(f"No data found for {start_backfill_date}, starting backfill...")
        backfill(start_backfill_date, today)

    logging.info(f"Collecting exchange rates for {today}")
    try:
        rows = collect_rates(today)
        if rows:
            insert_exchange_rates(rows)
            logging.info(f"Inserted {len(rows)} records for {today}")
        else:
            logging.warning(f"No exchange rates collected for {today}")

    except Exception as e:
        logging.error(f"Failed to collect exchange rates for {today}: {e}", exc_info=True)

if __name__ == "__main__":
    main()
