import builtins
import types
import pytest

class DummySupabaseTable:
    def __init__(self):
        self.upserts = []
        self.selections = []
        self.filters = []

    def upsert(self, rows, on_conflict=None):
        self.upserts.append((rows, on_conflict))
        return self

    def select(self, columns="*"):
        self.selections.append(columns)
        return self

    def eq(self, col, val):
        self.filters.append((col, val))
        return self

    def limit(self, n):
        return self

    def execute(self):
        # Minimal shape like supabase-py
        return types.SimpleNamespace(data=[])

class DummySupabaseClient:
    def __init__(self):
        self._table = DummySupabaseTable()
    def table(self, name):
        return self._table

@pytest.fixture
def dummy_supabase():
    return DummySupabaseClient()
