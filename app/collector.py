from currency_converter import CurrencyConverter, ECB_URL
from datetime import date
from app.db import insert_exchange_rates
from app.utils import deduplicate_rows
import logging
from pprint import pformat

def collect_rates(target_date: date):
    c = CurrencyConverter(
        ECB_URL,
        fallback_on_missing_rate=True,
        fallback_on_wrong_date=True
    )

    currencies = sorted(c.currencies)
    results = []

    # eur → others
    for cur in currencies:
        if cur == "EUR":
            continue
        rate = c.convert(1, "EUR", cur, date=target_date)
        results.append({
            "date": str(target_date),
            "base_currency": "EUR",
            "target_currency": cur,
            "exchange_rate": round(rate, 6)
        })

    # usd → others
    eur_to_usd = c.convert(1, "EUR", "USD", date=target_date)
    for cur in currencies:
        if cur in ["USD", "EUR"]:
            continue
        eur_to_cur = c.convert(1, "EUR", cur, date=target_date)
        usd_to_cur = eur_to_cur / eur_to_usd
        results.append({
            "date": str(target_date),
            "base_currency": "USD",
            "target_currency": cur,
            "exchange_rate": round(usd_to_cur, 6)
        })

    # dedupe
    deduped_rows = deduplicate_rows(results, keys=("date", "base_currency", "target_currency"))

    # insert
    insert_exchange_rates(deduped_rows)

    logging.info(f"Inserted {len(results)} records for {target_date}")
