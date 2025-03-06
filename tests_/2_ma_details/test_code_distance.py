import os

import pandas as pd
from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.ma_details_files.download_data.data_about_people_in_campaign import generate_data_about_people_in_campaign, \
    download_data_about_people_in_campaign

# Znajdź katalog główny projektu
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# Załaduj .env z katalogu głównego projektu
env_path = os.path.join(base_dir, ".env")
sorce_main = dotenv_values(env_path)
sorce_main = list(sorce_main.values())[0]
refresh_data = True
mail, con, engine = deaful_set(sorce_main)


def test_code_distance():
    generate_data_about_people_in_campaign(con, engine, True)
    data_ma_detail = download_data_about_people_in_campaign(con, engine, True)
    if not isinstance(data_ma_detail, pd.DataFrame):
        assert False, 'zwrócone dane nie są typu DataFrame'
    if len(data_ma_detail) == 0:
        assert False, 'zwrócony plik jest Dataframe, ale jest pusty'
