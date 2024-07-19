import pandas as pd
import streamlit as st
from dotenv import dotenv_values

from charts.basic_chart_bokeh import CreateCharts
from database.source_db import deaful_set
from pages.intentions.choose_options import ChooseOptionsForIntentions
from pages.intentions.download_data_intention import download_data_intention_count, download_data_intention_money
from pages.intentions.filter_data import filter_data
from pages.intentions.modificate_data import modificate_data, options_to_choose, create_df_with_options, \
    change_int_to_str_columns

with st.container():
    sorce_main = dotenv_values('.env')
    sorce_main = list(sorce_main.values())[0]
    mailings, con, engine = deaful_set(f'{sorce_main}')

    count_intentions = download_data_intention_count(con, False)
    money_intentions = download_data_intention_money(con, False)
    data_all_intentions = pd.concat([count_intentions, money_intentions])
    data_all_intentions['kwota'].fillna(0, inplace=True)
    data_about_people = pd.read_csv('./pages/ma_details_files/tmp_file/people.csv', index_col='Unnamed: 0',
                                    low_memory=False)
    data_to_analyze = modificate_data(data_all_intentions, data_about_people)
    options = options_to_choose()
    # Pobieram wybrane opcje
    with st.container(border=True):
        st.markdown('Odflitrowanie danych')
        intention_options = ChooseOptionsForIntentions(con)
        camp, year, type_of_campaign = intention_options.choose_options()

    # wskazuje ktore dane maja pojawic sie na wykresie
    with st.container(border=True):
        data_to_char_x_axis = st.multiselect(options=options, label='Wskaż dane na wykres', default=['patron'])

    # Filtruje dane dotyczace ilosci intencji
    filtered_data = filter_data(data_to_analyze, type_of_campaign, camp, year)
    data_to_pivot_table = change_int_to_str_columns(filtered_data, data_to_char_x_axis)
    pivot_table_to_char = data_to_pivot_table.pivot_table(index=data_to_char_x_axis,
                                                    values='correspondent_id',
                                                    aggfunc='count')
    temp_df = create_df_with_options(pivot_table_to_char)
    test = CreateCharts(data_to_pivot_table, data_to_char_x_axis, 'test', 'test', 'test',
                        pivot_table_to_char, temp_df)
    test.create_chart()
