import pandas as pd
import streamlit as st
from dotenv import dotenv_values

from charts.basic_chart_bokeh import CreateCharts
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
    data_all_intentions['kwota'].fillna(0, inplace=True)

    # Pobieram wybrane opcje
    intention_options = ChooseOptionsForIntentions(con)
    camp, year, type_of_campaign = intention_options.choose_options()

    # Filtruje dane dotyczace ilosci intencji
    filtered_data = filter_data(data_all_intentions, type_of_campaign, camp, year)
    test = filtered_data.pivot_table(columns=['grupa_akcji_2'], index=['patron'], values='correspondent_id',
                                     aggfunc='count')
    st.dataframe(test)
    st.bar_chart(test)
    temp_df = pd.DataFrame(data={'Nazwa parametru': ['MAILING Q2'],
                                 'oś': ['Oś główna'],
                                 'Opcje': ['Wykres Słupkowy', ]
                                 }, index=[0])
    test = CreateCharts(data_all_intentions, ['patron'], 'test', 'test', 'test', test,
                        temp_df)
    test.create_chart()
