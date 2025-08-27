import logging
from datetime import date, timedelta
from app.collector import collect_rates
from app.db import insert_exchange_rates
from supabase import create_client
from app import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def get_existing_dates() -> set[date]:
    response = supabase.table("exchange_rates").select("date").execute()
    if response.data:
        return {date.fromisoformat(row["date"]) for row in response.data}
    return set()

def backfill_missing_dates(start_date: date, end_date: date):
    existing_dates = get_existing_dates()
    current = start_date

    while current <= end_date:
        if current not in existing_dates:
            logging.info(f"Missing data for {current}, collecting...")
            try:
                rows = collect_rates(current)
                if rows:
                    insert_exchange_rates(rows)
                    logging.info(f"Backfilled {len(rows)} records for {current}")
                else:
                    logging.warning(f"No rates collected for {current}")
            except Exception as e:
                logging.error(f"Failed to collect rates for {current}: {e}", exc_info=True)
        current += timedelta(days=1)

def main():
    today = date.today()
    start_date = date(2024, 1, 1)

    backfill_missing_dates(start_date, today)

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
