from typing import List

import pandas as pd

from pages.intentions.modificate_data import create_df_with_options
from pages.ma_details_files.charts_in_days.basic_chart_bokeh_overwrite import BasicChartBokehOverwrite


class CreatePivotTableForChartsInDays:
    def __init__(self, mailing, years, days_from, days_to, data, cumulative, new_old, choose, choosed_options):
        self.mailing = mailing
        self.years = years
        self.days_from = days_from
        self.days_to = days_to
        self.data = data
        self.cumulative = cumulative
        self.new_old = new_old
        self.choose = choose
        self.data_to_show_not_show = None
        self.choosed_options = choosed_options



    def filtr_data_by_days_from_to(self) -> None:
        """zadaniem tej metody jest odfiltrowac dane za zakres dni wybrany przez użytkownika. Uwaga metody tej nie
        uzyzwac w wypadku klasy liczącej koszt oraz naklad. Dodatkowo, do zmiennej data_to_show_not_show,
        dodajemy dane od dnia pierwszego do wskazanego przez uzytkownika. Jest to niezbedne w przypadku gdy
        użyktownik wybral dzien poczatkowy inny niz 1, a chcemy aby np suma wplat byla pokazywana na 5 dzien od nadania.
        """

        if self.days_from > 1:
            self.data_to_show_not_show = self.data.loc[(self.data['dzien_po_mailingu'] <= self.days_from)]
            self.data = self.data.loc[
                (self.data['dzien_po_mailingu'] >= self.days_from + 1) & (
                        self.data['dzien_po_mailingu'] <= self.days_to)]
        else:
            self.data = self.data.loc[
                (self.data['dzien_po_mailingu'] >= self.days_from) & (self.data['dzien_po_mailingu'] <= self.days_to)]

    def filtr_data_by_user_options(self) -> List[str]:
        """Metoda filtruje dane na podstawienie przekazynch przez uzytkonika parametrów. Wynikiem jej dziaalnia jest
        lista okreslajaca jakie kolumny maja sie znalesc w tabeli przestawnej."""
        columns_for_pivot_table = []

        def _filtr_data(column_name, user_choices, days_from) -> None:
            """Zadaniem metody jest odfiltorwqnie danych na podstawie przekazanych paramwetrów"""
            self.data = self.data.loc[self.data[column_name].isin(user_choices)]
            if days_from > 1:
                self.data_to_show_not_show = self.data_to_show_not_show.loc[
                    self.data_to_show_not_show[column_name].isin(user_choices)]
            columns_for_pivot_table.append(column_name)

        if len(self.mailing) >= 1:
            _filtr_data('grupa_akcji_2_wysylki', self.mailing, self.days_from)
        if len(self.years) >= 1:
            _filtr_data('grupa_akcji_3_wysylki', self.years, self.days_from)
        if self.new_old:
            _filtr_data('nowy_stary', self.choose, self.days_from)

        for i in self.choosed_options:
            if i not in columns_for_pivot_table:
                columns_for_pivot_table.append(i)

        return columns_for_pivot_table

    def change_index_to_str(self, index: List) -> None:
        for i in index:

            if pd.api.types.is_integer_dtype(self.data[i]) or pd.api.types.is_float_dtype(self.data[i]):
                self.data[f'{i}_str'] = self.data[i].astype(str)
                self.data[f'{i}_str'].loc[self.data[i] < 10] = ('0' + self.data[f'{i}_str'])
                self.data = self.data.drop(columns=[i])
                self.data = self.data.rename(columns={f'{i}_str': i})

    def create_main_pivot_table(self, values, columns_for_pivot_table) -> pd.DataFrame:
        pivot_table = pd.pivot_table(self.data, index='dzien_po_mailingu', values=values,
                                     columns=columns_for_pivot_table, aggfunc='sum')
        return pivot_table

    def create_second_pivot_table(self, pivot_table, values, columns_for_pivot_table) -> pd.DataFrame:
        """Zadaniem metody jest stworzenie nowej tabeli przestawnej. Metoda ta bedzie wykorzystywana
        tylko w momencie gdy dzien od jest inny niz 1. W takim wypadku zostanie policzona tabela przestwna
        na wszystkie dni, a anstepnei zostanie wyciagnieta wartosc na wskazany przez uzytkownika dzien
        poczatkowy. ta tabela zosta nie nasteopnie polaczona z glowna tabela przestwna. Dzieki temu
        jesli 5 dnia od nadania bylo juz 1000 zl w sumie wplat, wartosc bedzie zaczynac sie od 1000
        a nie od 0. Metode uruchamiac tylko dal wylioczenia sumy oraz lcizby wplat"""
        pivot_table_sec = pd.pivot_table(self.data_to_show_not_show, index='dzien_po_mailingu', values=values,
                                         columns=columns_for_pivot_table, aggfunc='sum')
        pivot_table_sec = pivot_table_sec.cumsum()
        values_for_day_from = pivot_table_sec.loc[pivot_table_sec.index == self.days_from]
        pivot_table = pd.concat([values_for_day_from, pivot_table])
        return pivot_table

    def customize_pivot_table(self, pivot_table) -> pd.DataFrame:
        """Zadaniem metody jest, custmizacja tabel przestanwej."""
        pivot_table.fillna(0, inplace=True)
        if self.cumulative:
            pivot_table = pivot_table.cumsum()
        return pivot_table

    # def create_circulatuion_pivot_table_(self) -> pd.DataFrame:
    #     pivot_circulation = self.data_about_cicrulations.pivot_table(index=self.choosed_options,
    #                                                                  values=['id_korespondenta'],
    #                                                                  aggfunc='count')


    def create_char(self, pivot_table, y_label_title, char_title):
        df_with_options = create_df_with_options(pivot_table, 'Wykres liniowy')
        self.data['dzien_po_mailingu'] = self.data['dzien_po_mailingu'].astype(str)
        char_class = BasicChartBokehOverwrite(self.data, ['dzien_po_mailingu'], char_title,
                                              'Dzień po mailingu', y_label_title, pivot_table, df_with_options)
        final_char = char_class.create_chart(char_class.chart_class)
        return final_char

    @staticmethod
    def create_df_with_options_custom(data, char_type, extra_data) -> pd.DataFrame:
        """Tworzy tabele przestawna, ktora jest wykorzystywana jako przewodnik dla klasy tworzacej
        wykresu z ktorej kolumny jaki wykres ma zrobic."""

        columns_names = data.columns
        df_to_return = pd.DataFrame()
        for i in columns_names:
            temp_df = pd.DataFrame(data={'Nazwa parametru': [i],
                                         'oś': ['Oś główna'],
                                         'Opcje': [char_type],
                                         'Nakład': extra_data[i].iloc[0]
                                         }, index=[0])
            df_to_return = pd.concat([df_to_return, temp_df], ignore_index=True)
        return df_to_return

    def create_char_custom(self, pivot_table, y_label_title, char_title, extra_data):
        df_with_options = self.create_df_with_options_custom(pivot_table, 'Wykres liniowy', extra_data)
        self.data['dzien_po_mailingu'] = self.data['dzien_po_mailingu'].astype(str)
        char_class = BasicChartBokehOverwrite(self.data, ['dzien_po_mailingu'], char_title,
                                              'Dzień po mailingu', y_label_title, pivot_table, df_with_options)
        final_char = char_class.create_chart(BasicChartBokehOverwrite.chart_class)
        return final_char




