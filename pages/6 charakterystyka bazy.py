import pandas as pd
import streamlit as st
from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.about_db.checkbox import add_check_box
from pages.about_db.data import download_data

sorce_main = dotenv_values('.env')
sorce_main = list(sorce_main.values())[0]
mailings, con, engine = deaful_set(f'{sorce_main}')
refresh_data = 'False'
with st.container():
    char_options_df = add_check_box()
    #Miejsce na tutul wykresu zycia darczynocw
    title = st.text_input('Miejsce na tytuł wykresu', key='about_db_label')

    #pobieram dane
    data = download_data(con, refresh_data)

    #zmienne pomocnicze
    list_of_column = ['rodzaj']
    is_amount = char_options_df['Opcje'].loc[char_options_df['Nazwa parametru'] == 'wplata'].iloc[0]
    is_base = char_options_df['Opcje'].loc[char_options_df['Nazwa parametru'] == 'baza'].iloc[0]
    is_return = char_options_df['Opcje'].loc[char_options_df['Nazwa parametru'] == 'zwroty'].iloc[0]
    is_limitations = char_options_df['Opcje'].loc[char_options_df['Nazwa parametru'] == 'ograniczenie'].iloc[0]
    is_100 = char_options_df['Opcje'].loc[char_options_df['Nazwa parametru'] == 'czy_do_100'].iloc[0]

    #sprawdzam ktore opcje wchodza w kolumny
    if is_amount:
        list_of_column.append('wplata')
    if is_base == False:
        data.drop(data.loc[data['rodzaj'] == 'baza'].index, inplace=True)
    if is_return == False:
        data.drop(data.loc[data['rodzaj'] == 'zwroty'].index, inplace=True)
    if is_limitations == False:
        data.drop(data.loc[data['rodzaj'] == 'ograniczenie'].index, inplace=True)

    pivot = pd.pivot_table(index='rok', columns=list_of_column, values='id_korespondenta', aggfunc='count', data=data)
    if is_100:
        pivot.fillna(0, inplace=True)
        pivot['sum'] = 0
        if is_amount:
            sum_check = ('sum', '')
        else:
            sum_check = 'sum'
        for i in pivot.columns:
            if i != sum_check:
                pivot['sum'] = pivot['sum'] + pivot[i]
        tmp_df = pivot.copy()
        for j in pivot.columns:
            if j != sum_check:
                tmp_df[j] = tmp_df['sum']
        tmp2 = pivot.div(tmp_df)
        tmp2.drop(columns=['sum'], inplace=True)
        pivot = tmp2
    st.dataframe(pivot)







