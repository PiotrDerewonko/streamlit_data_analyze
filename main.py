import pandas as pd

import streamlit as st
from database.source_db import deaful_set
from database.dowload_data import download_first_data, download_second_data, download_dash_address_data, download_increase_data
from functions.pivot_table import pivot_table_w_subtotals
from functions.plot_cam_adr_dash import pivot_and_chart_for_dash
from datetime import datetime as date
from streamlit_functions.main_action_conf import a
import sys
#podstawowe ustawienia strony z raportami
st.set_page_config(page_title="Moduł raportowania dla firmy FSAPS",
                   page_icon=':bar_chart:',
                   layout='wide')
print(sys.argv)
try:
    sorce_main = sys.argv[3]
except:
    sorce_main = 'local'
mailings, con, engine = deaful_set(f'{sorce_main}')
try:
    refresh_data = sys.argv[4]
except:
    refresh_data = 'False'

with st.sidebar:
    year_range_slider = st.slider('Proszę wybrać lata', min_value=2008, max_value=date.now().year,
                                  value=[date.now().year - 4, date.now().year])
    st.write('Działy:')
    st.button('Malingi Adresowe')
    st.button('Malingi Bezadresowe')
    st.button('Korelacje')

year_from = year_range_slider[0]
year_to = year_range_slider[1]

data_ma = download_dash_address_data(con, refresh_data, engine, 'address')
data_to_show_ma = data_ma.loc[(data_ma['grupa_akcji_3'] >= year_from) & (data_ma['grupa_akcji_3'] <= year_to)]
data_db = download_dash_address_data(con, refresh_data, engine, 'non address')
data_to_show_db = data_db.loc[(data_db['grupa_akcji_3'] >= year_from) & (data_db['grupa_akcji_3'] <= year_to)]
data_increase = download_increase_data(con, refresh_data, engine)
data_to_show_increase = data_increase.loc[(data_increase['rok_dodania'] >= year_from) & (data_increase['rok_dodania'] <= year_to)]
# tworze pierwsza 3 zakladki dal mailnigu adresowego
st.header('Dane z głównych mailingów adresowych')

with st.container():
    a(data_to_show_ma)

    st.header('Dane z głównych wrzutek bezadresowych')
    tab4, tab5, tab6 = st.tabs(['Wykres', 'Tabela przestwna', 'Kolumny do wykresu'])
    with tab6:
        levels_db = st.multiselect(options=['grupa_akcji_3', 'grupa_akcji_2', 'miesiac'], label='Proszę wybrać kolejność dla mailingów bezadresowych',
                                default=['grupa_akcji_3', 'grupa_akcji_2'])
        cam_adr_plot_db, test_pivot_db = pivot_and_chart_for_dash(data_to_show_db, levels_db, 'nonaddress',
                                                                  'Wyniki wrzutek bezadresowych za lata ',
                                                                  'Wrzutki', 'Suma wpłat/Koszt',
                                                                  'Nakład/Liczba wpłat', {})
    with tab4:
        st.bokeh_chart(cam_adr_plot_db)
    with tab5:
        st.dataframe(test_pivot_db, 900, 400)
    st.header('Dane dotyczące przyrostu korespondentów')
    tab7, tab8, tab9 = st.tabs(['Wykres', 'Tabela przestwna', 'Kolumny do wykresu'])
    with tab9:
        levels_increase = st.multiselect(options=['rok_dodania', 'grupa_akcji_2', 'miesiac_dodania'],
                                         label='Prosze wybrac kolejnosc kolumn dla danych z przyrostu',
                                         default=['rok_dodania'])
        cam_inc_plot, test_pivot_inc = pivot_and_chart_for_dash(data_to_show_increase, levels_increase, 'increase',
                                                                'Wyniki pozyskania korespondentów za lata ',
                                                                'Pozyskanie', 'Ilość pozyskanych', '', {})

    with tab7:
        st.bokeh_chart(cam_inc_plot)
    with tab8:
        st.dataframe(test_pivot_inc)
