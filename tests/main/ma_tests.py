import os
import unittest

import pandas as pd
from dotenv import dotenv_values

from database.source_db import deaful_set

env_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.env'))
sql_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../.././sql_queries/main/ma_campaign.sql'))

class MyTestCase(unittest.TestCase):
    sorce_main = None  # Inicjalizacja zmiennych na poziomie klasy
    @classmethod
    def setUpClass(cls):
        cls.sorce_main = dotenv_values(env_file_path)
        cls.sorce_main = list(cls.sorce_main.values())[0]
        cls.mailings, cls.con, cls.engine = deaful_set(f'{cls.sorce_main}')

    def test_query_ma(self):
        with open(sql_file_path, 'r') as file:
            zapytanie = file.read()
        zapytanie = zapytanie + ' Limit 1'
        data_out = pd.read_sql_query(zapytanie, self.con)
        self.assertEqual(len(data_out), 1)




if __name__ == '__main__':
    unittest.main()
