import os

import pandas as pd
import psycopg2
from dotenv import dotenv_values

from database.source_db import deaful_set


def execute_sql_files(zapytanie_copy, file):
    env_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../.env'))
    sorce_main = dotenv_values(env_file_path)
    sorce_main = list(sorce_main.values())[0]
    mailings, con, engine = deaful_set(f'{sorce_main}')
    try:
        wynik = pd.read_sql_query(zapytanie_copy, con)
    except psycopg2.Error:
        assert False, f"Zapytanie SQL spowodowało błąd: dla pliku: {file}"
    except Exception:
        assert False, f"Zapytanie SQL spowodowało błąd: dla pliku: {file}"
    else:
        assert len(wynik) == 1, f"Błędna długość wyniku dla pliku: {file}"