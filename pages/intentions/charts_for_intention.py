import pandas as pd
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

    def create_pivot_table(self, value_param, aggfunc_par, is_cum_sum):
        self.pivot_table_to_char = self.data_to_pivot_table.pivot_table(index=self.data_to_char_x_axis,
                                                                        values=value_param,
                                                                        aggfunc=aggfunc_par,
                                                                        margins=True)
        # zmieniam nazwe kolumny w tabeli przestawnej aby bylo czytelniej na wykresie
        self.pivot_table_to_char = self.pivot_table_to_char.rename({'correspondent_id': self.columns_name},
                                                                   axis='columns')
        self.pivot_table_to_char_wout_margins = self.pivot_table_to_char.iloc[:-1]
        if is_cum_sum:
            self.pivot_table_to_char = self.pivot_table_to_char.cumsum()
            self.pivot_table_to_char_wout_margins = self.pivot_table_to_char_wout_margins.cumsum()

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


class ChartForPercentOfPaymentWithIntentions(ChartForCountIntentions):
    def create_pivot_table(self, value_param, aggfunc_par, money):
        '''Zadniem tej metody jest stworzenie tabeli przestawej zawierajacej informacje na temat % udzialu
        oplaconych intencji. Wazne jest to aby usunac duplikaty wplat, poniewaz nie ma tu znaczenia czy zostala
        dokonana  jedna czy wiele wplat, poniewaz na wykresie pokazujemy %. Dodatkowo, jesli przyszla wiecej niz
        jedna intencja od danego czlowieka, a dokonal on jednej wplaty, to wszystkie intencje polaczone z dana wplata
        zosrtana oznaczone jako oplacone.'''

        #lacze dane z intencji z danymi wplat po id korespodnenta i kodzie akcji
        money_direct = money.copy()
        money_direct['kwota'] = 1
        money_direct = money_direct[['correspondent_id', 'kod_akcji', 'kwota']].drop_duplicates()
        data_intention_plus_money = pd.merge(self.data_to_pivot_table,
                                             money_direct,
                                             how='left',
                                             on=['correspondent_id', 'kod_akcji'])
        data_intention_plus_money['grupa_akcji_2_mailingu'] = data_intention_plus_money[
            'grupa_akcji_2_mailingu'].fillna(' ')
        data_intention_plus_money['grupa_akcji_3_mailingu'] = data_intention_plus_money[
            'grupa_akcji_3_mailingu'].fillna(' ')

        #pobieram z danych o wplatach kolumny do laczenia po mailingach, odfiltrowuje dane, usuwam duplikaty we wplatach
        short_money = money[
            ['correspondent_id', 'kod_akcji', 'grupa_akcji_1_mailingu', 'grupa_akcji_2_mailingu',
             'grupa_akcji_3_mailingu', 'kwota']].copy()
        short_money['kwota'] = 1
        short_money = short_money.drop_duplicates()
        short_money_filtered = short_money.loc[short_money['grupa_akcji_2_mailingu'].isin(
            ['MAILING Q1', 'MAILING Q2', 'MAILING Q3', 'MAILING Q4'])]

        #prowencyjnie zamieniam grupe akcji 3 na str poniewaz pandas moze je potraktowac jako rok
        short_money_filtered['grupa_akcji_3_mailingu'] = short_money_filtered['grupa_akcji_3_mailingu'].astype('str')
        data_intention_plus_money['grupa_akcji_3_mailingu'] = data_intention_plus_money[
            'grupa_akcji_3_mailingu'].astype('str')

        #lacze dotychczasowe dane z wplatami raz jeszcze ale tym raz warunek laczenia mam bardzie ogolny
        data_intention_plus_money_extra = pd.merge(data_intention_plus_money,
                                                   short_money_filtered, how='left',
                                                   on=['correspondent_id', 'grupa_akcji_1_mailingu',
                                                       'grupa_akcji_2_mailingu', 'grupa_akcji_3_mailingu']
                                                   )

        #tworze pomocnicze kolumny oraz na jej podstawie tabele przestwna
        data_intention_plus_money_extra['is_payment'] = 'brak wpłaty'
        data_intention_plus_money_extra['is_payment'].loc[
            (data_intention_plus_money_extra['kwota_x'] > 0) | (
                    data_intention_plus_money_extra['kwota_y'] > 0)] = 'Wpłata'
        data_intention_plus_money_pivot_values = data_intention_plus_money_extra.pivot_table(
            index=self.data_to_char_x_axis,
            columns='is_payment',
            values=value_param,
            aggfunc=aggfunc_par, fill_value=0)

        #wyliczam procentowy udzial
        data_intention_plus_money_pivot_percent = data_intention_plus_money_pivot_values.copy()
        data_intention_plus_money_pivot_percent['% wpłat'] = data_intention_plus_money_pivot_percent[
                                                                 'Wpłata'] / (
                                                                     data_intention_plus_money_pivot_percent[
                                                                         'Wpłata'] +
                                                                     data_intention_plus_money_pivot_percent[
                                                                         'brak wpłaty'])
        data_intention_plus_money_pivot_percent = data_intention_plus_money_pivot_percent.drop(
            columns=['Wpłata', 'brak wpłaty'])
        self.pivot_table_to_char = data_intention_plus_money_pivot_percent
        self.pivot_table_to_char_wout_margins = data_intention_plus_money_pivot_percent
