import logging
from datetime import date
from app.collector import collect_rates
from app.db import insert_exchange_rates

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    today = date.today()
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
