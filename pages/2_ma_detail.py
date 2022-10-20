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
    def create_pivot():
        data = create_pivot_table(con, refresh_data, engine, qamp, years)
        st.dataframe(data)
    test = st.button('zaladuj dane')
    if test:
        create_pivot()
    st.header('Wykresy w dniach od nadania')
    charts(qamp, con, years, refresh_data, engine)

    st.header('Struktura kosztów')
