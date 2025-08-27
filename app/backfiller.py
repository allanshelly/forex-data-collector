import logging
from datetime import date, timedelta
from app.collector import collect_rates

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def backfill(start_date: date, end_date: date):
    """
    Collect and insert historical exchange rates from start_date to end_date.
    """
    logging.info(f"Starting backfill from {start_date} to {end_date}")
    current = start_date

    while current <= end_date:
        try:
            logging.info(f"Collecting rates for {current}")
            # collector handles deduplication and insertion
            collect_rates(current)
        except Exception as e:
            logging.error(f"Failed to collect rates for {current}: {e}", exc_info=True)
        current += timedelta(days=1)

    logging.info("Backfill complete!")

if __name__ == "__main__":
    start_date = date(2024, 1, 1)
    end_date = date.today()
    backfill(start_date, end_date)
