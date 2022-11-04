import pandas as pd
import streamlit as st

from streamlit_functions.dashboard.create_df_for_pivot import create_df


def options_col1_roi(axis_1, char_1):
    dict = {}
    checkbox = st.checkbox('ROI', value=False, on_change=create_df(dict, "ROI",
                                                                    st.session_state.ROI),
                     key="ROI")
    select_axis = st.selectbox('Oś dla ROI', axis_1, on_change=create_df(dict, "roiax", st.session_state.roiax),
                        key="roiax")
    select_char = st.selectbox('Rodzaj wykresu dla ROI', char_1, on_change=create_df(dict, "roichar",
                                                                                       st.session_state.roichar),
                          key="roichar")

    if checkbox == True:
        test_dict = {'Nazwa parametru': ['ROI'], 'oś': [f'{select_axis}'],
                     'Opcje': [select_char]}
        dataframe = pd.DataFrame(data=test_dict)
    else:
        test_dict = {}
        dataframe = pd.DataFrame(data=test_dict)
    return test_dict, dataframe

def options_col1_szlw(axis_1, char_1):
    dict = {}
    checkbox = st.checkbox('SZLW', value=False, on_change=create_df(dict, "SZLW",
                                                                    st.session_state.SZLW),
                     key="SZLW")
    select_axis = st.selectbox('Oś dla SZLW', axis_1, on_change=create_df(dict, "szlwax", st.session_state.szlwax),
                        key="szlwax")
    select_char = st.selectbox('Rodzaj wykresu dla SZLW', char_1, on_change=create_df(dict, "szlwchar",
                                                                                       st.session_state.szlwchar),
                          key="szlwchar")

    if checkbox == True:
        test_dict = {'Nazwa parametru': ['SZLW'], 'oś': [f'{select_axis}'],
                     'Opcje': [select_char]}
        dataframe = pd.DataFrame(data=test_dict)
    else:
        test_dict = {}
        dataframe = pd.DataFrame(data=test_dict)
    return test_dict, dataframe

def options_col1_1_perc(axis_1, char_1):
    dict = {}
    checkbox = st.checkbox('1 perc.', value=False, on_change=create_df(dict, "Pierwszy_percentyl",
                                                                    st.session_state.Pierwszy_percentyl),
                     key="Pierwszy_percentyl")
    select_axis = st.selectbox('Oś dla SZLW', axis_1, on_change=create_df(dict, "pier_pax", st.session_state.pier_pax),
                        key="pier_pax")
    select_char = st.selectbox('Rodzaj wykresu dla SZLW', char_1, on_change=create_df(dict, "pier_pchar",
                                                                                       st.session_state.pier_pchar),
                          key="pier_pchar")

    if checkbox == True:
        test_dict = {'Nazwa parametru': ['Pierwszy_percentyl'], 'oś': [f'{select_axis}'],
                     'Opcje': [select_char]}
        dataframe = pd.DataFrame(data=test_dict)
    else:
        test_dict = {}
        dataframe = pd.DataFrame(data=test_dict)
    return test_dict, dataframe

def options_col1_mediana(axis_1, char_1):
    dict = {}
    checkbox = st.checkbox('Mediana', value=False, on_change=create_df(dict, "mediana",
                                                                    st.session_state.mediana),
                     key="mediana")
    select_axis = st.selectbox('Oś dla mediany', axis_1, on_change=create_df(dict, "medax", st.session_state.medax),
                        key="medax")
    select_char = st.selectbox('Rodzaj wykresu dla mediany', char_1, on_change=create_df(dict, "medchar",
                                                                                       st.session_state.medchar),
                          key="medchar")

    if checkbox == True:
        test_dict = {'Nazwa parametru': ['mediana'], 'oś': [f'{select_axis}'],
                     'Opcje': [select_char]}
        dataframe = pd.DataFrame(data=test_dict)
    else:
        test_dict = {}
        dataframe = pd.DataFrame(data=test_dict)
    return test_dict, dataframe

