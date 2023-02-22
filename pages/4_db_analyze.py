import pandas as pd
import streamlit as st
from dotenv import dotenv_values

from database.source_db import deaful_set
from functions_pandas.plot_cam_adr_dash import pivot_and_chart_for_dash
from pages.db_analyze.get_data_to_db_analyze import live_people_from_db
from pages.db_analyze.options_for_char import char_options, list_options

with st.container():
    sorce_main = dotenv_values('.env')
    sorce_main = list(sorce_main.values())[0]
    refresh_data = 'False'
    mail, con, engine = deaful_set(sorce_main)

    #Wybor akcji do pokazania
    subaction_list = list_options(con)

    #Wybór danych na wykres
    char_options_df = char_options()

    #Miejsce na tutul wykresu
    title = st.text_input('Miejsce na tytuł wykresu')

    final_list_of_column_to_remove = ['wplaty', 'koszt_utrzymania' , 'koszt_insertu', 'profit']
    tmp = list(char_options_df['Nazwa parametru'].loc[char_options_df['Nazwa parametru'] != 'czy_kumulacyjnie'])
    for i in tmp:
        try:
            final_list_of_column_to_remove.remove(i)
        except:
            a= ''

    data = live_people_from_db(con, refresh_data)
    data = data.loc[data['kod_akcji'].isin(subaction_list)]
    uniq_subaction = list(data['kod_akcji'].drop_duplicates())
    pivot = pd.pivot_table(data, index='miesiac_obecnosci_w_bazie', columns='kod_akcji',
                             values=['wplaty', 'koszt_utrzymania' , 'koszt_insertu'], aggfunc='sum')
    for row in uniq_subaction:
        pivot[('profit', row)] = pivot[('wplaty', row)] - pivot[('koszt_utrzymania', row)] - pivot[('koszt_insertu', row)]
    for dele in final_list_of_column_to_remove:
        for row_ in uniq_subaction:
            pivot.drop((dele, row_), axis=1, inplace=True)


    if len(char_options_df.loc[char_options_df['Nazwa parametru'] == 'czy_kumulacyjnie']) == 1:
        pivot = pivot.cumsum()
    st.dataframe(pivot, use_container_width=True)
    char_options_df['oś'] = 'Oś główna'
    char_options_df['Opcje'] = 'Wykres liniowy'

    char, tmp_pivot = pivot_and_chart_for_dash(data, ['data_tmp'], 'people_db', title,
                                               'Miesiąc obecnosci w bazie', {}, pivot, char_options_df, title)

    st.bokeh_chart(char)




