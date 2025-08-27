import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

COLLECTION_TIME = os.getenv("COLLECTION_TIME", "16:30")
RETRY_TIMES = os.getenv("RETRY_TIMES", "17:30,18:30").split(",")
TIMEZONE = os.getenv("TIMEZONE", "Europe/Zurich")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

CACHE_DIR = Path("data")
CACHE_DIR.mkdir(exist_ok=True)
