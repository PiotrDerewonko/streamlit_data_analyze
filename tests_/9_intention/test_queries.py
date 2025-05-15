import os

from tests_.sql_test_utils import run_sql_test

SQL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../sql_queries/9_intention"))
EXCLUDE_LIMIT_FILES = {''}

TEST_CASES = [
    ("count_intention.sql", {}),
    ("money_intentions.sql", {}),
]

test_sql_queries = run_sql_test(SQL_DIR, TEST_CASES)
