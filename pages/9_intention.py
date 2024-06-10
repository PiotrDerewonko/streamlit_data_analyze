import pandas as pd
import streamlit as st
from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.intentions.choose_options import ChooseOptionsForIntentions
from pages.intentions.download_data_intention import download_data_intention_count, download_data_intention_money
from pages.intentions.filter_data import filter_data

with st.container():
    sorce_main = dotenv_values('.env')
    sorce_main = list(sorce_main.values())[0]
    mailings, con, engine = deaful_set(f'{sorce_main}')

    count_intentions = download_data_intention_count(con, False)
    money_intentions = download_data_intention_money(con, False)
    data_all_intentions = pd.concat([count_intentions, money_intentions])
    data_all_intentions['intencja'].fillna(0, inplace=True)
    data_all_intentions['kwota'].fillna(0, inplace=True)

    # Pobieram wybrane opcje
    intention_options = ChooseOptionsForIntentions(con)
    camp, year, type_of_campaign = intention_options.choose_options()

    # Filtruje dane
    filtered_data = filter_data(data_all_intentions, type_of_campaign, camp, year)
    test = filtered_data.pivot_table(columns=['grupa_akcji_1'], values='correspondent_id', aggfunc='count')
    st.dataframe(test)
