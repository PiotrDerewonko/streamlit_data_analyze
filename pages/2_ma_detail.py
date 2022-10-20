import pandas as pd
import streamlit as st

from database.source_db import deaful_set
from pages.ma_details_files.chars_for_days import charts
from pages.ma_details_files.chose_campaign import choose
from pages.ma_details_files.pivot_table_for_ma import create_pivot_table

sorce_main = 'lwowska'
mailings, con, engine = deaful_set(f'{sorce_main}')
refresh_data = 'False'

st.header('Analiza głównych mailingów adresowych ')
with st.container():
    qamp, years = choose()
    st.header('Wersje z wybranych mailingów ')
    tab1, tab2 = st.tabs(['Tabela przestawna', 'Kolejność kolumn'])
    with tab2:
        sql = 'select * from raporty.people_data limit 1'
        tmp = pd.read_sql_query(sql, con)
        list_options = tmp.columns.to_list()
        list_options.append('grupa_akcji_2_wysylki')
        list_options.append('grupa_akcji_3_wysylki')
        list_options.append('kod_akcji_wysylki')
        columns_options = st.multiselect(options=list_options, default=['grupa_akcji_2_wysylki', 'grupa_akcji_3_wysylki'],
                                         label='Prosze wybrac kolumny')
        def create_pivot():
            data = create_pivot_table(con, refresh_data, engine, qamp, years, columns_options)
            st.dataframe(data)
        test = st.button('zaladuj dane')
    with tab1:
        if test:
            create_pivot()
    st.header('Wykresy w dniach od nadania')
    charts(qamp, con, years, refresh_data, engine)

    st.header('Struktura kosztów')
