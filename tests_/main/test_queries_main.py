import os

import pytest

from tests_.execute_sql_files import execute_sql_files

SQL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../sql_queries/1_main"))
EXCLUDE_LIMIT_FILES = {"last_mailing.sql"}


@pytest.mark.parametrize("filename, params", [
    ("increase_correspondents.sql", {"{default_camp}": "MAILING Q4", "{default_year}": "2024"}),
    ("cost_campaign.sql", {}),
    ("db_campaign.sql", {}),
    ("is_still_active.sql", {"{default_camp}": "MAILING Q4", "{default_year}": "2024"}),
    ("last_mailing.sql", {}),
    ("ma_campaign.sql", {}),
    ("pay_from_new.sql", {}),
    ("promise_gifts.sql", {}),
    ("total_cost_and_pay.sql", {}),
    ("total_new.sql", {})])
def test_sql_queries(filename, params):
    sql_file_path = os.path.join(SQL_DIR, filename)

    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()

    for key, value in params.items():
        zapytanie = zapytanie.replace(key, value)
    if filename not in EXCLUDE_LIMIT_FILES:
        zapytanie += " limit 1"

    execute_sql_files(zapytanie, filename)
