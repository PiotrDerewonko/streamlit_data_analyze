import streamlit as st

from database.source_db import deaful_set
from pages.ma_details_files.chars_for_days import charts
from pages.ma_details_files.chose_campaign import choose

sorce_main = 'local'
st.header('Analiza głównych mailingów adresowych ')
mailings, con, engine = deaful_set(f'{sorce_main}')
refresh_data = 'False'
with st.container():
    qamp, years = choose()
    st.header('Wersje z wybranych mailingów ')

    st.header('Wykresy w dniach od nadania')
    charts(qamp, con, years, refresh_data, engine)

    st.header('Struktura kosztów')
