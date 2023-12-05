import datetime

import pandas as pd  # type: ignore
import streamlit as st
from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.cycle_of_life.download_data import download_data_cycle_of_life
from pages.cycle_of_life.filtr_data import filtr_data_by_year_of_add, filtr_data_by_source, filtr_data_by_year
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
    data_copy = data.copy()
    st.header('Cykl życia')
    for i in range(2008, aktualny_rok+1):
        list_of_years.append(i)
    years = st.multiselect(options=list_of_years, label='Wybierz rok pozyskania korespondenta',
                           default=[i for i in range(aktualny_rok-4, aktualny_rok+1)])

    source_db = st.multiselect(options=data['grupa_akcji_1'].drop_duplicates(), label='Wybierz grupę wejścia', default=data['grupa_akcji_1'].drop_duplicates())
    type_of_year = st.selectbox(options=['aktualny_numer_roku', 'aktualny_rok'], label='Wybierz typ roku')
    title_of_char = st.text_input('Podaj tytul wykresu')
    index_for_pivot = [type_of_year, 'rok_dodania']
    data = filtr_data_by_year_of_add(data, years)
    data = filtr_data_by_source(data, source_db)
    pivot = pd.pivot_table(data, index=index_for_pivot, columns=['udzial', 'adres', 'wplata'],
                                values='id_korespondenta', aggfunc='count')
    flattened_columns = pivot.columns.map('_'.join)
    pivot.columns = flattened_columns
    value_tab, percent_tab = st.tabs(['Wykres wartościowy', 'Wykres procentowy'])
    with value_tab:
        genarate_char(pivot, index_for_pivot, data, title_of_char)
    pivot_cum = generate_data_to_100(pivot)
    with percent_tab:
        genarate_char(pivot_cum, index_for_pivot, data, title_of_char)

    st.header('Udział pozyskanych w latach')
    year_range_slider = st.slider('Proszę wybrać lata', min_value=2008, max_value=aktualny_rok,
                                  value=[aktualny_rok - 4, aktualny_rok])
    title_of_char_years = st.text_input('Podaj tytul wykresu ')
    data_copy = filtr_data_by_year(data_copy, year_range_slider)
    data_copy['aktualny_rok'] = data_copy['aktualny_rok'].astype(str)
    data_copy['rok_dodania'] = data_copy['rok_dodania'].astype(str)
    pivot_years = pd.pivot_table(data_copy, index='aktualny_rok', columns='rok_dodania',
                                 values='id_korespondenta', aggfunc='count')
    value_tab_year, percent_tab_year = st.tabs(['Wykres wartościowy', 'Wykres procentowy'])
    pivot_years_cum = generate_data_to_100(pivot_years)
    with value_tab_year:
        genarate_char(pivot_years, ['aktualny_rok'], data_copy, title_of_char_years)
    with percent_tab_year:
        genarate_char(pivot_years_cum, ['aktualny_rok'], data_copy, title_of_char_years)


