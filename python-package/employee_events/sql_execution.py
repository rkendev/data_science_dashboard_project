from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd


db_path = Path(__file__).resolve().parent / "employee_events.db"


class QueryMixin:
    def pandas_query(self, sql_query_string):
        """
        Execute a query using Pandas, returning a DataFrame.
        """
        with connect(db_path) as conn:
            df = pd.read_sql(sql_query_string, conn)
        return df

    # Rename 'query' to something else (e.g. 'run_query')
    def run_query(self, sql_query_string):
        """
        Execute a query using a cursor, returning a list of tuples.
        """
        with connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query_string)
            data = cursor.fetchall()
        return data

    # Leave this code unchanged
    def query(func):
        """
        Decorator that runs a standard sql execution
        and returns a list of tuples
        """

        @wraps(func)
        def run_query(*args, **kwargs):
            query_string = func(*args, **kwargs)
            connection = connect(db_path)
            cursor = connection.cursor()
            result = cursor.execute(query_string).fetchall()
            connection.close()
            return result

        return run_query
