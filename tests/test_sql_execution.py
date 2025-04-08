import sys
from pathlib import Path

# Modify sys.path early (before other imports) to ensure we can import modules from employee_events.
test_dir = Path(__file__).resolve().parent
project_root = test_dir.parent
employee_events_dir = project_root / "python-package" / "employee_events"
sys.path.insert(0, str(employee_events_dir.parent))  # noqa: E402

from employee_events.sql_execution import QueryMixin  # noqa: E402
import pandas as pd  # noqa: E402, F401

class MixinTester(QueryMixin):
    def get_tables_as_list_of_tuples(self):
        return self.run_query("SELECT name FROM sqlite_master WHERE type='table'")

    def get_tables_as_dataframe(self):
        return self.pandas_query("SELECT name FROM sqlite_master WHERE type='table'")


def test_list_of_tuples():
    tester = MixinTester()
    data = tester.get_tables_as_list_of_tuples()
    assert isinstance(data, list), "Expected a list"
    if data:
        assert isinstance(data[0], tuple), "Expected a list of tuples"


def test_list_of_tables_dataframe():
    tester = MixinTester()
    df = tester.get_tables_as_dataframe()
    assert hasattr(df, "columns"), "Expected a DataFrame with columns attribute"
    assert "name" in df.columns, "Expected a column named 'name'"