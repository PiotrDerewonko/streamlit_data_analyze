import streamlit as st

from database.dowload_data import download_dash_address_data
from ma_details_files.chars_for_days import charts
from ma_details_files.chose_campaign import choose
from main import con, refresh_data, engine

st.header('Analiza głównych mailingów adresowych')

with st.container():
    qamp, years = choose()
    data_ma = download_dash_address_data(con, refresh_data, engine, 'address')
    data_ma_to_show = data_ma[data_ma['grupa_akcji_2'].isin(qamp)]
    data_ma_to_show = data_ma_to_show[data_ma['grupa_akcji_3'].isin(years)]
    #main_action_config(data_ma_to_show, False)
    st.header('Wersje z wybranych mailingów')

    st.header('Wykresy w dniach od nadania')
    charts(data_ma_to_show, qamp, con, years)

    st.header('Struktura kosztów')
