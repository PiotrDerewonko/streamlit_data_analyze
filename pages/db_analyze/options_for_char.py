import os

import pandas as pd
import streamlit as st

from pages.db_analyze import checkboxs


def char_options():
    with st.container():
        st.header('Wykres utrzymania i wpłat')
        dict = {'suma_wplat': False, 'koszt_utrzymania': False, 'koszt_insertu': False,
                'profit': True, 'czy_kumulacyjnie': True}
        c1, c2, c3, c4, c5 = st.columns(5)
        list_of_objects = [['suma_wplat', True],
                           ['koszt_utrzymania', False],
                           ['koszt_insertu', False],
                           ['czy_kumulacyjnie', True],
                           ['profit', True],
                           ]

        for x in list_of_objects:
            if x[0] not in st.session_state:
                st.session_state[x[0]] = x[1]

        with c1:
            dict_sw, suma_wplat_df = checkboxs.suma_wplat()
        with c2:
            dict_ku, koszt_utrzymania = checkboxs.koszt_utrzymania()
        with c3:
            dict_ki, koszt_insertu = checkboxs.koszt_insertu()
        with c4:
            dict_profit, profit = checkboxs.profit()
        with c5:
            dict_cum, czy_kumulacyjnie = checkboxs.czy_kumulacyjnie()

        test_df = pd.DataFrame()
        test_df = pd.concat([test_df, suma_wplat_df, koszt_utrzymania, koszt_insertu, profit, czy_kumulacyjnie])
        return test_df


def list_options(con):
    with st.container():
        st.header('Wybór akcji do przeanalizowania')
        sql_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         '../.././sql_queries/4/subackion_list.sql'))
        with open(sql_file_path, 'r') as sql_file:
            sql = sql_file.read()
        data = pd.read_sql_query(sql, con)
        data_copy = data.copy()
        list_of_year = list(data['grupa_akcji_3'].drop_duplicates().sort_values())
        rok = st.multiselect(options=list_of_year, label='Proszę wybrać rok', default=[list_of_year[-1]])
        if len(rok) >= 1:
            data_copy = data_copy.loc[data_copy['grupa_akcji_3'].isin(rok)]
        miesiac = st.multiselect(options=list(data_copy['miesiac'].drop_duplicates().sort_values()),
                                 label='Proszę wybrać miesiac')
        if len(miesiac) >= 1:
            data_copy = data_copy.loc[data_copy['miesiac'].isin(miesiac)]
        newspaper = st.multiselect(options=list(data_copy['grupa_akcji_2'].drop_duplicates().sort_values()),
                                   label='Proszę wybrać gazetę')
        if len(newspaper) >= 1:
            data_copy = data_copy.loc[data_copy['grupa_akcji_2'].isin(newspaper)]

        subactions = st.multiselect(options=list(data_copy['kod_akcji'].drop_duplicates().sort_values()),
                                    label='Proszę wybrać subakcję')
        if len(subactions) >= 1:
            return subactions
        else:
            return list(data_copy['kod_akcji'].drop_duplicates().sort_values())
