from datetime import datetime

import streamlit as st
from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.deposite_range.download_data import download_data, create_pivot_table

sorce_main = dotenv_values('.env')
sorce_main = list(sorce_main.values())[0]
mailings, con, engine = deaful_set(f'{sorce_main}')
refresh_data = 'False'

with st.container():
    # Ta podstrona ma za zadanie zaprezentowanie jak wygladaly przedzialy wplat osob ktore dokonaly choc jednej wplatyy
    # z wybranym przedzialem wplat

    # wybor danych do analizy
    deposite_range = st.selectbox(label='Wybierz przedział wpłaty', options=['[100-110)', '[020-030)', '[200-maks)'])
    current_year = datetime.now().year
    year_range = st.slider(min_value=2008, max_value=current_year,
                           label='Wybierz zakres lat z których będą odfiltrowane osoby z wybranym przedziałem wpłaty',
                           value=[current_year - 5, current_year])
    year_range_to_analize = st.slider(min_value=2008, max_value=current_year,
                                      label='Wybierz zakres lat która mają zostać podjęte analizie',
                                      value=[current_year - 5, current_year])
    index_to_pivot_table = st.multiselect(label='Wybierz pola do wykresu',
                                          options=['grupa_akcji_3_wplaty', 'grupa_akcji_2_wplaty'],
                                          default=['grupa_akcji_3_wplaty'])


    def create_chart_and_df():
        data = download_data(deposite_range, year_range, year_range_to_analize, con, refresh_data)
        pivot = create_pivot_table(data, index_to_pivot_table)
        st.dataframe(pivot)



    realod_data = st.button('Przelicz dane')
    if realod_data:
        create_chart_and_df()
