from datetime import date
import logging
from app.utils import deduplicate_rows, load_currency_converter

def collect_rates(target_date: date):
    c = load_currency_converter()
    currencies = sorted(c.currencies)
    results = []
    total_attempts = 0
    failures = 0

    for base in ["EUR", "USD"]:
        for cur in currencies:
            if cur == base:
                continue
            total_attempts += 1
            try:
                rate = c.convert(1, base, cur, date=target_date)
                results.append({
                    "date": str(target_date),
                    "base_currency": base,
                    "target_currency": cur,
                    "exchange_rate": round(rate, 6)
                })
            except Exception as e:
                failures += 1
                logging.error(f"Convert failed {base}->{cur} for {target_date}: {e}")

    deduped_rows = deduplicate_rows(results, keys=("date", "base_currency", "target_currency"))

    if getattr(c, "fallback_on_missing_rate", False) or getattr(c, "fallback_on_wrong_date", False):
        logging.warning(f"Fallback may have been used for {target_date} "
                        f"(attempted={total_attempts}, ok={len(deduped_rows)}, failed={failures}).")

    return deduped_rows
