import pandas as pd

import streamlit as st
from database.source_db import deaful_set
from database.dowload_data import download_first_data, download_second_data, download_dash_address_data
from functions.pivot_table import pivot_table_w_subtotals
from functions.plot_cam_adr_dash import pivot_for_dash
from datetime import datetime as date

#podstawowe ustawienia strony z raportami
st.set_page_config(page_title="Moduł raportowania dla firmy FSAPS",
                   page_icon=':bar_chart:',
                   layout='wide')

# pobieram dane z bazy dabych w zaleznosci od lokalizacji
mailings, con = deaful_set('local')

with st.sidebar:
    year_range_slider = st.slider('Proszę wybrać lata', min_value=2008, max_value=date.now().year,
                                  value=[date.now().year - 4, date.now().year])
    st.write('Działy:')
    st.button('Malingi Adresowe')
    st.button('Malingi Bezadresowe')
    st.button('Korelacje')

year_from = year_range_slider[0]
year_to = year_range_slider[1]

data = download_dash_address_data(con)
data_to_show = data.loc[(data['grupa_akcji_3'] >=year_from) & (data['grupa_akcji_3'] <=year_to)]

a1, a2 = st.columns((10,1))
cam_adr_plot = pivot_for_dash(data_to_show)
a1.bokeh_chart(cam_adr_plot)
b1, b2 = st.columns((4.5,5.5))
b1.dataframe(data_to_show)
