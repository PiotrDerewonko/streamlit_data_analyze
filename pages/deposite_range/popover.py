from typing import List

import streamlit as st


def add_popover() -> List:
    """Funkcja ma za zadanie dodać popovery dodatkowymi litrami i zwrocić listę dodatkowych filtrów do loc"""
    list_to_loc = []
    popover = st.popover('Wybierz dodatkowe filtry')
    gr_2_wpl = popover.checkbox('Filtruj po grupie akcji 2 wpłaty', False)

    if gr_2_wpl:
        with st.container(border=True):
            #todo dodac tutaj aby bral z listy unikalny warttosci a nie na sztywno
            filtr = st.multiselect(options=['MAILING Q1', 'MAILING Q2'], default=['MAILING Q1'], label='Filtruj po mailingu')
            filtr_text = f"""(df['grupa_akcji_2_wplaty'].isin({filtr}))"""
            list_to_loc.append(filtr_text)

    return list_to_loc