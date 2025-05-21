import os

from tests_.sql_test_utils import run_sql_test

SQL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../sql_queries/2_ma_detail"))
EXCLUDE_LIMIT_FILES = {"find_last_mailing.sql"}

TEST_CASES = [
    ("age.sql", {"#A#": '2025'}),
    ("cost_and_circulation_for_char_days.sql", {"#A#": '9', "#B#": '18', "#C#": '17'}),
    ("count_and_sum_amount_char_for_days.sql", {"#A#": '9', "#B#": '18', "#C#": '17'}),
    ("find_last_mailing.sql", {}),
    ("is_vip_for_year.sql", {"#A#": '2025', "#B#": '2024'}),
    ("origin_material.sql", {}),
    ("paymant_from_mailing.sql", {}),
    ("people_camp_data.sql", {}),
    ("short_names.sql", {}),
    ("payment_from_mailingv2.sql", {}),
    ("big_cost.sql", {}),
    ("people_camp_data.sql", {}),
    ("card_for_mailings.sql", {}),
    ("all_people.sql", {}),
    ("chosen_city.sql", {}),
    ("count_of_pays_in_year.sql", {"#A#": '2024'}),
    ("how_many_rosary_have.sql", {}),
    ("is_correspondent_has_product.sql", {"#A#": str('MAGAZYN_DZIEKUJE_Q2_2017 po koszcie 0.263')}),
    ("card_for_mailings.sql", {}),
    ("is_in_rosary.sql", {}),
    ("list_of_products.sql", {}),
    ("people_source.sql", {}),
    ("postal_districts.sql", {}),
]
test_sql_queries = run_sql_test(SQL_DIR, TEST_CASES, EXCLUDE_LIMIT_FILES)
