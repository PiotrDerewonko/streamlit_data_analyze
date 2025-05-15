import os

from tests_.sql_test_utils import run_sql_test

SQL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../sql_queries/10_chart_in_days"))
EXCLUDE_LIMIT_FILES = {''}

TEST_CASES = [
    ("action_three_id.sql", {}),
    ("action_two_id.sql", {}),
    ("cost_and_cirtulation_for_char_days.sql", {"#A#": '9', "#B#": '2',"#C#": '9'}),
    ("count_and_sum_amount_for_char_days.sql",  {"#A#": '9', "#B#": '2',"#C#": '9'}),
]

test_sql_queries = run_sql_test(SQL_DIR, TEST_CASES)
