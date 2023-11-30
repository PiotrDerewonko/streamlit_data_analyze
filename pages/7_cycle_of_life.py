import datetime

import pandas as pd
import streamlit as st
from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.cycle_of_life.download_data import download_data_cycle_of_life
from pages.cycle_of_life.filtr_data import filtr_data_by_year_of_add
from pages.cycle_of_life.genarate_data_to_100 import generate_data_to_100
from pages.cycle_of_life.generate_char_of_value import genarate_char

sorce_main = dotenv_values('.env')
sorce_main = list(sorce_main.values())[0]
mailings, con, engine = deaful_set(f'{sorce_main}')
refresh_data = 'False'

with st.container():
    list_of_years = []
    aktualny_rok = int(datetime.datetime.now().year)
    data = download_data_cycle_of_life(con, refresh_data)
    for i in range(2008, aktualny_rok+1):
        list_of_years.append(i)
    years = st.multiselect(options=list_of_years, label='Wybierz rok pozyskania korespondenta',
                           default=[i for i in range(aktualny_rok-4, aktualny_rok+1)])
    type_of_year = st.selectbox(options=['aktualny_rok', 'aktualny_numer_roku'], label='Wybierz typ roku')
    index_for_pivot = [type_of_year, 'rok_dodania']
    data = filtr_data_by_year_of_add(data, years)
    pivot = pd.pivot_table(data, index=index_for_pivot, columns=['udzial', 'adres', 'wplata'],
                                values='id_korespondenta', aggfunc='count')
    flattened_columns = pivot.columns.map('_'.join)
    pivot.columns = flattened_columns
    value_tab, percent_tab = st.tabs(['Wykres wartościowy', 'Wykres procentowy'])
    with value_tab:
        genarate_char(pivot, index_for_pivot, data)
    pivot_cum = generate_data_to_100(pivot)
    with percent_tab:
        genarate_char(pivot_cum, index_for_pivot, data)
