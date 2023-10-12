import pandas as pd
import streamlit as st

import streamlit_functions.nonadr_action_dash.objects_for_nonadr_dash.tabs_for_nonma_dash as tabs_ma
from functions_pandas.plot_cam_adr_dash import pivot_and_chart_for_dash
from streamlit_functions.dashboard.localization_label_db import label_orientations


def non_action_main_conf(data_to_show_db, con):
    prime = st.container()
    with prime:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(['Wykres', 'Tabela przestawna', 'Kolumny do wykresu', 'Ustawienie wykresu',
                                    'Filtr danych'])
        with tab5:
            magazine = st.multiselect(options=['GOŚĆ NIEDZIELNY', 'NIEDZIELA', 'IDZIEMY', 'CUDA I ŁASKI BOŻE',
                                               'KTÓŻ JAK BÓG', 'DO RZECZY', 'SIECI', 'DOBRY TYDZIEŃ', 'CUDA I OBJAWIENIA',
                                               'LUDZIE I WIARA', 'TELETYDZIEŃ', 'PRZYJACIÓŁKA', 'TO I OWO',
                                               'ŻYCIE NA GORĄCO', 'CHWILA DLA CIEBIE', 'TELEŚWIAT', 'TV14', 'KURIER TV',
                                               'SUPER TV', 'TELEMAX', 'POLSKA PRESS'], label='Prosze wybrać gazety')
            options_kind_of_gift = pd.read_sql_query('''select distinct value from fsaps_material_parameter where utility_parameter_name_id=1''', con)

            kind_of_gift = st.multiselect(options=options_kind_of_gift['value'].tolist(), label='Proszę wybrać rodzaj giftu')
            month_db = st.slider(min_value=1, max_value=12, value=[1, 12], label='Proszę wybrać miesiąc')
            if len(magazine) >= 1:
                data_to_show_db = data_to_show_db.loc[data_to_show_db['grupa_akcji_2'].isin(magazine)]
            if len(kind_of_gift) >= 1:
                data_to_show_db = data_to_show_db.loc[data_to_show_db['rodzaj_giftu'].isin(kind_of_gift)]
            if len(month_db)>=1:
                data_to_show_db['miesiac_int'] = data_to_show_db['miesiac'].astype(int)
                data_to_show_db = data_to_show_db.loc[(data_to_show_db['miesiac_int'] >= month_db[0]) & (
                        data_to_show_db['miesiac_int'] <= month_db[1]
                )]
        with tab4:
            dictionary_options, title, sub_title = tabs_ma.char_options()
            label = label_orientations()
        with tab3:
            levels_db = st.multiselect(options=['grupa_akcji_3', 'grupa_akcji_2', 'miesiac', 'kod_akcji',
                                                'obiecywany_gift', 'rodzaj_giftu'],
                                       label='Proszę wybrać kolejność dla mailingów bezadresowych',
                                       default=['grupa_akcji_3', 'grupa_akcji_2'])
            if title != '':
                title_fin = title
                if sub_title != '':
                    title_fin = f'''{title_fin}
                    {sub_title}'''
            else:
                title_fin = ''


            cam_adr_plot_db, test_pivot_db = pivot_and_chart_for_dash(data_to_show_db, levels_db, 'nonaddress',
                                                                      'Wyniki wrzutek bezadresowych za lata ',
                                                                      'Wrzutki', dictionary_options, title_fin, label)
        with tab2:
            st.dataframe(test_pivot_db, 900, 400, use_container_width=True)

        with tab1:
            st.bokeh_chart(cam_adr_plot_db, use_container_width=True)
