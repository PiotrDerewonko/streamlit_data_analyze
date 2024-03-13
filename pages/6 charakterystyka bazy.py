from datetime import datetime

import pandas as pd
import streamlit as st
from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.about_db.checkbox import add_check_box
from pages.about_db.data import download_data
from pages.charakterystyka_bazy.download_data import download_data_about_age
from pages.charakterystyka_bazy.modificate_data import to_100_percent, download_char

sorce_main = dotenv_values('.env')
sorce_main = list(sorce_main.values())[0]
mailings, con, engine = deaful_set(f'{sorce_main}')
refresh_data = 'False'

years = st.slider(min_value=2008, max_value=datetime.now().year,
                  value=[datetime.now().year - 5, datetime.now().year],
                  label='Wybierz lata do analizy')
with st.container(height=1200):
    char_options_df = add_check_box()
    # Miejsce na tutul wykresu zycia darczynocw
    title = st.text_input('Miejsce na tytuł wykresu', key='about_db_label')

    # pobieram dane
    data = download_data(con, refresh_data)
    data = data.loc[(data['rok'] >= years[0]) & (data['rok'] <= years[1])]
    data['rok'] = data['rok'].astype(int)
    data['rok'] = data['rok'].astype(str)

    # zmienne pomocnicze
    list_of_column = ['rodzaj']
    is_amount = char_options_df['Opcje'].loc[char_options_df['Nazwa parametru'] == 'wplata'].iloc[0]
    is_base = char_options_df['Opcje'].loc[char_options_df['Nazwa parametru'] == 'baza'].iloc[0]
    is_return = char_options_df['Opcje'].loc[char_options_df['Nazwa parametru'] == 'zwroty'].iloc[0]
    is_limitations = char_options_df['Opcje'].loc[char_options_df['Nazwa parametru'] == 'ograniczenie'].iloc[0]

    # sprawdzam ktore opcje wchodza w kolumny
    if is_amount:
        list_of_column.append('wplata')
    if is_base == False:
        data.drop(data.loc[data['rodzaj'] == 'baza'].index, inplace=True)
    if is_return == False:
        data.drop(data.loc[data['rodzaj'] == 'zwroty'].index, inplace=True)
    if is_limitations == False:
        data.drop(data.loc[data['rodzaj'] == 'ograniczenie'].index, inplace=True)

    pivot = pd.pivot_table(index='rok', columns=list_of_column, values='id_korespondenta', aggfunc='count', data=data)
    if is_amount:
        flattened_columns = pivot.columns.map('_'.join)
        pivot.columns = flattened_columns

    tab1_a, tab2_a = st.tabs(['Wykres wartośc', 'Wykres do 100 procent'])
    with tab1_a:
        char_value = download_char(pivot, data, ['rok'],
                                   f'Przyrost darczyńców na przestrzeni lat {years[0]} - {years[1]}')
        st.bokeh_chart(char_value)
        with st.expander(label='Dane tabelaryczne'):
            st.dataframe(pivot)
    with tab2_a:
        pivot = to_100_percent(pivot, is_amount)
        char_value = download_char(pivot, data, ['rok'],
                                   f'Struktura przyrostu darczyńców na przestrzeni lat {years[0]} - {years[1]}')
        st.bokeh_chart(char_value)
        with st.expander(label='Dane tabelaryczne'):
            st.dataframe(pivot)

with st.container(height=1200):
    # czesc poswiecona wiekowi-------------------------
    data_age = download_data_about_age(con, False, engine)
    data_age = data_age.loc[(data_age['rok'] >= years[0]) & (data_age['rok'] <= years[1])]
    data_age['rok_dodania'].fillna(0, inplace=True)
    drop_index = data_age.loc[(data_age['rok_dodania'] == 0) | (data_age['rok_dodania'] > data_age['rok'])].index
    data_age.drop(drop_index, inplace=True)
    data_age['rok'] = data_age['rok'].astype(str)
    data_age['rok_dodania'] = data_age['rok_dodania'].astype(int)
    data_age['rok_dodania'] = data_age['rok_dodania'].astype(str)

    st.header('Podział darczyńców ze względu na wiek')
    is_empty = st.checkbox(value=False, label='Czy pokazywać brak danych')
    add_year_of_add = st.checkbox(value=False, label='Dodaj rok wejścia')
    index_data = ['rok']
    if is_empty == False:
        data_age.drop(data_age.loc[data_age['przedzial_wieku'] == 'brak danych'].index, inplace=True)
    if add_year_of_add:
        index_data.append('rok_dodania')
    tab1, tab2 = st.tabs(['Wykres wartośc', 'Wykres do 100 procent'])
    with tab1:
        pivot_table_age = pd.pivot_table(data_age, values='id_korespondenta', aggfunc='count', index=index_data,
                                         columns='przedzial_wieku')
        char_value = download_char(pivot_table_age, data_age, index_data,
                                   f'Przedzial wieku darczyńców w latach {years[0]} - {years[1]}')
        st.bokeh_chart(char_value)
        with st.expander(label='Dane tabelaryczne'):
            st.dataframe(pivot_table_age)
    with tab2:
        pivot_table_ag_to_100 = to_100_percent(pivot_table_age, False)
        char_value_100 = download_char(pivot_table_ag_to_100, data_age, index_data,
                                       f'Struktura wieku w latach {years[0]} - {years[1]}')
        st.bokeh_chart(char_value_100)
        with st.expander(label='Dane tabelaryczne'):
            st.dataframe(pivot_table_ag_to_100)
