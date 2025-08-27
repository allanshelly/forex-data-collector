from datetime import date
from app import db

def test_insert_calls_upsert(monkeypatch, dummy_supabase):
    # Patch module-level client
    monkeypatch.setattr(db, "supabase", dummy_supabase)

    rows = [
        {"date": "2024-01-02", "base_currency": "EUR", "target_currency": "USD", "exchange_rate": 1.1}
    ]
    db.insert_exchange_rates(rows)
    assert dummy_supabase._table.upserts, "Expected an upsert call"
    up_rows, conflict = dummy_supabase._table.upserts[-1]
    assert up_rows == rows
    assert "date" in conflict and "base_currency" in conflict and "target_currency" in conflict

def test_has_rates_for_date(monkeypatch, dummy_supabase):
    monkeypatch.setattr(db, "supabase", dummy_supabase)
    # default Dummy returns empty -> False
    assert db.has_rates_for_date(date(2024,1,2)) is False
