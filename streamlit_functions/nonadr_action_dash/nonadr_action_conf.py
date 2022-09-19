import streamlit as st
import streamlit_functions.nonadr_action_dash.objects_for_nonadr_dash.tabs_for_nonma_dash as tabs_ma
from functions_pandas.plot_cam_adr_dash import pivot_and_chart_for_dash

def non_action_main_conf(data_to_show_db):
    prime = st.container()
    with prime:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(['Wykres', 'Tabela przestawna', 'Kolumny do wykresu', 'Ustawienie wykresu',
                                    'Filtr danych'])
        with tab4:
            dictionary_options = tabs_ma.char_options()
        with tab3:
            levels_db = st.multiselect(options=['grupa_akcji_3', 'grupa_akcji_2', 'miesiac'],
                                       label='Proszę wybrać kolejność dla mailingów bezadresowych',
                                       default=['grupa_akcji_3', 'grupa_akcji_2'])
            cam_adr_plot_db, test_pivot_db = pivot_and_chart_for_dash(data_to_show_db, levels_db, 'nonaddress',
                                                                      'Wyniki wrzutek bezadresowych za lata ',
                                                                      'Wrzutki', 'Suma wpłat/Koszt',
                                                                      'Nakład/Liczba wpłat', {})
        with tab2:
            st.bokeh_chart(cam_adr_plot_db)
        with tab1:
            st.dataframe(test_pivot_db, 900, 400)