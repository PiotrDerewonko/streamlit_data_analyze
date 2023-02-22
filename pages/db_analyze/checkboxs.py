import pandas as pd
import streamlit as st

from streamlit_functions.dashboard.create_df_for_pivot import create_df


def suma_wplat():
    dict = {}
    suma_wplat = st.checkbox(label='Suma wpłat', on_change=create_df(dict, "suma_wplat",
                                                                    st.session_state.suma_wplat),
                     key="suma_wplat")
    if suma_wplat == True:
        test_dict = {'Nazwa parametru': ['suma_wplat'], 'Opcje': [suma_wplat]}
        dataframe = pd.DataFrame(data=test_dict)
    else:
        test_dict = {}
        dataframe = pd.DataFrame(data=test_dict)
    return test_dict, dataframe

def koszt_utrzymania():
    dict = {}
    suma_wplat = st.checkbox(label='Koszt utrzymania', on_change=create_df(dict, "koszt_utrzymania",
                                                                    st.session_state.koszt_utrzymania),
                     key="koszt_utrzymania")
    if suma_wplat == True:
        test_dict = {'Nazwa parametru': ['koszt_utrzymania'], 'Opcje': [suma_wplat]}
        dataframe = pd.DataFrame(data=test_dict)
    else:
        test_dict = {}
        dataframe = pd.DataFrame(data=test_dict)
    return test_dict, dataframe

def koszt_insertu():
    dict = {}
    suma_wplat = st.checkbox(label='Koszt insertu dla nowych', on_change=create_df(dict, "koszt_insertu",
                                                                    st.session_state.koszt_insertu),
                     key="koszt_insertu")
    if suma_wplat == True:
        test_dict = {'Nazwa parametru': ['koszt_insertu'], 'Opcje': [suma_wplat]}
        dataframe = pd.DataFrame(data=test_dict)
    else:
        test_dict = {}
        dataframe = pd.DataFrame(data=test_dict)
    return test_dict, dataframe

def profit():
    dict = {}
    suma_wplat = st.checkbox(label='Profit', on_change=create_df(dict, "profit",
                                                                    st.session_state.profit),
                     key="profit")
    if suma_wplat == True:
        test_dict = {'Nazwa parametru': ['profit'], 'Opcje': [suma_wplat]}
        dataframe = pd.DataFrame(data=test_dict)
    else:
        test_dict = {}
        dataframe = pd.DataFrame(data=test_dict)
    return test_dict, dataframe

def czy_kumulacyjnie():
    dict = {}
    suma_wplat = st.checkbox(label='Czy dane kumulacyjne', on_change=create_df(dict, "czy_kumulacyjnie",
                                                                    st.session_state.czy_kumulacyjnie),
                     key="czy_kumulacyjnie")
    if suma_wplat == True:
        test_dict = {'Nazwa parametru': ['czy_kumulacyjnie'], 'Opcje': [suma_wplat]}
        dataframe = pd.DataFrame(data=test_dict)
    else:
        test_dict = {}
        dataframe = pd.DataFrame(data=test_dict)
    return test_dict, dataframe