def options_col1_3_perc(axis_1, char_1):
    dict = {}
    checkbox = st.checkbox('3 percentyl', value=False, on_change=create_df(dict, "Trzeci_percentyl",
                                                                    st.session_state.Trzeci_percentyl),
                     key="Trzeci_percentyl")
    select_axis = st.selectbox('Oś dla 3 perc.', axis_1, on_change=create_df(dict, "trzec_pax", st.session_state.trzec_pax),
                        key="trzec_pax")
    select_char = st.selectbox('Rodzaj wykresu dla 3 perc.', char_1, on_change=create_df(dict, "trzec_pchar",
                                                                                       st.session_state.trzec_pchar),
                          key="trzec_pchar")

    if checkbox == True:
        test_dict = {'Nazwa parametru': ['Trzeci_percentyl'], 'oś': [f'{select_axis}'],
                     'Opcje': [select_char]}
        dataframe = pd.DataFrame(data=test_dict)
    else:
        test_dict = {}
        dataframe = pd.DataFrame(data=test_dict)
    return test_dict, dataframe


def options_col1_std(axis_1, char_1):
    dict = {}
    checkbox = st.checkbox('Odchylenie', value=False, on_change=create_df(dict, "Odchylenie",
                                                                    st.session_state.Odchylenie),
                     key="Odchylenie")
    select_axis = st.selectbox('Oś dla STD', axis_1, on_change=create_df(dict, "stdax", st.session_state.stdax),
                        key="stdax")
    select_char = st.selectbox('Rodzaj wykresu STD', char_1, on_change=create_df(dict, "stdchar",
                                                                                       st.session_state.stdchar),
                          key="stdchar")

    if checkbox == True:
        test_dict = {'Nazwa parametru': ['Odchylenie'], 'oś': [f'{select_axis}'],
                     'Opcje': [select_char]}
        dataframe = pd.DataFrame(data=test_dict)
    else:
        test_dict = {}
        dataframe = pd.DataFrame(data=test_dict)
    return test_dict, dataframe


def options_col1_avg(axis_1, char_1):
    dict = {}
    checkbox = st.checkbox('Średnia', value=False, on_change=create_df(dict, "średnia",
                                                                    st.session_state.średnia),
                     key="średnia")
    select_axis = st.selectbox('Oś dla Średnia', axis_1, on_change=create_df(dict, "avgax", st.session_state.avgax),
                        key="avgax")
    select_char = st.selectbox('Rodzaj wykresu Średnia', char_1, on_change=create_df(dict, "avgchar",
                                                                                       st.session_state.avgchar),
                          key="avgchar")

    if checkbox == True:
        test_dict = {'Nazwa parametru': ['średnia'], 'oś': [f'{select_axis}'],
                     'Opcje': [select_char]}
        dataframe = pd.DataFrame(data=test_dict)
    else:
        test_dict = {}
        dataframe = pd.DataFrame(data=test_dict)
    return test_dict, dataframe


def options_col1_kng(axis_1, char_1):
    dict = {}
    checkbox = st.checkbox('KNG', value=False, on_change=create_df(dict, "Koszt_na_głowę",
                                                                    st.session_state.Koszt_na_głowę),
                     key="Koszt_na_głowę")
    select_axis = st.selectbox('Oś dla KNG', axis_1, on_change=create_df(dict, "kngdax", st.session_state.kngdax),
                        key="kngdax")
    select_char = st.selectbox('Rodzaj wykresu KNG', char_1, on_change=create_df(dict, "kngchar",
                                                                                       st.session_state.kngchar),
                          key="kngchar")

    if checkbox == True:
        test_dict = {'Nazwa parametru': ['Koszt_na_głowę'], 'oś': [f'{select_axis}'],
                     'Opcje': [select_char]}
        dataframe = pd.DataFrame(data=test_dict)
    else:
        test_dict = {}
        dataframe = pd.DataFrame(data=test_dict)
    return test_dict, dataframe