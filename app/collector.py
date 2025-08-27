from datetime import date
import logging
from app.utils import deduplicate_rows, load_currency_converter

def collect_rates(target_date: date):
    c = load_currency_converter()

    currencies = sorted(c.currencies)
    results = []

    for base in ["EUR", "USD"]:
        for cur in currencies:
            if cur == base:
                continue
            try:
                rate = c.convert(1, base, cur, date=target_date)
                results.append({
                    "date": str(target_date),
                    "base_currency": base,
                    "target_currency": cur,
                    "exchange_rate": round(rate, 6)
                })
            except Exception as e:
                logging.error(f"Failed to convert {base}->{cur} for {target_date}: {e}")

    # dedupe
    deduped_rows = deduplicate_rows(results, keys=("date", "base_currency", "target_currency"))

    # fallback
    if getattr(c, "fallback_on_missing_rate", False):
        logging.warning(f"Fallback rates may have been used for {target_date}")

    return deduped_rows
