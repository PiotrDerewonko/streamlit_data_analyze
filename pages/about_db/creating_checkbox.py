import pandas as pd
import streamlit as st

from streamlit_functions.dashboard.create_df_for_pivot import create_df


def baza():
    dict = {}
    suma_wplat = st.checkbox(label='Baza', on_change=create_df(dict, "baza",
                                                                    st.session_state.baza),
                     key="baza")
    test_dict = {'Nazwa parametru': ['baza'], 'Opcje': [suma_wplat]}
    dataframe = pd.DataFrame(data=test_dict)

    return test_dict, dataframe

def ograniczenie():
    dict = {}
    suma_wplat = st.checkbox(label='Ograniczenia korespondencji', on_change=create_df(dict, "ograniczenie",
                                                                    st.session_state.ograniczenie),
                     key="ograniczenie")
    test_dict = {'Nazwa parametru': ['ograniczenie'], 'Opcje': [suma_wplat]}
    dataframe = pd.DataFrame(data=test_dict)

    return test_dict, dataframe

def zwroty():
    dict = {}
    suma_wplat = st.checkbox(label='Zwroty', on_change=create_df(dict, "zwroty",
                                                                    st.session_state.zwroty),
                     key="zwroty")
    test_dict = {'Nazwa parametru': ['zwroty'], 'Opcje': [suma_wplat]}
    dataframe = pd.DataFrame(data=test_dict)
    return test_dict, dataframe

def wplata():
    dict = {}
    suma_wplat = st.checkbox(label='Wpłaty', on_change=create_df(dict, "wplata",
                                                                    st.session_state.wplata),
                     key="wplata")
    test_dict = {'Nazwa parametru': ['wplata'], 'Opcje': [suma_wplat]}
    dataframe = pd.DataFrame(data=test_dict)
    return test_dict, dataframe
