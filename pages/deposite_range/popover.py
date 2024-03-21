from typing import List

import pandas as pd
import streamlit as st


def add_popover() -> List:
    """Funkcja ma za zadanie dodać popovery z dodatkowymi filitrami i zwrocić listę dodatkowych filtrów do loc"""
    list_to_loc = []
    popover = st.popover('Wybierz dodatkowe filtry')
    gr_2_wpl = popover.checkbox('Filtruj po grupie akcji 2 wpłaty', False)
    gr_1_dod = popover.checkbox('Filtruj po grupie akcji 1 dodania', False)
    gr_2_dod = popover.checkbox('Filtruj po grupie akcji 2 dodania', False)
    rok_dod = popover.checkbox('Filtruj po roku dodania', False)
    przedzial_wieku = popover.checkbox('Filtruj po przedziale wiekowym', False)
    uniq_data = pd.read_csv('./pages/ma_details_files/tmp_file/column_with_options.csv')

    if gr_2_wpl:
        with st.container(border=True):
            options_gr2_wpl = uniq_data['grupa_akcji_2_wysylki'].dropna().sort_values()
            filtr_gr2_wpl = st.multiselect(options=options_gr2_wpl, label='Filtruj po mailingu')
            filtr_text_gr2_wpl = f"""(df['grupa_akcji_2_wplaty'].isin({filtr_gr2_wpl}))"""
            list_to_loc.append(filtr_text_gr2_wpl)

    if gr_1_dod:
        with st.container(border=True):
            options_gr_1_dod = uniq_data['grupa_akcji_1_dodania'].dropna().sort_values()
            filtr_gr1_dod = st.multiselect(options=options_gr_1_dod, label='Filtruj po grupie akcji 1 dodania')
            filtr_text_gr1_dod = f"""(df['grupa_akcji_1_dodania'].isin({filtr_gr1_dod}))"""
            list_to_loc.append(filtr_text_gr1_dod)

    if gr_2_dod:
        with st.container(border=True):
            options_gr2_dod = uniq_data['grupa_akcji_2_dodania'].dropna().sort_values()
            filtr_gr2_dod = st.multiselect(options=options_gr2_dod, label='Filtruj po grupie akcji 2 dodania')
            filtr_text_gr2_dod = f"""(df['grupa_akcji_2_dodania'].isin({filtr_gr2_dod}))"""
            list_to_loc.append(filtr_text_gr2_dod)

    if rok_dod:
        with st.container(border=True):
            options_rok = uniq_data['rok_dodania'].dropna().sort_values().to_list()
            filtr_rok_dod = st.slider(label='Filtruj po roku dodania', min_value=2008, max_value=int(options_rok[-1]),
                              value=[int(options_rok[-5]), int(options_rok[-1])])
            filtr_text_rok_dod = f"""(df['rok_dodania'].isin({filtr_rok_dod}))"""
            list_to_loc.append(filtr_text_rok_dod)
    if przedzial_wieku:
        with st.container(border=True):
            options_przedzial_wieku = uniq_data['przedzial_wieku'].dropna().sort_values().to_list()
            filtr_przedzial_wieku = st.multiselect('Filtruj po przedziale wieku', options=options_przedzial_wieku)
            filtr_text_przedzial_wieku = f"""(df['przedzial_wieku'].isin({filtr_przedzial_wieku}))"""
            list_to_loc.append(filtr_text_przedzial_wieku)


    return list_to_loc
