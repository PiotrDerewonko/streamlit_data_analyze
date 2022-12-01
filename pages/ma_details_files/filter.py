import streamlit as st
from pages.ma_details_files.data_about_people_and_campaign_pay import distinct_options
import streamlit as st

from pages.ma_details_files.data_about_people_and_campaign_pay import distinct_options


def filtr_options(con):
    refresh_data = False
    filter_value = distinct_options(refresh_data)
    list = filter_value.columns.to_list()
    list[0] = ''
    c1, c2, c3, c4 = st.columns(4)
    list_values_1 = [' ']
    list_values_2 = [' ']
    list_values_3 = [' ']
    list_values_4 = [' ']
    list_of_objects = ['f1', 'f2', 'f3', 'f4']
    for x in list_of_objects:
        if x not in st.session_state:
            st.session_state[x] = ' '
    def change_options_1(value):
        tmp = filter_value[value]
        tmp.dropna(inplace=True)
        for z, row in tmp.iteritems():
            list_values_1.append(row)
    def change_options_2(value):
        tmp = filter_value[value]
        tmp.dropna(inplace=True)
        for z, row in tmp.iteritems():
            list_values_2.append(row)
    def change_options_3(value):
        tmp = filter_value[value]
        tmp.dropna(inplace=True)
        for z, row in tmp.iteritems():
            list_values_3.append(row)
    def change_options_4(value):
        tmp = filter_value[value]
        tmp.dropna(inplace=True)
        for z, row in tmp.iteritems():
            list_values_4.append(row)
    with c1:
        st.selectbox(label="Pierwszy filtr", options=list, on_change=change_options_1(st.session_state.f1), key='f1')
        st.multiselect(label='Wartosc filtru 1', options=list_values_1)
    with c2:
        st.selectbox(label="Drugi filtr", options=list, on_change=change_options_2(st.session_state.f2), key='f2')
        st.multiselect(label='Wartosc filtru 2', options=list_values_2)
    with c3:
        st.selectbox(label="Trzeci filtr", options=list, on_change=change_options_3(st.session_state.f3), key='f3')
        st.multiselect(label='Wartosc filtru 3', options=list_values_3)
    with c4:
        st.selectbox(label="Czwarty filtr", options=list, on_change=change_options_4(st.session_state.f4), key='f4')
        st.multiselect(label='Wartosc filtru 4', options=list_values_4)