import logging
from datetime import date
from app.collector import collect_rates

logging.basicConfig(level=logging.INFO)

def main():
    today = date.today()
    logging.info(f"Collecting exchange rates for {today}")
    collect_rates(today)

if __name__ == "__main__":
    main()
