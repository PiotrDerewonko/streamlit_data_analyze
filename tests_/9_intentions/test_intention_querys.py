import os

from tests_.execute_sql_files import execute_sql_files


def test_count_intentions():
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), f'../.././sql_queries/9_intention/count_intention.sql'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()
        zapytanie_copy = zapytanie + ' limit 1'
        execute_sql_files(zapytanie_copy, 'count_intentions.sql')

def test_money_intentions():
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), f'../.././sql_queries/9_intention/money_intentions.sql'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()
        zapytanie_copy = zapytanie + ' limit 1'
        execute_sql_files(zapytanie_copy, 'count_intentions.sql')