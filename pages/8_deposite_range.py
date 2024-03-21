from datetime import datetime

import streamlit as st
from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.deposite_range.create_charts_and_dfs import create_chart_and_df_for_deposite_range, \
    create_chart_and_df_for_avg_pay_per_year
from pages.deposite_range.popover import add_popover

sorce_main = dotenv_values('.env')
sorce_main = list(sorce_main.values())[0]
mailings, con, engine = deaful_set(f'{sorce_main}')
refresh_data = 'False'

with st.container(border=True):
    # Ta podstrona ma za zadanie zaprezentowanie jak wygladaly przedzialy wplat osob ktore dokonaly choc jednej wplatyy
    # z wybranym przedzialem wplat

    # wybor danych do analizy
    deposite_range = st.selectbox(label='Wybierz przedział wpłaty',
                                  options=['[00-010)', '[010-020)', '[020-030)', '[030-040)', '[040-050)', '[050-060)',
                                           '[060-070)', '[070-080)', '[080-090)', '[090-100)', '[100-110)', '[110-120)',
                                           '[120-200)', '[200-maks)'])
    current_year = datetime.now().year
    year_range = st.slider(min_value=2008, max_value=current_year,
                           label='Wybierz zakres lat z których będą odfiltrowane osoby z wybranym przedziałem wpłaty',
                           value=[current_year - 5, current_year])
    year_range_to_analize = st.slider(min_value=2008, max_value=current_year,
                                      label='Wybierz zakres lat która mają zostać podjęte analizie',
                                      value=[current_year - 5, current_year])
    index_to_pivot_table = st.multiselect(label='Wybierz pola do wykresu',
                                          options=['grupa_akcji_3_wplaty', 'grupa_akcji_2_wplaty', 'przedzial_wieku',
                                                   'rok_dodania', 'grupa_akcji_1_dodania', 'grupa_akcji_2_dodania',
                                                   'grupa_akcji_3_dodania'],
                                          default=['grupa_akcji_3_wplaty'])
    list_to_loc = add_popover()

    title_fin = st.text_input('Miejsce na tytuł')

    realod_data = st.button('Przelicz dane')
    if realod_data:
        create_chart_and_df_for_deposite_range(title_fin, deposite_range, year_range, year_range_to_analize, con,
                                               refresh_data, index_to_pivot_table, list_to_loc)
        create_chart_and_df_for_avg_pay_per_year(year_range_to_analize, con, refresh_data)
