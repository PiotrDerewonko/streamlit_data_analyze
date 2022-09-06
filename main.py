import pandas as pd

import streamlit as st
from database.source_db import deaful_set
from database.dowload_data import download_first_data, download_second_data, download_dash_address_data
from functions.pivot_table import pivot_table_w_subtotals
from functions.plot_cam_adr_dash import pivot_and_chart_for_dash
from datetime import datetime as date
import sys
#podstawowe ustawienia strony z raportami
st.set_page_config(page_title="Moduł raportowania dla firmy FSAPS",
                   page_icon=':bar_chart:',
                   layout='wide')

try:
    sorce_main = sys.argv[1]
except:
    sorce_main = 'lwowska'
mailings, con, engine = deaful_set(f'{sorce_main}')
try:
    refresh_data = sys.argv[2]
except:
    refresh_data = False

with st.sidebar:
    year_range_slider = st.slider('Proszę wybrać lata', min_value=2008, max_value=date.now().year,
                                  value=[date.now().year - 4, date.now().year])
    st.write('Działy:')
    st.button('Malingi Adresowe')
    st.button('Malingi Bezadresowe')
    st.button('Korelacje')

year_from = year_range_slider[0]
year_to = year_range_slider[1]

data = download_dash_address_data(con, refresh_data, engine)
data_to_show = data.loc[(data['grupa_akcji_3'] >=year_from) & (data['grupa_akcji_3'] <=year_to)]

# tworze pierwsza 3 zakladki dal mailnigu adresowego
tab1, tab2, tab3 = st.tabs(['Wykres', 'Tabela przestawna', 'Sortowanie/Zmiany wykresu'])
# todo dorobic tutaj mozliwosci zmiany sortowania oraz kolejnsoci grupowania
with tab3:
    levels = st.multiselect(options=['grupa_akcji_3', 'grupa_akcji_2'], label='Proszę wybrać kolejność',
                            default=['grupa_akcji_3', 'grupa_akcji_2'])
    cam_adr_plot, test_pivot = pivot_and_chart_for_dash(data_to_show, levels)
with tab1:
    st.bokeh_chart(cam_adr_plot)
with tab2:
    st.dataframe(test_pivot)
