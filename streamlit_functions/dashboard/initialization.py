import streamlit as st
def create_dictionary():
    return {'sw': True, 'sw_axis': 'Oś główna', 'sw_char': 'bar',
                          'lw': True, 'lw_axis': 'Oś pomocnicza', 'lw_char': 'line',
                          'nc': True, 'nc_axis': 'Oś pomocnicza', 'nc_char': 'line',
                          'kc': True, 'kc_axis': 'Oś główna', 'kc_char': 'bar',
                          'roi': False, 'roi_axis': 'Oś główna', 'roi_char': 'bar',
                          'szlw': False, 'szlw_axis': 'Oś główna', 'szlw_char': 'bar',
                          }
def create_session_state_key(data):
    for x, y in data.items():
        if x not in st.session_state:
            st.session_state[x] = y

