import streamlit as st

from charts.basic_chart_bokeh import CreateCharts
from pages.intentions.filter_data import filter_data
from pages.intentions.modificate_data import create_df_with_options, change_int_to_str_columns, delate_dupliactes


class ChartForCountIntentions:
    """Zadaniem tej klasy jest przygotowanie danych, które nastepnie są wykorzystywane do tworzenia wykresow
    z danych dotyczacych przeslanych intencji oraz wplat. Klasa nie zwraca żadnych danych a jedynie wstawia
    wykres i tabele przestwna w odpowiendi miejsce aplikacji"""
    def __init__(self, data_to_analyze, type_of_campaign, camp, year, data_to_char_x_axis,
                 columns_name, title, x_title, y_title):
        self.data_to_analyze = data_to_analyze
        self.type_of_campaign = type_of_campaign
        self.camp = camp
        self.year = year
        self.data_to_char_x_axis = data_to_char_x_axis
        self.columns_name = columns_name
        self.title = title
        self.x_title = x_title
        self.y_title = y_title
        self.data_to_pivot_table = None
        self.pivot_table_to_char_wout_margins = None
        self.pivot_table_to_char = None

    def prepare_data(self):
        filtered_data = filter_data(self.data_to_analyze, self.type_of_campaign, self.camp, self.year)
        self.data_to_pivot_table = change_int_to_str_columns(filtered_data, self.data_to_char_x_axis)

    def create_pivot_table(self, value_param, aggfunc_par):
        self.pivot_table_to_char = self.data_to_pivot_table.pivot_table(index=self.data_to_char_x_axis,
                                                                        values=value_param,
                                                                        aggfunc=aggfunc_par,
                                                                        margins=True)
        # zmieniam nazwe kolumny w tabeli przestawnej aby bylo czytelniej na wykresie
        self.pivot_table_to_char = self.pivot_table_to_char.rename({'correspondent_id': self.columns_name},
                                                                   axis='columns')
        self.pivot_table_to_char_wout_margins = self.pivot_table_to_char.iloc[:-1]

    def create_chart(self):
        temp_df = create_df_with_options(self.pivot_table_to_char_wout_margins)
        intention_count_char = CreateCharts(self.data_to_pivot_table, self.data_to_char_x_axis,
                                            self.title, self.x_title, self.y_title,
                                            self.pivot_table_to_char_wout_margins, temp_df)
        intention_count_char.create_chart()
        with st.expander("Tabela przestawna"):
            st.dataframe(self.pivot_table_to_char)


class ChartForUniqeIdFromIntentions(ChartForCountIntentions):
    def prepare_data(self):
        """Dodatkowa linijka usuwa zduplikowane dane. Ma to na celu pokazanie ile osob przeslalo dany typ intencji
        a nie ile bylo sztuk intencji."""
        self.data_to_analyze = delate_dupliactes(self.data_to_analyze, self.data_to_char_x_axis)
        super().prepare_data()


