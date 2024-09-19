from typing import Tuple, Any, Dict, List

import pandas as pd
import streamlit as st

from pages.ma_details_files.charts_in_days.download_data_for_days_charts import download_data_for_days_charts
from pages.ma_details_files.data_about_people_and_campaign_pay import distinct_options
from pages.ma_details_files.data_about_people_and_campaign_pay import download_data_about_people


class ChartsInDays:
    def __init__(self, mailing, con, years, refresh_data, engine):
        self.mailing = mailing
        self.con = con
        self.years = years
        self.refresh_data = refresh_data
        self.engine = engine
        self.data_cost_and_circulation = None
        self.data_sum_count = None

    @staticmethod
    def choose_filter_options() -> Dict[Any, List[Any]]:
        """Metoda dodaje opcje filtrowania danych po kolumnach. Zwraca słownik, gdzie kluczem jest nazwa kolumny,
        a wartoscia jest lista z wybranymi opcjami."""
        filter_value = distinct_options(False)
        list_of_filter_value = filter_value.columns.to_list()

        # zamieniam pierwszy element z id_korespondenta na pusta wartosc
        list_of_filter_value[0] = ' '

        filtr_1_column_name = st.selectbox(label="Pierwszy filtr", options=list_of_filter_value)
        filtr_1_values = st.multiselect(label="Wybierz wartosci",
                                        options=filter_value[filtr_1_column_name].dropna().drop_duplicates())

        st.markdown(filtr_1_column_name, unsafe_allow_html=True)
        st.markdown(filtr_1_values, unsafe_allow_html=True)

        dict_to_return = {filtr_1_column_name: filtr_1_values}
        return dict_to_return

    def create_tabs(self) -> Tuple[Any, Any, Any, Any, Any, Any, Any, Any, Any, Dict[Any, List[Any]]]:
        """Metoda tworzy zakladki potrzebne, w których wybieramy jakie dane mają znaleść się na wykresie. 
        Dodatkowo metoda umiesza wygenerowane wykresy i tabele przestawne """
        with st.container():
            tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
                ['Suma Wpłat', 'Liczba Wpłat', 'Stopa zwrotu liczby wplat', 'ROI',
                 'Profit', 'Ustawienia', 'Filtry'])
            with tab6:
                days_range = st.slider('Proszę wybrać dnia od nadania mailingu', min_value=1, max_value=60,
                                       value=[1, 60])
                cumulative = st.checkbox(label='Wykresy kumulacyjnie', value=True)
                new_old = st.checkbox(label='Podział nowi/starzy', value=False)

                chose_new_old = st.multiselect(label='Kogo wyświetlać', options=['nowy', 'stary'],
                                               default=['nowy', 'stary'])
            with tab7:
                dict_of_user_choice = self.choose_filter_options()
        return days_range, cumulative, new_old, chose_new_old, tab1, tab2, tab3, tab4, tab5, dict_of_user_choice

    def download_data(self):
        """Metoda pobiera dane niezbedne do dalszej analizy."""
        self.data_sum_count = download_data_for_days_charts(self.con, self.engine, False, 'dash_char_ma_data_by_id',
                                                            '10_chart_in_days/count_and_sum_amount_char_for_days')
        self.data_cost_and_circulation = download_data_for_days_charts(self.con, self.engine, False,
                                                                       'dash_char_ma_data_cost_cir_by_id',
                                                                       '10_chart_in_days/cost_and_cirtulation_for_char_days')
        self.data_cost_and_circulation['koszt'] = self.data_cost_and_circulation['koszt'].astype(float)
        self.data_cost_and_circulation['grupa_akcji_3_wysylki'] = self.data_cost_and_circulation[
            'grupa_akcji_3_wysylki'].astype(str)
        data_about_people = download_data_about_people(self.con, False, 10000, [])
        self.data_sum_count = pd.merge(self.data_sum_count, data_about_people, on='id_korespondenta', how='left')
        self.data_sum_count['grupa_akcji_3_wysylki'] = self.data_sum_count['grupa_akcji_3_wysylki'].astype(str)
        self.data_cost_and_circulation = pd.merge(self.data_cost_and_circulation, data_about_people,
                                                  on='id_korespondenta', how='left')

    def filtr_data_by_user_choise(self, filtr_value) -> None:
        """Metoda filtruje dane na podsatwie wybranych przez uzuytkonika danych w zakaldce filtry"""
        for i, j in filtr_value.items():
            column_to_filter = i
            values_to_filter = j
            self.data_sum_count = self.data_sum_count.loc[self.data_sum_count[column_to_filter].isin(values_to_filter)]
            self.data_cost_and_circulation = self.data_cost_and_circulation.loc[
                self.data_cost_and_circulation[column_to_filter].isin(values_to_filter)]
