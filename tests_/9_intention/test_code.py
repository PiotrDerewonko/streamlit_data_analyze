import pandas as pd

from pages.intentions.download_data import *
import os
from dotenv import dotenv_values
from database.source_db import deaful_set


# Znajdź katalog główny projektu
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# Załaduj .env z katalogu głównego projektu
env_path = os.path.join(base_dir, ".env")
sorce_main = dotenv_values(env_path)
sorce_main = list(sorce_main.values())[0]
refresh_data = True
mail, con, engine = deaful_set(sorce_main)


def test_generate_intention_money():
    generate_data_for_intention_report_money(con, engine, True)
    data = download_data_for_intention_report_money(con, engine, True)
    assert isinstance(data, pd.DataFrame), 'Zwrócony plik nie jest data frame'
    assert len(data) > 0, 'Zwrocony plik jest pusty'

def test_generate_intention_count():
    generate_data_for_intention_report_count(con, engine, True)
    data = download_data_for_intention_report_count(con, engine, True)
    assert isinstance(data, pd.DataFrame), 'Zwrócony plik nie jest data frame'
    assert len(data) > 0, 'Zwrocony plik jest pusty'