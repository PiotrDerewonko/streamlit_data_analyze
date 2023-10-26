import streamlit as st
def create_dictionary_adr():
    return {
            'kc': True, 'kc_axis': 'Oś główna', 'kc_char': 'Wykres Słupkowy',
        'sw': True, 'sw_axis': 'Oś główna', 'sw_char': 'Wykres Słupkowy',
                          'lw': True, 'lw_axis': 'Oś pomocnicza', 'lw_char': 'Wykres liniowy',
                          'nc': True, 'nc_axis': 'Oś pomocnicza', 'nc_char': 'Wykres liniowy',
                          'roi': False, 'roi_axis': 'Oś główna', 'roi_char': 'Wykres liniowy',
                          'szlw': False, 'szlw_axis': 'Oś główna', 'szlw_char': 'Wykres liniowy',
                          }

def create_dictionary_nonadr():
    return {
            'kc_db': True, 'kc_axis_db': 'Oś główna', 'kc_char_db': 'Wykres Słupkowy',
        'sw_db': True, 'sw_axis_db': 'Oś główna', 'sw_char_db': 'Wykres Słupkowy',
                          'lw_db': True, 'lw_axis_db': 'Oś pomocnicza', 'lw_char_db': 'Wykres liniowy',
                          'nc_db': True, 'nc_axis_db': 'Oś pomocnicza', 'nc_char_db': 'Wykres liniowy',
                          'roi_db': False, 'roi_axis_db': 'Oś główna', 'roi_char_db': 'Wykres liniowy',
                          'szlw_db': False, 'szlw_axis_db': 'Oś główna', 'szlw_char_db': 'Wykres liniowy',
                            'szp_db': False, 'szp_axis_db': 'Oś główna', 'szp_char_db': 'Wykres liniowy',
                            'swt_db': False, 'swt_axis_db': 'Oś główna', 'swt_char_db': 'Wykres Słupkowy',
            'kct_db': False, 'kct_axis_db': 'Oś główna', 'kct_char_db': 'Wykres Słupkowy',
            'poz_db': False, 'poz_axis_db': 'Oś główna', 'poz_char_db': 'Wykres Słupkowy',
            'kcin_db': False, 'kcin_axis_db': 'Oś główna', 'kcin_char_db': 'Wykres Słupkowy',
            'un_db': False, 'un_axis_db': 'Oś główna', 'un_char_db': 'Wykres Słupkowy',
            'swn_db': False, 'swn_axis_db': 'Oś główna', 'swn_char_db': 'Wykres Słupkowy',
            'udzial_aktywnych_nowych_db': False, 'udzial_aktywnych_nowych_db_axic': 'Oś główna', 'udzial_aktywnych_nowych_db_char': 'Wykres Słupkowy',
                          }

def create_dictionary_increase():
    return {'sw_db': True, 'sw_axis_db': 'Oś główna', 'sw_char_db': 'Wykres Słupkowy',
            'kc_db': True, 'kc_axis_db': 'Oś główna', 'kc_char_db': 'Wykres Słupkowy',
                          'lw_db': True, 'lw_axis_db': 'Oś pomocnicza', 'lw_char_db': 'Wykres liniowy',
                          'nc_db': True, 'nc_axis_db': 'Oś pomocnicza', 'nc_char_db': 'Wykres liniowy',
                          'roi_db': False, 'roi_axis_db': 'Oś główna', 'roi_char_db': 'Wykres liniowy',
                          'szlw_db': False, 'szlw_axis_db': 'Oś główna', 'szlw_char_db': 'Wykres liniowy',
                            'szp_db': False, 'szp_axis_db': 'Oś główna', 'szp_char_db': 'Wykres liniowy',
                          }
def create_session_state_key(data):
    for x, y in data.items():
        if x not in st.session_state:
            st.session_state[x] = y

