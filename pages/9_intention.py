import pandas as pd
import streamlit as st
from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.intentions.choose_options import ChooseOptionsForIntentions
from pages.intentions.download_data_intention import download_data_intention_count, download_data_intention_money

with st.container():
    sorce_main = dotenv_values('.env')
    sorce_main = list(sorce_main.values())[0]
    mailings, con, engine = deaful_set(f'{sorce_main}')

    count_intentions = download_data_intention_count(con, False)
    money_intentions = download_data_intention_money(con, False)
    data_all_intentions = pd.concat([count_intentions, money_intentions])
    data_all_intentions['intencja'].fillna(0, inplace=True)
    data_all_intentions['kwota'].fillna(0, inplace=True)

    #Pobieram wybrane opcje
    test = ChooseOptionsForIntentions(con)
    a, b, c = test.choose_options()




