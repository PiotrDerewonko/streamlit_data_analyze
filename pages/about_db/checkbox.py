import pandas as pd
import streamlit as st

from pages.about_db import creating_checkbox


def add_check_box():
    st.header('Wykres struktury bazy danych')
    dict = {'baza': True, 'ograniczenie': True, 'zwroty': True,
            'wplata': True, 'czy_do_100': False}
    c1, c2, c3, c4, c5 = st.columns(5)
    list_of_objects = [['baza', True],
                       ['ograniczenie', True],
                       ['zwroty', True],
                       ['wplata', True],
                       ['czy_do_100', False]]

    for x in list_of_objects:
        if x[0] not in st.session_state:
            st.session_state[x[0]] = x[1]
    with c1:
        dict_baza, baza_df = creating_checkbox.baza()
    with c2:
        dict_ogra, ogra_df = creating_checkbox.ograniczenie()
    with c3:
        dict_zwr, zwroty_df = creating_checkbox.zwroty()
    with c4:
        dict_wpl, wplaty_df = creating_checkbox.wplata()
    with c5:
        dict_typ, typ_df = creating_checkbox.typ()

    test_df = pd.DataFrame()
    test_df = pd.concat([test_df, baza_df, ogra_df, zwroty_df, wplaty_df, typ_df])
    return test_df