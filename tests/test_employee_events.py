import pytest

from pathlib import Path


# 1) Create a project_root variable set to the absolute path
# for the *root* of your project directory.
# Since this file is inside "tests/", we move up one level
# to get the project root (which contains python-package, report, 
# assets, etc.).
project_root = Path(__file__).resolve().parent.parent


# 2) Create a pytest fixture called `db_path`.
#    This fixture returns a Path object pointing to your 
#     employee_events.db file.
@pytest.fixture
def db_path():
    # The DB is located in: python-package/employee_events/employee_events.db
    return (project_root 
        / "python-package" / "employee_events" / "employee_events.db")


# 3) Define a function called `test_db_exists` that accepts `db_path`.
#    We check if the DB file physically exists.
def test_db_exists(db_path):
    assert db_path.is_file(), f"Database file not found at {db_path}"


@pytest.fixture
def db_conn(db_path):
    from sqlite3 import connect

    return connect(db_path)


@pytest.fixture
def table_names(db_conn):
    """
    Returns a list of table names in the employee_events.db database.
    """
    name_tuples = db_conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()

    return [x[0] for x in name_tuples]


# 4) Define a test function `test_employee_table_exists`.
#    It receives the `table_names` fixture and checks that "employee"
#    is in that list.
def test_employee_table_exists(table_names):
    assert ("employee" in table_names, 
        "employee table does not exist in the database.")


# 5) Define a test function `test_team_table_exists`.
def test_team_table_exists(table_names):
    assert ("team" in table_names, 
        "team table does not exist in the database.")


# 6) Define a test function `test_employee_events_table_exists`.
def test_employee_events_table_exists(table_names):
    assert (
        "employee_events" in table_names
    ), "employee_events table does not exist in the database."
