import sys
from pathlib import Path


test_dir = Path(__file__).resolve().parent
project_root = test_dir.parent
employee_events_dir = project_root / "python-package" / "employee_events"
sys.path.insert(0, str(employee_events_dir.parent))


from employee_events.sql_execution import QueryMixin
import pandas as pd


class MixinTester(QueryMixin):
    def get_tables_as_list_of_tuples(self):
        return self.run_query("SELECT name FROM sqlite_master WHERE type='table'")


    def get_tables_as_dataframe(self):
        return self.pandas_query("SELECT name FROM sqlite_master WHERE type='table'")


# Define top-level test functions
def test_list_of_tuples():
    tester = MixinTester()
    data = tester.get_tables_as_list_of_tuples()
    assert isinstance(data, list), "Expected a list"
    if data:
        assert isinstance(data[0], tuple), "Expected list of tuples"


def test_list_of_tables_dataframe():
    tester = MixinTester()
    df = tester.get_tables_as_dataframe()
    assert hasattr(df, "columns"), "Expected a DataFrame with columns attribute"
    assert "name" in df.columns, "Expected a column named 'name'"
