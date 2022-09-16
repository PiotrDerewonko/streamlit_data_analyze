import streamlit as st
def create_dictionary():
    return {'sw': True, 'sw_axis': 'Oś główna', 'sw_char': 'Wykres Słupkowy',
                          'lw': True, 'lw_axis': 'Oś pomocnicza', 'lw_char': 'Wykres liniowy',
                          'nc': True, 'nc_axis': 'Oś pomocnicza', 'nc_char': 'Wykres liniowy',
                          'kc': True, 'kc_axis': 'Oś główna', 'kc_char': 'Wykres Słupkowy',
                          'roi': False, 'roi_axis': 'Oś główna', 'roi_char': 'Wykres liniowy',
                          'szlw': False, 'szlw_axis': 'Oś główna', 'szlw_char': 'Wykres liniowy',
                          }
def create_session_state_key(data):
    for x, y in data.items():
        if x not in st.session_state:
            st.session_state[x] = y

