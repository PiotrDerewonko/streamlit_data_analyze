import datetime
import os

import pandas as pd
import streamlit as st

from pages.cycle_of_life.add_corr import (download_correspondent_data, download_pay_data, download_mailings,
                                          download_good_adress, modificate_data)


@st.cache_data(ttl=7200)
def download_data_cycle_of_life(_con, refresh_data) -> pd.DataFrame:
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_file/data_cycle_of_life.csv'))
    if refresh_data == 'True':
        aktualny_rok = int(datetime.datetime.now().year)
        data_all = pd.DataFrame()
        #todo sqle do porawki
        data_all = download_correspondent_data(_con, aktualny_rok, data_all)
        data_all = download_pay_data(_con, data_all, aktualny_rok)
        data_all = download_mailings(_con, data_all, aktualny_rok)
        data_all = download_good_adress(_con, data_all)
        data_all = modificate_data(data_all)
        data_all.to_csv(csv_path)
    data = pd.read_csv(csv_path, index_col='Unnamed: 0', low_memory=False)
    return data
