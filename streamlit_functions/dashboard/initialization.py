import streamlit as st
def create_dictionary():
    return  {'sw': True, 'os_sw': 'prime', 'char_sm': 'bar',
                          'lw': True, 'os_lw': 'prime', 'char_lw': 'bar',
                          'nc': True, 'os_nc': 'second', 'char_nc': 'line',
                          'kc': True, 'os_kc': 'second', 'char_kc': 'line',
                          'roi': False, 'os_roi': 'prime', 'char_roi': 'bar',
                          'szlw': False, 'os_szlw': 'prime', 'char_szlw': 'bar',
                          }
def create_session_state_key():
    if 'sw' not in st.session_state:
        st.session_state['sw'] = True
    if 'lw' not in st.session_state:
        st.session_state['lw'] = True
    if 'nc' not in st.session_state:
        st.session_state['nc'] = True
    if 'kc' not in st.session_state:
        st.session_state['kc'] = True
    if 'roi' not in st.session_state:
        st.session_state['roi'] = False
    if 'szlw' not in st.session_state:
        st.session_state['szlw'] = False