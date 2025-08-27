import logging
from collections import Counter

supabase = None

def init_supabase(client):
    global supabase
    supabase = client

def deduplicate_rows(rows, keys=("date", "base_currency", "target_currency")):
    seen = {}
    for row in rows:
        key = tuple(row[k] for k in keys)
        seen[key] = row
    return list(seen.values())

def insert_exchange_rates(rows):
    if not rows:
        logging.warning("No rows to insert.")
        return

    # dedupe
    deduped_rows = deduplicate_rows(rows)
    logging.info(f"{len(rows)} rows received, deduplicated to {len(deduped_rows)} rows.")

    try:
        response = supabase.table("exchange_rates").upsert(
            deduped_rows,
            on_conflict='exchange_rates_date_base_target_key'
        ).execute()

        if hasattr(response, "error") and response.error:
            logging.error(f"Supabase insert error: {response.error}")
        else:
            logging.info(f"Inserted/updated {len(deduped_rows)} rows.")

    except Exception as e:
        logging.error(f"Failed to insert exchange rates: {e}", exc_info=True)

