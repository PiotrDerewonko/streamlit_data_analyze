import streamlit as st

from ma_details_files.chars_for_days import charts
from ma_details_files.chose_campaign import choose
from main import con, refresh_data, engine

st.header('Analiza głównych mailingów adresowych')

with st.container():
    qamp, years = choose()
    st.header('Wersje z wybranych mailingów')

    st.header('Wykresy w dniach od nadania')
    charts(qamp, con, years, refresh_data, engine)

    st.header('Struktura kosztów')
