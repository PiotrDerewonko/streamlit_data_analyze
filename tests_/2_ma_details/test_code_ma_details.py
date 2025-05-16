import os

import pandas as pd
from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.ma_details_files.add_prefix import add_prefix
from pages.ma_details_files.download_data.data_about_cost_in_campaign import generate_data_about_cost_in_campaign, \
    download_data_about_cost_in_campaign
from pages.ma_details_files.download_data.data_about_pay_in_campaign import generate_data_about_pay_in_campaign, \
    download_data_about_pay_in_campaign
from pages.ma_details_files.download_data.data_about_pay_in_days import \
    generate_data_about_cost_and_circulation_in_days, generate_data_about_sum_and_count_in_days, \
    download_data_about_cost_and_circulation_in_days, download_data_about_sum_and_count_in_days
from pages.ma_details_files.download_data.data_about_people_in_campaign import generate_data_about_people_in_campaign, \
    download_data_about_people_in_campaign
from pages.ma_details_files.download_data.data_about_structure_of_pays import generate_data_about_structure_of_pays, \
    download_data_about_structure_of_pays

# Znajdź katalog główny projektu
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# Załaduj .env z katalogu głównego projektu
env_path = os.path.join(base_dir, ".env")
sorce_main = dotenv_values(env_path)
sorce_main = list(sorce_main.values())[0]
refresh_data = True
mail, con, engine = deaful_set(sorce_main)


def test_code_data_about_people_in_campaign():
    generate_data_about_people_in_campaign(con, engine, True)
    data_ma_detail = download_data_about_people_in_campaign(con, engine, True)
    if not isinstance(data_ma_detail, pd.DataFrame):
        assert False, 'zwrócone dane nie są typu DataFrame'
    if len(data_ma_detail) == 0:
        assert False, 'zwrócony plik jest Dataframe, ale jest pusty'


def test_code_data_about_pay_in_campaign():
    generate_data_about_pay_in_campaign(con, engine, True)
    data_ma_detail = download_data_about_pay_in_campaign(con, engine, True)
    if not isinstance(data_ma_detail, pd.DataFrame):
        assert False, 'zwrócone dane nie są typu DataFrame'
    if len(data_ma_detail) == 0:
        assert False, 'zwrócony plik jest Dataframe, ale jest pusty'


def test_code_data_about_cost_in_campaign():
    generate_data_about_cost_in_campaign(con, engine, True)
    data_ma_detail = download_data_about_cost_in_campaign(con, engine, True)
    assert isinstance(data_ma_detail, pd.DataFrame), "Zwrócone dane nie są typu DataFrame"
    assert len(data_ma_detail) > 0, "Zwrócony DataFrame jest pusty"


def test_code_data_about_cost_and_circulation_in_days():
    generate_data_about_cost_and_circulation_in_days(con, engine, True)
    data_ma_detail = download_data_about_cost_and_circulation_in_days(con, engine, True)
    assert isinstance(data_ma_detail, pd.DataFrame), "Zwrócone dane nie są typu DataFrame"
    assert len(data_ma_detail) > 0, "Zwrócony DataFrame jest pusty"


def test_code_data_about_sum_and_count_in_days():
    generate_data_about_sum_and_count_in_days(con, engine, True)
    data_ma_detail = download_data_about_sum_and_count_in_days(con, engine, True)
    assert isinstance(data_ma_detail, pd.DataFrame), "Zwrócone dane nie są typu DataFrame"
    assert len(data_ma_detail) > 0, "Zwrócony DataFrame jest pusty"


def test_code_data_about_structure_of_pays():
    generate_data_about_structure_of_pays(con, engine, True)
    data_ma_detail = download_data_about_structure_of_pays(con, engine, True)
    assert isinstance(data_ma_detail, pd.DataFrame), "Zwrócone dane nie są typu DataFrame"
    assert len(data_ma_detail) > 0, "Zwrócony DataFrame jest pusty"

def test_add_prefix():
    add_prefix(con, 'True', engine)
    path_to_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pages/ma_details_files/tmp_file/people_camp.csv'))
    data_to_test = pd.read_csv(path_to_csv)
    filtered_df = data_to_test.loc[data_to_test['KARTA_NA_MAILING'] == 'ZŁOTA']
    assert len(filtered_df) > 0, "Zwrócony DataFrame jest pusty"