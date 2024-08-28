from typing import Tuple, List

import pandas as pd
import streamlit as st

from pages.ma_details_files.charts_in_days.pivot_table_fo_charts_in_days import CreatePivotTableForChartsInDays


def put_data_into_stremlit(tab_param, pivot_table_to_show, char):
    with tab_param:
        st.bokeh_chart(char, use_container_width=True)
        with st.expander('Zobacz tabele z danymi'):
            st.dataframe(pivot_table_to_show)


class CreatePivotTableAndChart:
    """Klasa tworzy nowy obiekt klasy CreatePivotTableForChartsInDays a nastepnie wykonuje jej metody.
    Klasa zosatal wprowadozna po to aby, efektywnie tworzyc tabele przestawne i wykresy"""

    def __init__(self, tab_param, qamp, years, days_from, days_to, data, cumulative, new_old,
                 chose_new_old, values, choosed_options):
        self.tab_param = tab_param
        self.qamp = qamp
        self.years = years
        self.days_from = days_from
        self.days_to = days_to
        self.data = data
        self.cumulative = cumulative
        self.new_old = new_old
        self.chosen_new_old = chose_new_old
        self.values = values
        self.choosed_options = choosed_options
        self.create_pivot_table_object = None

    def create_pivot_table(self) -> Tuple[pd.DataFrame, List]:
        """Metoda tworzy now obiekt klasy odpowiedzialnej za tworzenie tabel przestanwych i wykresow"""
        self.create_pivot_table_object = CreatePivotTableForChartsInDays(self.qamp, self.years, self.days_from,
                                                                         self.days_to, self.data, self.cumulative,
                                                                         self.new_old, self.chosen_new_old,
                                                                         self.choosed_options)
        self.create_pivot_table_object.filtr_data_by_days_from_to()
        # todo ta funckje trzeba przerobic tak, aby przyjmowala liste wybrana przez uzytkowniak i petla for gdzie sie da filtorwala oraz tworzyla finalna liste dla tabeli
        list_of_columns = self.create_pivot_table_object.filtr_data_by_user_options()
        self.create_pivot_table_object.change_index_to_str(['dzien_po_mailingu'])
        pivot_table_sum_amount = self.create_pivot_table_object.create_main_pivot_table(self.values, list_of_columns)
        return pivot_table_sum_amount, list_of_columns

    def change_pivot_table(self, pivot_table, list_of_columns) -> pd.DataFrame:
        if self.days_from > 1:
            pivot_table = self.create_pivot_table_object.create_second_pivot_table(pivot_table, self.values,
                                                                                   list_of_columns)
        return pivot_table

    def customize_pivot_table_(self, pivot_table) -> pd.DataFrame:
        pivot_table = self.create_pivot_table_object.customize_pivot_table(pivot_table)
        return pivot_table

    def put_data_into_streamlit(self, pivot_table, char) -> None:
        put_data_into_stremlit(self.tab_param, pivot_table, char)

    def create_char_helper(self, pivot_table, y_label_title, char_title):
        char = self.create_pivot_table_object.create_char(pivot_table, y_label_title, char_title)
        return char

    def create_char_helper_custom(self, pivot_table, y_label_title, char_title, extra_data):
        char = self.create_pivot_table_object.create_char_custom(pivot_table, y_label_title, char_title, extra_data)
        return char

    @staticmethod
    def calculation_roi_or_szlw(data_sum_or_count_amount, data_cost_or_circ, operation) -> pd.DataFrame:
        """Metoda przyjmuje trzy parametry, jeden to dataframe z liczba badz suma wplat, a drugi to data frame
        z nakladem lub kosztem oraz operacje jaka ma byc wykonanna. Pierwszy data frame ma zaostac podzielny lub odjety
        przez drugi i aby tro sie udalo, rugi datfarme musi zawierac tyle samo wierszy co pierwszy. W tym celu w petli
        dodajemy kolejne wiersze z kosztem lub nakladem ale z kolejnym dniem. W ten sposob uzyskujemy datafrme ktory ma
        taka sama ilsoc wierszy jak dataframe z suma/liczba wplat, i mozemy dokonac operacji"""
        df1_index_len = len(data_sum_or_count_amount)
        data_cost_or_circ_in_one_day = data_cost_or_circ.copy()
        for i in range(2, df1_index_len + 3):
            data_cost_or_circ_in_one_day['dzien_po_mailingu'] = i
            data_cost_or_circ = pd.concat([data_cost_or_circ, data_cost_or_circ_in_one_day])
        data_cost_or_circ.set_index('dzien_po_mailingu', inplace=True)
        method = getattr(data_sum_or_count_amount, operation)
        data_to_return = method(data_cost_or_circ)
        return data_to_return

