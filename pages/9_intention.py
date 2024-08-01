import pandas as pd
import streamlit as st
from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.intentions.charts_for_intention import ChartForCountIntentions, ChartForUniqeIdFromIntentions, \
    ChartForPercentOfPaymentWithIntentions
from pages.intentions.choose_options import ChooseOptionsForIntentions
from pages.intentions.download_data_intention import download_data_intention_count, download_data_intention_money
from pages.intentions.modificate_data import modificate_data, options_to_choose

with st.container():
    sorce_main = dotenv_values('.env')
    sorce_main = list(sorce_main.values())[0]
    mailings, con, engine = deaful_set(f'{sorce_main}')

    count_intentions = download_data_intention_count(con, False)
    money_intentions = download_data_intention_money(con, False)
    data_all_intentions = count_intentions
    data_about_people = pd.read_csv('./pages/ma_details_files/tmp_file/people.csv', index_col='Unnamed: 0',
                                    low_memory=False)
    data_to_analyze = modificate_data(data_all_intentions, data_about_people)
    options = options_to_choose()
    # Pobieram wybrane opcje
    with st.container(border=True):
        st.markdown('Odflitrowanie danych')
        intention_options = ChooseOptionsForIntentions(con)
        camp, year, type_of_campaign = intention_options.choose_options()

    with st.container(border=True):
        tab1_prim, tab2_prim = st.tabs(['Wykresy z intencji', 'Wykresy z wpłat'])

        with tab1_prim:
            data_to_char_x_axis = st.multiselect(options=options, label='Wybierz dane do wykresu z intencji',
                                                 default=['typ_intencji'])
            if len(data_to_char_x_axis) == 0:
                data_to_char_x_axis = ['grupa_akcji_1']
            tab1, tab2, tab5 = st.tabs(
                ['Wykres ilości przesłanych intencji', 'Wykres ilości ludzi którzy przesłali intencje', '% opłaconych intencji'])
            with tab1:
                chart_count_intention = ChartForCountIntentions(data_to_analyze, type_of_campaign, camp, year,
                                                                data_to_char_x_axis, 'liczba intencji',
                                                                'Wykres ilości przesłanych intencji',
                                                                '', 'ilość intencji')
                chart_count_intention.prepare_data()
                chart_count_intention.create_pivot_table('correspondent_id', 'count')
                chart_count_intention.create_chart()
            with tab2:
                chart_uniq_intention = ChartForUniqeIdFromIntentions(data_to_analyze, type_of_campaign, camp, year,
                                                                     data_to_char_x_axis, 'ilość_osób',
                                                                     'Wykres ilości osób ktore przesłały intencje',
                                                                     '', 'ilość_osób')
                chart_uniq_intention.prepare_data()
                chart_uniq_intention.create_pivot_table('correspondent_id', 'count')
                chart_uniq_intention.create_chart()
            with tab5:
                chart_percent = ChartForPercentOfPaymentWithIntentions(data_to_analyze, type_of_campaign, camp, year,
                                                                       data_to_char_x_axis, 'liczba_wplat',
                                                                       '% opłaconych intencji',
                                                                       '',
                                                                       '%')
                chart_percent.prepare_data()
                chart_percent.create_pivot_table('correspondent_id', 'count', money_intentions)
                chart_percent.create_chart()
        with tab2_prim:
            options_to_paymant_char = ['rok_wpłaty', 'miesiac_wpłaty', 'data_wpłaty', 'typ_intencji',
                                       'grupa_akcji_1_mailingu',
                                       'grupa_akcji_2_mailingu', 'grupa_akcji_3_mailingu']
            char_options_to_paymant_char = st.multiselect(options=options_to_paymant_char,
                                                          label='Wybierz dane do wykresu z wpłat',
                                                          default=['rok_wpłaty', 'miesiac_wpłaty'])
            tab3, tab4 = st.tabs(['Suma wpłat', 'Liczba wpłat'])

            with tab3:
                chart_money_values_intention = ChartForCountIntentions(money_intentions, type_of_campaign, camp, year,
                                                                       char_options_to_paymant_char, 'suma_wplat',
                                                                       'Wykres sumy wpłat z intencji',
                                                                       '', 'suma wpłat')
                chart_money_values_intention.prepare_data()
                chart_money_values_intention.create_pivot_table('kwota', 'sum')
                chart_money_values_intention.create_chart()
            with tab4:
                chart_money_count_intention = ChartForCountIntentions(money_intentions, type_of_campaign, camp, year,
                                                                      char_options_to_paymant_char, 'liczba_wplat',
                                                                      'Wykres liczby wpłat z intencji',
                                                                      '', 'liczba wpłat')
                chart_money_count_intention.prepare_data()
                chart_money_count_intention.create_pivot_table('kwota', 'count')
                chart_money_count_intention.create_chart()

