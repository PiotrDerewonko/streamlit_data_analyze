import streamlit as st
from dotenv import dotenv_values

from pages.ma_details_files.char_options.char_options_part_1 import char_options_part1, char_options_part2


def char_options():
    sorce_main = dotenv_values('.env')
    sorce_main = list(sorce_main.values())[0]
    refresh_data = 'False'
    with st.container():
        st.subheader("Wartośc bezwzgledne")
        option_1 = char_options_part1()
        st.subheader("Współczynniki")
        char_options_part2()
    return option_1
