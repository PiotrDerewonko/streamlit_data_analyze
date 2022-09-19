
import streamlit as st
from streamlit_functions.dashboard.initialization import create_dictionary, create_session_state_key
import streamlit_functions.main_action_dash.objects_for_ma_dash.columns_for_ma_dash as columns_for_ma_dash
from functions.plot_cam_adr_dash import pivot_and_chart_for_dash

def filtr_mailings():
    levels_ma_ma = st.multiselect(options=['grupa_akcji_3', 'grupa_akcji_2'],
                                  label='Proszę wybrać rodzaje mailingów',
                                  default=['grupa_akcji_3', 'grupa_akcji_2'])
    levels_ma_year = st.multiselect(options=['2022', '2021'],
                                    label='Proszę wybrać lata mailingów',
                                    default=['2022', '2021'])

def char_options():
    with st.container():
        st.caption("Prosze wybrać parametry które maja znaleść sie na wykresie")
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        dictionary_options = create_dictionary()
        create_session_state_key(dictionary_options)
        with c1:
            columns_for_ma_dash.column_sum_amount(dictionary_options)
        with c2:
            columns_for_ma_dash.column_count_amount(dictionary_options)
        with c3:
            columns_for_ma_dash.circulation(dictionary_options)
        with c4:
            columns_for_ma_dash.cost(dictionary_options)
        with c5:
            columns_for_ma_dash.roi(dictionary_options)
        with c6:
            columns_for_ma_dash.szlw(dictionary_options)
    st.markdown(dictionary_options)
    return dictionary_options

def columns_order(dictionary_options, data_to_show_ma):
    with st.container():
        levels_ma = st.multiselect(options=['grupa_akcji_3', 'grupa_akcji_2'],
                                   label='Proszę wybrać kolejność kolumn',
                                   default=['grupa_akcji_3', 'grupa_akcji_2'])
        cam_adr_plot_ma, test_pivot_ma = pivot_and_chart_for_dash(data_to_show_ma, levels_ma, 'address',
                                                                  'Wyniki mailingów adresowych za lata ',
                                                                  'Malingi', 'Suma wpłat/Koszt',
                                                                  'Nakład/Liczba wpłat', dictionary_options)
        return cam_adr_plot_ma, test_pivot_ma