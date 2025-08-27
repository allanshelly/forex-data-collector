# 📊 Forex Data Collector

A Python service that collects daily foreign exchange rates from the **European Central Bank (ECB)** using the `CurrencyConverter` package and stores them in **Supabase**.  
Runs in Docker with automatic scheduling and retry handling.

---

## ⚙️ Features
- Collects **EUR → 41 currencies** and **USD → 41 currencies** (total **82 pairs daily**)
- Stores results in Supabase (`exchange_rates` table)
- Automatic backfill from **2024-01-01 → today**
- Daily scheduled job at **16:30 CET** with **retries at 17:30 & 18:30 CET**
- Fallback mechanism if ECB data is not yet published
- Local caching of ECB data files
- Robust logging and error handling
- Dockerized for easy deployment

---

## 🗄 Database Schema
Make sure your Supabase project has this table:

```sql
CREATE TABLE exchange_rates (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    base_currency VARCHAR(3) NOT NULL,
    target_currency VARCHAR(3) NOT NULL,
    exchange_rate DECIMAL(18, 6) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(date, base_currency, target_currency)
);
```

## 🔐 Environment Variables

Create a .env file:

```SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Scheduler config
COLLECTION_TIME=16:30   # Daily collection time (CET)
RETRY_TIMES=17:30,18:30 # Retry attempts (CET)
TIMEZONE=Europe/Zurich  # Timezone

# Logging
LOG_LEVEL=INFO
```

##🐳 Docker Setup
Build & Run
``docker build -t forex-collector .``
``docker run --env-file .env forex-collector``

Docker Compose (recommended)
``docker-compose up --build``

🏃 Running Locally (without Docker)

Install dependencies:

``pip install -r requirements.txt``


Run backfill + today’s collection:

``python -m app.main``


Run the scheduler (background collection):

``python -m app.scheduler``

##📦 Project Structure
```
 app/
 	├── backfiller.py    # (legacy) optional backfill script
 	├── collector.py     # rate collection logic
 	├── config.py        # env vars + paths
 	├── db.py            # Supabase integration
 	├── main.py          # backfill + today's run
 	├── scheduler.py     # APScheduler jobs
 	├── utils.py         # helpers (cache, dedupe, etc.)
.env.example
.docker-compose.yaml
dockerfile
README.md
requirements.txt
```

##✅ Development Notes

- Uses CurrencyConverterwith ECB_URL for historical rates.
- ECB updates daily ~16:00 CET. Weekends/holidays have no new rates → system retries & uses fallback until next business day.
- Cache files are stored in /app/cache/ecb_YYYY-MM-DD.xml.
- All inserts use Supabase upsert to avoid duplicates.
