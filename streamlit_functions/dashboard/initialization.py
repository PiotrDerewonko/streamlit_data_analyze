import streamlit as st
def create_dictionary_adr():
    return {'sw': True, 'sw_axis': 'Oś główna', 'sw_char': 'Wykres Słupkowy',
            'kc': True, 'kc_axis': 'Oś główna', 'kc_char': 'Wykres Słupkowy',
                          'lw': True, 'lw_axis': 'Oś pomocnicza', 'lw_char': 'Wykres liniowy',
                          'nc': True, 'nc_axis': 'Oś pomocnicza', 'nc_char': 'Wykres liniowy',
                          'roi': False, 'roi_axis': 'Oś główna', 'roi_char': 'Wykres liniowy',
                          'szlw': False, 'szlw_axis': 'Oś główna', 'szlw_char': 'Wykres liniowy',
                          }

def create_dictionary_nonadr():
    return {'sw_db': True, 'sw_axis_db': 'Oś główna', 'sw_char_db': 'Wykres Słupkowy',
            'kc_db': True, 'kc_axis_db': 'Oś główna', 'kc_char_db': 'Wykres Słupkowy',
                          'lw_db': True, 'lw_axis_db': 'Oś pomocnicza', 'lw_char_db': 'Wykres liniowy',
                          'nc_db': True, 'nc_axis_db': 'Oś pomocnicza', 'nc_char_db': 'Wykres liniowy',
                          'roi_db': False, 'roi_axis_db': 'Oś główna', 'roi_char_db': 'Wykres liniowy',
                          'szlw_db': False, 'szlw_axis_db': 'Oś główna', 'szlw_char_db': 'Wykres liniowy',
                          }
def create_session_state_key(data):
    for x, y in data.items():
        if x not in st.session_state:
            st.session_state[x] = y

