import os
import unittest

import pandas as pd
import psycopg2
from dotenv import dotenv_values

from database.source_db import deaful_set

env_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.env'))
directory_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../.././sql_queries/main'))


def list_files_in_directory(directory):
    file_list = os.listdir(directory)
    return file_list


# Wywołanie funkcji i zapisanie listy plików
files = list_files_in_directory(directory_path)


class MyTestCase(unittest.TestCase):
    sorce_main = None  # Inicjalizacja zmiennych na poziomie klasy

    @classmethod
    def setUpClass(cls):
        cls.sorce_main = dotenv_values(env_file_path)
        cls.sorce_main = list(cls.sorce_main.values())[0]
        cls.mailings, cls.con, cls.engine = deaful_set(f'{cls.sorce_main}')


# Dynamiczne tworzenie metod testowych na podstawie plików z zapytaniami SQL
for i, file in enumerate(files):
    def test_generator(file):
        def test(self):
            sql_file_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), f'../.././sql_queries/main/{file}'))
            with open(sql_file_path, 'r') as sql_file:
                zapytanie = sql_file.read()
                if file != 'find_last_campaign.sql':
                    zapytanie = zapytanie + ' Limit 1'
                try:
                    wynik = pd.read_sql_query(zapytanie, self.con)
                    test = len(wynik)
                except psycopg2.Error:
                    self.fail(f"Zapytanie SQL spowodowało błąd: dla pliku: {file}")
                except Exception:
                    self.fail(f"Zapytanie SQL spowodowało błąd: dla pliku: {file}")
                else:
                    self.assertEqual(len(wynik), 1, f"Błędna długość wyniku dla pliku: {file}")

        return test


    test_name = f"test_query_{i}"
    test_func = test_generator(file)
    setattr(MyTestCase, test_name, test_func)

if __name__ == '__main__':
    unittest.main()
