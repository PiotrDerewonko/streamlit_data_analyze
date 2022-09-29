import sys
from datetime import datetime as date

import streamlit as st

from database.dowload_data import download_dash_address_data, download_increase_data
from database.source_db import deaful_set
from functions_pandas.plot_cam_adr_dash import pivot_and_chart_for_dash
from streamlit_functions.adr_action_dash.adr_action_conf import main_action_config
from streamlit_functions.nonadr_action_dash.nonadr_action_conf import non_action_main_conf

#podstawowe ustawienia strony z raportami
st.set_page_config(page_title="Moduł raportowania dla firmy FSAPS",
                   page_icon=':bar_chart:',
                   layout='wide')
print(sys.argv)
#try:
#    sorce_main = sys.argv[3]
#except:
sorce_main = 'local'
mailings, con, engine = deaful_set(f'{sorce_main}')
#try:
#    refresh_data = sys.argv[4]
#except:
refresh_data = 'False'

with st.sidebar:
    year_range_slider = st.slider('Proszę wybrać lata', min_value=2008, max_value=date.now().year,
                                  value=[date.now().year - 4, date.now().year])
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
    # odwoluje sie do funkcji ktore generuje caly modul odpowiedzialny za mailingi adresowe
    main_action_config(data_to_show_ma, True)
    st.header('Dane z głównych wrzutek bezadresowych')
    non_action_main_conf(data_to_show_db)
    st.header('Dane dotyczące przyrostu korespondentów')
    tab7, tab8, tab9 = st.tabs(['Wykres', 'Tabela przestwna', 'Kolumny do wykresu'])
    with tab9:
        levels_increase = st.multiselect(options=['rok_dodania', 'grupa_akcji_2', 'miesiac_dodania', 'kod_akcji'],
                                         label='Prosze wybrac kolejnosc kolumn dla danych z przyrostu',
                                         default=['rok_dodania'])
        cam_inc_plot, test_pivot_inc = pivot_and_chart_for_dash(data_to_show_increase, levels_increase, 'increase',
                                                                'Wyniki pozyskania korespondentów za lata ',
                                                                 '', {})

    with tab7:
        st.bokeh_chart(cam_inc_plot)
    with tab8:
        st.dataframe(test_pivot_inc)
