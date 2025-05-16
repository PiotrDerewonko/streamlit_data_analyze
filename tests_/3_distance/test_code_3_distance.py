import os

import pandas as pd
from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.custom_reports_files.download_data import generate_data_distance_first_nad_second_pay, \
    download_data_distance_first_nad_second_pay

# Znajdź katalog główny projektu
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# Załaduj .env z katalogu głównego projektu
env_path = os.path.join(base_dir, ".env")
sorce_main = dotenv_values(env_path)
sorce_main = list(sorce_main.values())[0]
refresh_data = True
mail, con, engine = deaful_set(sorce_main)


def test_code_distance():
    generate_data_distance_first_nad_second_pay(con, engine, True)
    data_ma_main = download_data_distance_first_nad_second_pay(con, engine, True)
    if not isinstance(data_ma_main, pd.DataFrame):
        assert False, 'zwrócone dane nie są typu DataFrame'
    if len(data_ma_main) == 0:
        assert False, 'zwrócony plik jest Dataframe, ale jest pusty'
