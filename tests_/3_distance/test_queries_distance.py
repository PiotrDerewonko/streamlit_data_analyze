import os

from tests_.sql_test_utils import run_sql_test

SQL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../sql_queries/3_distance_1_and_second_pay"))
EXCLUDE_LIMIT_FILES = {''}

TEST_CASES = [
    ("data_about_correspondents.sql", {"{default_camp}": "MAILING Q4", "{default_year}": "2024"}),
    ("data_about_pay.sql", {})]

test_sql_queries = run_sql_test(SQL_DIR, TEST_CASES)
