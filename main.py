from datetime import datetime as date

import streamlit as st
from dotenv import dotenv_values

from database.dowload_data import download_dash_address_data, download_increase_data
from database.source_db import deaful_set
from functions_pandas.plot_cam_adr_dash import pivot_and_chart_for_dash
from streamlit_functions.adr_action_dash.adr_action_conf import main_action_config
from streamlit_functions.nonadr_action_dash.nonadr_action_conf import non_action_main_conf

#podstawowe ustawienia strony z raportami
st.set_page_config(page_title="Moduł raportowania dla firmy FSAPS",
                   page_icon=':bar_chart:',
                   layout='wide')

sorce_main = dotenv_values('.env')
sorce_main = list(sorce_main.values())[0]
mailings, con, engine = deaful_set(f'{sorce_main}')
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


with st.container():
    st.header('Dane z głównych mailingów adresowych ')

    # odwoluje sie do funkcji ktore generuje caly modul odpowiedzialny za mailingi adresowe
    main_action_config(data_to_show_ma, True)

    st.header('Dane z głównych wrzutek bezadresowych')
    #todo wykres z przychodu i do 100 % porzychod
    non_action_main_conf(data_to_show_db, con)
    st.header('Dane dotyczące przyrostu korespondentów')
    tab7, tab8, tab9, tab10 = st.tabs(['Wykres', 'Tabela przestawna', 'Kolumny do wykresu', 'Filtr'])
    with tab10:
        month = st.slider(min_value=1, max_value=12, value=[1, 12], label='Proszę wybrać miesiące')
    with tab9:
        data_to_show_increase['miesiac_int'] = data_to_show_increase['miesiac_dodania'].astype(int)
        data_to_show_increase['rok_dodania'] = data_to_show_increase['rok_dodania'].astype(int)
        data_to_show_increase['miesiac_dodania'] = data_to_show_increase['miesiac_dodania'].astype(str)
        data_to_show_increase = data_to_show_increase.loc[(data_to_show_increase['miesiac_int']>=month[0]) & (
                data_to_show_increase['miesiac_int'] <= month[1]
        )]
        data_to_show_increase['miesiac_dodania'].loc[data_to_show_increase['miesiac_int'] < 10] = \
            '0' + data_to_show_increase['miesiac_dodania']
        index = st.multiselect(options=['rok_dodania', 'grupa_akcji_1', 'grupa_akcji_2', 'miesiac_dodania', 'kod_akcji',
                                        'mailingi', 'wpłata'],
                                         label='Prosze wybrac dane do indeksu',
                                         default=['miesiac_dodania'])
        columns_label = st.multiselect(options=['rok_dodania', 'grupa_akcji_1','grupa_akcji_2', 'miesiac_dodania',
                                                'kod_akcji', 'mailingi', 'wpłata'],
                                         label='Prosze wybrac dane do kolumn',
                                         default=['rok_dodania'])
        cam_inc_plot, test_pivot_inc = pivot_and_chart_for_dash(data_to_show_increase, index, 'increase',
                                                                'Wyniki pozyskania korespondentów za lata ',
                                                                 '',{}, columns_label)

    with tab7:
        st.bokeh_chart(cam_inc_plot, use_container_width=True)
    with tab8:
        test_pivot_inc.reset_index(inplace=True)
        test_pivot_inc.loc[len(test_pivot_inc.index)] = 'Suma'
        test_pivot_inc.set_index(index, inplace=True)
        test_pivot_inc.iloc[len(test_pivot_inc)-1] = 0
        for i in test_pivot_inc.columns:
            tmp = sum(test_pivot_inc[f'{i}'])
            test_pivot_inc[f'{i}'].iloc[len(test_pivot_inc)-1] = sum(test_pivot_inc[f'{i}'])
        st.dataframe(test_pivot_inc)
