from supabase import create_client
import os

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def insert_exchange_rates(rows: list[dict]):
    return supabase.table("exchange_rates").upsert(rows).execute()
