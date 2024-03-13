import pandas as pd
import streamlit as st
from dotenv import dotenv_values

from database.source_db import deaful_set
from functions_pandas.plot_cam_adr_dash import pivot_and_chart_for_dash
from pages.db_analyze.generete_pivot_tables import generete_pivot_tables
from pages.db_analyze.get_data_to_db_analyze import live_people_from_db, weeks_of_db
from pages.db_analyze.options_for_char import char_options, list_options

with st.container():
    sorce_main = dotenv_values('.env')
    sorce_main = list(sorce_main.values())[0]
    refresh_data = 'False'
    mail, con, engine = deaful_set(sorce_main)

    # Wybor akcji do pokazania
    subaction_list = list_options(con)

    # dodanie check box do grupowania danych w grupy akcji
    is_grouped = st.checkbox(label='Zgrupuj kody')

    st.header('Wykres tygodniach')

    # Miejsce na tutul wykresu zycia darczynocw
    title_weeks = st.text_input('Miejsce na tytuł wykresu')

    ilosc_tygodni = st.slider('Proszę wybrać zakres tygodni', min_value=1, max_value=10,
                              value=[1, 7])
    from_ = ilosc_tygodni[0]
    to_ = ilosc_tygodni[1]

    # pobieranie i odfiltoprwanie danych
    data_second = weeks_of_db(con, refresh_data, engine)
    data_second = data_second.loc[data_second['kod_akcji'].isin(subaction_list)]
    data_second = data_second.loc[(data_second['numer_tygodnia'] >= from_) & (data_second['numer_tygodnia'] <= to_)]
    data_second['numer_tygodnia'] = data_second['numer_tygodnia'].astype(str)

    # tworzenie tabel przestawnych oraz indesku do nich
    pivot_to_weeks_final, index_values = generete_pivot_tables(subaction_list, data_second, is_grouped)

    # tworzenie wykresów dla tygodni
    char_options_df_weeks = pd.DataFrame(
        data={'Nazwa parametru': ['suma_wplat', 'pozyskano', 'koszt_insertu', 'koszt_wysylki_giftu'
                                  ],
              'oś': ['Oś główna', 'Oś pomocnicza', 'Oś główna', 'Oś główna'],
              'Opcje': ['Wykres Słupkowy', 'Wykres liniowy', 'Wykres Słupkowy Skumulowany',
                        'Wykres Słupkowy Skumulowany']}, index=[0, 1, 2, 3])
    dict_of_oriantation = {'major': 'vertical', 'group': 'vertical', 'sub_group': 'vertical'}

    char_weeks, aa = pivot_and_chart_for_dash(data_second, index_values, 'me_detail', 'test tytulu',
                                              'Tydzień', {}, pivot_to_weeks_final, char_options_df_weeks, title_weeks,
                                              dict_of_oriantation
                                              )
    st.bokeh_chart(char_weeks)
    with st.expander('Zobacz tabele z danymi'):
        st.dataframe(pivot_to_weeks_final, use_container_width=True)

    ################################################################################
    # pobieram i filtruje dane dane
    data = live_people_from_db(con, refresh_data)
    data = data.loc[data['kod_akcji'].isin(subaction_list)]
    uniq_subaction = list(data['kod_akcji'].drop_duplicates())

    # tworze tabele przestawna
    pivot = pd.pivot_table(data, index='miesiac_obecnosci_w_bazie', columns='kod_akcji',
                           values=['wplaty', 'koszt_utrzymania', 'koszt_insertu'], aggfunc='sum')
    for row in uniq_subaction:
        pivot[('profit', row)] = pivot[('wplaty', row)] - pivot[('koszt_utrzymania', row)] - pivot[
            ('koszt_insertu', row)]
    # Wybór danych na wykres zycia darczyncow
    char_options_df = char_options()

    # Miejsce na tutul wykresu zycia darczynocw
    title = st.text_input('Miejsce na tytuł wykresu', key='zycie')

    final_list_of_column_to_remove = ['wplaty', 'koszt_utrzymania', 'koszt_insertu', 'profit']
    tmp = list(char_options_df['Nazwa parametru'].loc[char_options_df['Nazwa parametru'] != 'czy_kumulacyjnie'])
    for i in tmp:
        try:
            final_list_of_column_to_remove.remove(i)
        except:
            a = ''

    for dele in final_list_of_column_to_remove:
        for row_ in uniq_subaction:
            pivot.drop((dele, row_), axis=1, inplace=True)

    if len(char_options_df.loc[char_options_df['Nazwa parametru'] == 'czy_kumulacyjnie']) == 1:
        pivot = pivot.cumsum()

    char_options_df['oś'] = 'Oś główna'
    char_options_df['Opcje'] = 'Wykres liniowy'
    # todo sprawdzic czemu to nie dziala
    char, tmp_pivot = pivot_and_chart_for_dash(data, ['data_tmp'], 'people_db', title,
                                               'Miesiąc obecnosci w bazie', {}, pivot, char_options_df, title)

    st.bokeh_chart(char)
    with st.expander('Zobacz tabele z danymixxx'):
        st.dataframe(pivot, use_container_width=True)
