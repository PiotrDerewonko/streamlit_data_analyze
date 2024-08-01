import os

from tests_.execute_sql_files import execute_sql_files


def test_people_from_year_sql():
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), f'../.././sql_queries/7/people_from_year.sql'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()
        zapytanie = zapytanie.replace('{rok}', '2008')
        zapytanie_copy = zapytanie + ' limit 1'
        execute_sql_files(zapytanie_copy, 'people_from_year')


def test_pay_on_year_sql():
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), f'../.././sql_queries/7/pay_on_year.sql'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()
        zapytanie = zapytanie.replace('{rok}', '2008')
        zapytanie_copy = zapytanie + ' limit 1'
        execute_sql_files(zapytanie_copy, 'pay_on_year')


def test_mailing_sql():
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), f'../.././sql_queries/7/mailing.sql'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()
        zapytanie = zapytanie.replace('{rok}', '2008')
        zapytanie_copy = zapytanie + ' limit 1'
        execute_sql_files(zapytanie_copy, 'mailing')


def test_good_adress_sql():
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), f'../.././sql_queries/7/good_adress.sql'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()
        zapytanie_copy = zapytanie + ' limit 1'
        execute_sql_files(zapytanie_copy, 'good_adress')


def test_current_mailing_sql():
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), f'../.././sql_queries/7/current_mailing.sql'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()
        zapytanie = zapytanie.replace('{rok}', '2008')
        zapytanie_copy = zapytanie + ' limit 1'
        execute_sql_files(zapytanie_copy, 'current_mailing')
