import os
from typing import List

import pandas as pd
import streamlit as st


def column_options(con):
    list_options = distinct_columns()

    final_option_list = ['']
    if 'text_key' not in st.session_state:
        st.session_state.text_key = ''
    if 'text_key_1' not in st.session_state:
        st.session_state.text_key_1 = ''
    if 'test_list' not in st.session_state:
        st.session_state.test_list = ''
    final_option_list.append(st.session_state.test_list)

    # todo przerobic ten kod na docelowy
    def test():
        a = st.session_state.text_key
        for ii in range(0, len(a)):
            final_option_list.append(a[ii])

    def test_1():
        a = st.session_state.text_key_1
        for ii in range(0, len(a)):
            final_option_list.append(a[ii])

    columns_options = st.multiselect(options=list_options, default=['grupa_akcji_2_wysylki', 'grupa_akcji_3_wysylki'],
                                     label='Prosze wybrac gift')
    corr_method = st.selectbox(options=['spearman', 'pearson'], label='Metoda korelacji')

    return columns_options, corr_method


def distinct_columns() -> List:
    """Funkcja zwraca liste nazwy kolumn plikow people i people_camp. Lista ta jest wykorzystywana pozniej do
    wybory ktore dane maja byc prezentowane na wykresie/w tabeli"""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_file/people.csv'))
    tmp_peaople = pd.read_csv(csv_path, index_col='Unnamed: 0', nrows=1)
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_file/people_camp.csv'))
    tmp_campaign = pd.read_csv(csv_path, index_col='Unnamed: 0', nrows=1)
    tmp_all = pd.concat([tmp_peaople, tmp_campaign])
    tmp_all = tmp_all.drop(columns=['id_korespondenta'])
    list_options = tmp_all.columns.to_list()
    list_options = sorted(list_options)
    return list_options
