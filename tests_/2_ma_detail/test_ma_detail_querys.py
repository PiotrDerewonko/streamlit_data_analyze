import os

from tests_.execute_sql_files import execute_sql_files


def test_people_from_year_sql():
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), f'../.././sql_queries/2_ma_detail/age.sql'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()
        zapytanie = zapytanie.replace('#A#', '2008')
        zapytanie_copy = zapytanie + ' limit 1'
        execute_sql_files(zapytanie_copy, 'age')


def test_cost_and_cirtulation_for_char_days_sql():
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     f'../.././sql_queries/2_ma_detail/cost_and_cirtulation_for_char_days.sql'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()
        zapytanie = zapytanie.replace('#A#', '10')
        zapytanie = zapytanie.replace('#B#', '10')
        zapytanie = zapytanie.replace('#C#', '10')
        zapytanie_copy = zapytanie + ' limit 1'
        execute_sql_files(zapytanie_copy, 'cost_and_cirtulation_for_char_days')


def test_count_and_sum_amount_char_for_days_sql():
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     f'../.././sql_queries/2_ma_detail/count_and_sum_amount_char_for_days.sql'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()
        zapytanie = zapytanie.replace('#A#', '10')
        zapytanie = zapytanie.replace('#B#', '10')
        zapytanie = zapytanie.replace('#C#', '10')
        zapytanie_copy = zapytanie + ' limit 1'
        execute_sql_files(zapytanie_copy, 'count_and_sum_amount_char_for_days')


def test_find_last_mailing_sql():
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), f'../.././sql_queries/2_ma_detail/find_last_mailing.sql'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()
        zapytanie = zapytanie.replace('#A#', '2008')
        zapytanie = zapytanie.replace('#B#', '2008')
        zapytanie = zapytanie.replace('#C#', '2008')
        execute_sql_files(zapytanie, 'find_last_mailing')


def test_is_vip_for_year_sql():
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), f'../.././sql_queries/2_ma_detail/is_vip_for_year.sql'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()
        zapytanie = zapytanie.replace('#A#', '2008')
        zapytanie = zapytanie.replace('#B#', '2008')
        zapytanie_copy = zapytanie + ' limit 1'
        execute_sql_files(zapytanie_copy, 'is_vip_for_year')


def test_origin_material_sql():
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), f'../.././sql_queries/2_ma_detail/origin_material.sql'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()
        zapytanie_copy = zapytanie + ' limit 1'
        execute_sql_files(zapytanie_copy, 'origin_material')


def test_paymant_from_mailing_sql():
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), f'../.././sql_queries/2_ma_detail/paymant_from_mailing.sql'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()
        zapytanie_copy = zapytanie + ' limit 1'
        execute_sql_files(zapytanie_copy, 'paymant_from_mailing')
