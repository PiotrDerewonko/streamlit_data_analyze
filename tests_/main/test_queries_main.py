import os

from tests_.sql_test_utils import run_sql_test

SQL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../sql_queries/1_main"))
EXCLUDE_LIMIT_FILES = {"last_mailing.sql"}

TEST_CASES = [
    ("increase_correspondents.sql", {"{default_camp}": "MAILING Q4", "{default_year}": "2024"}),
    ("cost_campaign.sql", {}),
    ("db_campaign.sql", {}),
    ("is_still_active.sql", {"{default_camp}": "MAILING Q4", "{default_year}": "2024"}),
    ("last_mailing.sql", {}),
    ("ma_campaign.sql", {}),
    ("pay_from_new.sql", {}),
    ("promise_gifts.sql", {}),
    ("total_cost_and_pay.sql", {}),
    ("total_new.sql", {})]
test_sql_queries = run_sql_test(SQL_DIR, TEST_CASES, EXCLUDE_LIMIT_FILES)
