import pandas as pd
import streamlit as st
from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.ma_details_files.chars_for_days import charts
from pages.ma_details_files.chose_campaign import choose
from pages.ma_details_files.pivot_table_for_ma import create_pivot_table

sorce_main = dotenv_values('.env')
sorce_main = list(sorce_main.values())[0]
mailings, con, engine = deaful_set(f'{sorce_main}')
refresh_data = 'False'

st.header('Analiza głównych mailingów adresowych ')
with st.container():
    qamp, years = choose()
    st.header('Wersje z wybranych mailingów ')
    tab1, tab2, tab3, tab4, tab5 = st.tabs(['Wykres', 'Tabela przestawna', 'korelacje', 'Kolejność kolumn', 'Opcje wykresu'])
    with tab4:
        sql = 'select * from raporty.people_data limit 1'
        tmp = pd.read_sql_query(sql, con)
        list_options = tmp.columns.to_list()
        list_options = sorted(list_options)
        list_options.append('grupa_akcji_2_wysylki')
        list_options.append('grupa_akcji_3_wysylki')
        list_options.append('kod_akcji_wysylki')
        test1 = ['']
        if 'text_key' not in st.session_state:
            st.session_state.text_key = ''
        if 'text_key_1' not in st.session_state:
            st.session_state.text_key_1 = ''
        if 'test_list' not in st.session_state:
            st.session_state.test_list = ''
        test1.append(st.session_state.test_list)

        def test():
            a= st.session_state.text_key
            for ii in range(0, len(a)):

                test1.append(a[ii])
        def test_1():
            a= st.session_state.text_key_1
            for ii in range(0, len(a)):
                test1.append(a[ii])
        columns_options = st.multiselect(options=list_options, default=['grupa_akcji_2_wysylki', 'grupa_akcji_3_wysylki'],
                                         label='Prosze wybrac gift')
        columns_options2 = st.multiselect(options=['grupa_akcji_22_wysylki', 'grupa_akcji_33_wysylki',''],
                                         label='Modlitwy', on_change=test(), key='text_key')
        columns_options2_1 = st.multiselect(options=['grupa_akcji_22_1_wysylki', 'grupa_akcji_33_1_wysylki',''],
                                         label='Prosze wybrac kolumny2_1', on_change=test_1(), key='text_key_1')
        columns_options3 = st.multiselect(options=test1,
                                         label='Prosze wybrac kolumny3')
        corr_method = st.selectbox(options=['pearson', 'spearman'], label='Metoda korelacji')
        def create_pivot():
            data, char = create_pivot_table(con, refresh_data, engine, qamp, years, columns_options, corr_method)
            st.dataframe(data)

            with tab3:
                st.pyplot(char)
        test = st.button('Przelicz dane')

    with tab2:
        if test:
            create_pivot()
    st.header('Wykresy w dniach od nadania')
    charts(qamp, con, years, refresh_data, engine)

    st.header('Struktura kosztów')
