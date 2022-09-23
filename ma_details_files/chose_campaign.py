import streamlit as st

def choose():
    qamp = st.multiselect(options=['MAILING Q1', 'MAILING Q2', 'MAILING Q3'], label='Proszę wybrać mailing',
                          default='MAILING Q1')
    years = st.multiselect(options=['2018', '2019', '2020'], label='Proszę wybrać rok mailingu',
                           default='2019')
    return qamp, years