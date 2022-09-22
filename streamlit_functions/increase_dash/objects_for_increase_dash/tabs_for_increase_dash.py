
import streamlit as st

import streamlit_functions.nonadr_action_dash.objects_for_nonadr_dash.columns_for_nonadr_dash as columns_for_nonadr_dash
from streamlit_functions.dashboard.initialization import create_dictionary_increase, create_session_state_key


def char_options():
    with st.container():
        st.caption("Prosze wybrać parametry które maja znaleść sie na wykresie")
        c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
        dictionary_options = create_dictionary_increase()
        create_session_state_key(dictionary_options)
        with c1:
            columns_for_nonadr_dash.column_sum_amount(dictionary_options)
        with c2:
            columns_for_nonadr_dash.column_count_amount(dictionary_options)
        with c3:
            columns_for_nonadr_dash.circulation(dictionary_options)
        with c4:
            columns_for_nonadr_dash.cost(dictionary_options)
        with c5:
            columns_for_nonadr_dash.roi(dictionary_options)
        with c6:
            columns_for_nonadr_dash.szlw(dictionary_options)
        with c7:
            columns_for_nonadr_dash.szp(dictionary_options)
    st.markdown(dictionary_options)
    return dictionary_options