import logging
from datetime import date
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from app.collector import collect_rates
from app.db import insert_exchange_rates, has_rates_for_date
from app import config

logging.basicConfig(level=config.LOG_LEVEL)
scheduler = BlockingScheduler(timezone=config.TIMEZONE)

def run_collection(target_date: date):
    logging.info(f"Running scheduled collection for {target_date}")
    try:
        rows = collect_rates(target_date)
        if not rows:
            logging.warning(f"No rates collected for {target_date}")
            return

        if not has_rates_for_date(target_date):
            insert_exchange_rates(rows)
            logging.info(f"Inserted {len(rows)} records for {target_date}")
        else:
            insert_exchange_rates(rows)  # Upsert ensures freshness
            logging.info(f"Updated {len(rows)} records for {target_date}")
    except Exception as e:
        logging.error(f"Scheduled collection failed for {target_date}: {e}", exc_info=True)

# daily
hour, minute = map(int, config.COLLECTION_TIME.split(":"))
scheduler.add_job(run_collection, CronTrigger(hour=hour, minute=minute), args=[date.today()])

# retry
for rt in config.RETRY_TIMES:
    hour, minute = map(int, rt.split(":"))
    scheduler.add_job(run_collection, CronTrigger(hour=hour, minute=minute), args=[date.today()])

scheduler.start()
