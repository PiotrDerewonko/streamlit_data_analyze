import os

import pandas as pd
import psycopg2
from dotenv import dotenv_values

from database.source_db import deaful_set

env_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.env'))

def test_main_sql():
    sorce_main = dotenv_values(env_file_path)
    sorce_main = list(sorce_main.values())[0]
    mailings, con, engine = deaful_set(f'{sorce_main}')

    # Dynamiczne tworzenie metod testowych na podstawie plików z zapytaniami SQL
    def test_generator(file):
        sql_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), f'../.././sql_queries/7/{file}'))
        with open(sql_file_path, 'r') as sql_file:
            zapytanie = sql_file.read()
            zapytanie = zapytanie.replace('{rok}', '2008')
            zapytanie_copy = zapytanie + ' limit 1'
            try:
                wynik = pd.read_sql_query(zapytanie_copy, con)
                test = len(wynik)
            except psycopg2.Error:
                assert False, f"Zapytanie SQL spowodowało błąd: dla pliku: {file}"
            except Exception:
                assert False, f"Zapytanie SQL spowodowało błąd: dla pliku: {file}"
            else:
                assert len(wynik) == 1, f"Błędna długość wyniku dla pliku: {file}"

    sql_file = 'people_from_year.sql'
    test_generator(sql_file)
