import streamlit as st
from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.ma_details_files.charts_in_days.charts_in_days_basic import ChartsInDays
from pages.ma_details_files.choose_options import ChooseOptions
from pages.ma_details_files.column_order import distinct_columns

with st.container():
    sorce_main = dotenv_values('.env')
    sorce_main = list(sorce_main.values())[0]
    mailings, con, engine = deaful_set(f'{sorce_main}')

    #wybor ktorych mailingow ma dotyczyc analiza
    class_options = ChooseOptions(con)
    qamp, years, type_of_campaign = class_options.choose_options()

    #wybor jakie dane maja znalesc sie na wykresie
    option_list = distinct_columns()
    choosed_options = st.multiselect(options=option_list, default=['grupa_akcji_2_wysylki', 'grupa_akcji_3_wysylki'],
                                     label='Wybierz dane do wykresu')
    test = ChartsInDays(mailings, con, years, False, engine)
    test.create_tabs()
    test.download_data()


