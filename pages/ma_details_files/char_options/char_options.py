import streamlit as st
from dotenv import dotenv_values

def char_options():
    sorce_main = dotenv_values('.env')
    sorce_main = list(sorce_main.values())[0]
    refresh_data = 'False'
    with st.container():
        st.subheader("Wartośc bezwzgledne")
        sc = st.checkbox('Suma wpłat', value=True)
        st.subheader("Współczynniki")
