import pandas as pd
from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.main_diractor.dowload_data_main_db import generate_data_main_db, download_data_main_db
from pages.main_diractor.dowload_data_main_ma import generate_data_main_ma, download_data_main_ma

sorce_main = dotenv_values('../../.env')
sorce_main = list(sorce_main.values())[0]
refresh_data = True
mail, con, engine = deaful_set(sorce_main)

def test_main_ma():
    generate_data_main_ma(con, engine, True)
    data_ma_main = download_data_main_ma(con, engine, True)
    if not isinstance(data_ma_main, pd.DataFrame):
        assert False, 'zwrócone dane nie są typu DataFrame'
    if len(data_ma_main) == 0:
        assert False, 'zwrócony plik jest Dataframe, ale jest pusty'


def test_main_db():
    generate_data_main_db(con, engine, True)
    data_db_main = download_data_main_db(con, engine, True)
    if not isinstance(data_db_main, pd.DataFrame):
        assert False, 'zwrócone dane nie są typu DataFrame'
    if len(data_db_main) == 0:
        assert False, 'zwrócony plik jest Dataframe, ale jest pusty'