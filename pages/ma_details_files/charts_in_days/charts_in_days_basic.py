from typing import Tuple, Any

import streamlit as st

from pages.ma_details_files.charts_in_days.download_data_for_days_charts import download_data_for_days_charts


class ChartsInDays:
    def __init__(self, mailing, con, years, refresh_data, engine):
        self.mailing = mailing
        self.con = con
        self.years = years
        self.refresh_data = refresh_data
        self.engine = engine
        self.data_cost_and_circulation = None
        self.data_sum_count = None

    def create_tabs(self) -> Tuple[Any, Any, Any, Any, Any, Any, Any, Any, Any]:
        """Metoda tworzy zakladki potrzebne, w których wybieramy jakie dane mają znaleść się na wykresie. 
        Dodatkowo metoda umiesza wygenerowane wykresy i tabele przestawne """
        with st.container():
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
                ['Suma Wpłat', 'Liczba Wpłat', 'Stopa zwrotu liczby wplat', 'ROI',
                 'Profit', 'Ustawienia'])
            with tab6:
                days_range = st.slider('Proszę wybrać dnia od nadania mailingu', min_value=1, max_value=60,
                                       value=[1, 60])
                cumulative = st.checkbox(label='Wykresy kumulacyjnie', value=True)
                new_old = st.checkbox(label='Podział nowi/starzy', value=False)

                chose_new_old = st.multiselect(label='Kogo wyświetlać', options=['nowy', 'stary'],
                                               default=['nowy', 'stary'])
        return days_range, cumulative, new_old, chose_new_old, tab1, tab2, tab3, tab4, tab5

    def download_data(self):
        """Metoda pobiera dane niezbedne do dalszej analizy."""
        self.data_sum_count = download_data_for_days_charts(self, False, 'dash_char_ma_data',
                                                                       'count_and_sum_amount_char_for_days')
        self.data_cost_and_circulation = download_data_for_days_charts(self, False, 'dash_char_ma_data_cost_cir',
                                                            'cost_and_cirtulation_for_char_days')
