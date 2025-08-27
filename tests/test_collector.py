from datetime import date
import types

def test_collects_82_pairs(monkeypatch):
    # Mock CurrencyConverter with minimal API
    class DummyCC:
        def __init__(self, *args, **kwargs):
            self.fallback_on_missing_rate = kwargs.get("fallback_on_missing_rate", True)
            self.currencies = {"EUR","USD","JPY","AUD","GBP","CHF","CAD","SEK","NOK","DKK",
                               "PLN","CZK","HUF","RON","BGN","HRK","TRY","BRL","MXN","CNY",
                               "HKD","SGD","KRW","INR","ZAR","NZD","ILS","AED","SAR","RUB",
                               "THB","MYR","IDR","PHP","TWD","ISK","ARS","CLP","COP","PEN",
                               "VND","UAH"}  # 42 incl. EUR, USD -> 41 targets each
        def convert(self, amt, base, cur, date=None):
            return 1.234567  # dummy

    # Patch loader to return our dummy converter
    from app import collector
    def fake_loader():
        return DummyCC(fallback_on_missing_rate=True)
    monkeypatch.setattr(collector, "load_currency_converter", fake_loader)

    rows = collector.collect_rates(date(2024,1,2))
    # EUR target count = 41, USD target count = 41 -> total 82
    assert len(rows) == 82
    # basic row shape
    sample = rows[0]
    assert {"date","base_currency","target_currency","exchange_rate"} <= set(sample.keys())
