import pandas as pd
import streamlit as st

from streamlit_functions.dashboard.create_df_for_pivot import create_df


def options_col1_suma_wplat(axis_1, char_1):
    dict = {}
    checkbox = st.checkbox('Suma wpłat', value=False, on_change=create_df(dict, "suma_wplat",
                                                                    st.session_state.suma_wplat),
                     key="suma_wplat")
    select_axis = st.selectbox('Oś dla sumy wpłat', axis_1, on_change=create_df(dict, "swax", st.session_state.swax),
                        key="swax")
    select_char = st.selectbox('Rodzaj wykresu dla Sumy wpłat', char_1, on_change=create_df(dict, "swchar",
                                                                                       st.session_state.swchar),
                          key="swchar")

    if checkbox == True:
        test_dict = {'Nazwa parametru': ['suma_wplat'], 'oś': [f'{select_axis}'],
                     'Opcje': [select_char]}
        dataframe = pd.DataFrame(data=test_dict)
    else:
        test_dict = {}
    return test_dict, dataframe

def options_col1_liczba_wplat(axis_1, char_1):
    dict = {}
    checkbox = st.checkbox('Liczba wpłat', value=False, on_change=create_df(dict, "liczba_wplat",
                                                                    st.session_state.liczba_wplat),
                     key="liczba_wplat")
    select_axis = st.selectbox('Oś dla liczby wpłat', axis_1, on_change=create_df(dict, "lwax", st.session_state.lwax),
                        key="lwax")
    select_char = st.selectbox('Rodzaj wykresu dla Sumy wpłat', char_1, on_change=create_df(dict, "lwchar",
                                                                                       st.session_state.lwchar),
                          key="lwchar")

    if checkbox == True:
        test_dict = {'Nazwa parametru': ['liczba_wplat'], 'oś': [f'{select_axis}'],
                     'Opcje': [select_char]}
        dataframe = pd.DataFrame(data=test_dict)
    else:
        test_dict = {}
    return test_dict, dataframe

def options_col1_naklad(axis_1, char_1):
    dict = {}
    checkbox = st.checkbox('Nakład', value=False, on_change=create_df(dict, "naklad",
                                                                    st.session_state.naklad),
                     key="naklad")
    select_axis = st.selectbox('Oś dla nakladu', axis_1, on_change=create_df(dict, "ncax", st.session_state.ncax),
                        key="ncax")
    select_char = st.selectbox('Rodzaj wykresu dla Sumy wpłat', char_1, on_change=create_df(dict, "ncchar",
                                                                                       st.session_state.ncchar),
                          key="ncchar")

    if checkbox == True:
        test_dict = {'Nazwa parametru': ['naklad'], 'oś': [f'{select_axis}'],
                     'Opcje': [select_char]}
        dataframe = pd.DataFrame(data=test_dict)
    else:
        test_dict = {}
    return test_dict, dataframe

def options_col1_koszt(axis_1, char_1):
    dict = {}
    checkbox = st.checkbox('Kosztu', value=False, on_change=create_df(dict, "koszt",
                                                                    st.session_state.koszt),
                     key="koszt")
    select_axis = st.selectbox('Oś dla kosztu', axis_1, on_change=create_df(dict, "kcax", st.session_state.kcax),
                        key="kcax")
    select_char = st.selectbox('Rodzaj wykresu dla kosztu', char_1, on_change=create_df(dict, "kcchar",
                                                                                       st.session_state.kcchar),
                          key="kcchar")

    if checkbox == True:
        test_dict = {'Nazwa parametru': ['koszt'], 'oś': [f'{select_axis}'],
                     'Opcje': [select_char]}
        dataframe = pd.DataFrame(data=test_dict)
    else:
        test_dict = {}
    return test_dict, dataframe