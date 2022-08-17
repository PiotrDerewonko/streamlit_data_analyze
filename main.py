import pandas as pd
import plotly_express as px
import streamlit as st
from database.source_db import deaful_set
from database.dowload_data import download_first_data
from functions.pivot_table import pivot_table_w_subtotals

#podstawowe ustawienia strony z raportami
st.set_page_config(page_title="Moduł raportowania dla firmy FSAPS",
                   page_icon=':bar_chart:',
                   layout='wide')

# pobieram dane z bazy dabych w zaleznosci od lokalizacji
mailings, con = deaful_set('local')

#pobieram dane podstawowe
data = download_first_data(con)


#dodaje sidebary z mozlowoscia wyboru mailingow i lat
#todo zastanowic sie jak zrobic aby pokazywal wciecia
st.sidebar.header('Proszę wybrać rodzaj mailingu')
chose_mailing = st.sidebar.multiselect(
    "Wybierz mailing", options=mailings, default=mailings
)

st.sidebar.header('Proszę wybrać rok mailingu')
chose_year = st.sidebar.multiselect(
    "Wybierz rok", options=data['grupa_akcji_3'].unique(), default=data['grupa_akcji_3'].unique()
)
st.sidebar.header('Proszę wybrać wiersze tabeli')
chose_row_of_pivot_table = st.sidebar.multiselect(
    "Wybierz wiersze", options=['grupa_akcji_1', 'grupa_akcji_2', 'grupa_akcji_3', 'kod_akcji'], default=['grupa_akcji_3', 'grupa_akcji_2']
)
#zawezam dataframe tylko do wybranych pozycji
data_selections = data.query("grupa_akcji_2 == @chose_mailing & grupa_akcji_3==@chose_year")
pivot_table = pivot_table_w_subtotals(data_selections, ['suma_wplat', 'liczba_wplat'],chose_row_of_pivot_table,[], 'sum',
                                      0)
st.dataframe(data_selections)
st.dataframe(pivot_table)


