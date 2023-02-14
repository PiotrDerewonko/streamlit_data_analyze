import pandas as pd
import streamlit as st
from dotenv import dotenv_values

from pages.ma_details_files.char_options.char_options_part_1 import char_options_part1, char_options_part2
from pages.ma_details_files.char_options.char_options_part_2 import label_orientations


def char_options():
    sorce_main = dotenv_values('.env')
    sorce_main = list(sorce_main.values())[0]
    refresh_data = 'False'
    with st.container():
        st.subheader("Wartośc bezwzgledne")
        option_1 = char_options_part1()
        st.subheader("Współczynniki")
        option_2 = char_options_part2()
        all = pd.concat([option_1, option_2])
        st.subheader("Tytuły")
        title = st.text_input('Miejsce na tytuł')
        sub_title = st.text_input('Miejsce na pod tytuł')
        st.subheader("Ustawienia orientacji osi")
        dict_of_oriantation = label_orientations()
    return all, title, sub_title, dict_of_oriantation
