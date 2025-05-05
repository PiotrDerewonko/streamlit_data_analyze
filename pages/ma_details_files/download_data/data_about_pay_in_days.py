import os
import pandas as pd
from pages.main_diractor.download_data_main import DownloadDataMain
import copy
from database.read_file_sql import read_file_sql


class DataAboutSumAndCountInDays(DownloadDataMain):
    """Klasa generuje dane potrzebne do wykresów w dniach od nadania dla mailingu adresowego."""

    def download_data_with_extra_replace(self, text) -> pd.DataFrame:
        list_of_id_gr2 = pd.read_sql_query('''select id from fsaps_dictionary_action_group_two 
        where is_for_billing = True order by text''', self.con)
        list_of_id_gr2 = list_of_id_gr2['id'].tolist()
        list_of_years = pd.read_sql_query('''select id::int from fsaps_dictionary_action_group_three 
        where id <>7 order by text''', self.con)
        list_of_years = list_of_years['id'].tolist()
        data = pd.DataFrame()

        # zmienna pomocnicza konieczna do określenia roku poprzedniego, ponieważ w bazie danych jest jedna wartość
        # nie liczbowa
        tmp = 0
        for j in list_of_years:
            for i in list_of_id_gr2:
                zapytanie_copy = copy.copy(text)
                zapytanie_copy = zapytanie_copy.replace("#A#", str(i))
                zapytanie_copy = zapytanie_copy.replace("#B#", str(j))
                if tmp > 0:
                    zapytanie_copy = zapytanie_copy.replace("#C#", str(list_of_years[tmp - 1]))
                else:
                    zapytanie_copy = zapytanie_copy.replace("#C#", str(list_of_years[tmp]))
                data_tmp = pd.read_sql_query(zapytanie_copy, self.con)
                data = pd.concat([data, data_tmp])
            tmp += 1
            if self.test_mode & (tmp == 3):
                break
        return data

class DataAboutCostAndCirculationsInDays(DownloadDataMain):
    """Klasa generuje dane potrzebne do wykresów w dniach od nadania dla mailingu adresowego."""


def generate_data_about_sum_and_count_in_days(con, engine, test_mode=False) -> None:
    """Funkcja tworzy obiekt klasy, który generuje dane potrzebne do raportów w dniach od nadania dla mailingu adresowego."""
    table_name = 'dash_char_ma_data'
    sum_and_count_in_days = DataAboutSumAndCountInDays(con, engine, table_name, test_mode=test_mode)
    sql_file = read_file_sql('sql_queries/2_ma_detail/count_and_sum_amount_char_for_days.sql')
    data_to_analyze = sum_and_count_in_days.download_data_with_extra_replace(sql_file)
    sum_and_count_in_days.insert_data(data_to_analyze)

def download_data_about_sum_and_count_in_days(con, engine, test_mode=False) -> pd.DataFrame:
    """Funkcja tworzy obiekt klasy, który pobiera dane potrzebne do raportów w dniach od nadania dla mailingu adresowego."""
    table_name = 'dash_char_ma_data'
    sum_and_count_in_days = DataAboutSumAndCountInDays(con, engine, table_name, test_mode=test_mode)
    data_to_analyze = sum_and_count_in_days.download_data()
    return data_to_analyze

def generate_data_about_cost_and_circulation_in_days(con, engine, test_mode=False) -> None:
    """Funkcja tworzy obiekt klasy, który generuje dane potrzebne do raportów w dniach od nadania dla mailingu adresowego."""
    table_name = 'dash_char_ma_data_cost_cir'
    sum_and_count_in_days = DataAboutSumAndCountInDays(con, engine, table_name, test_mode=test_mode)
    sql_file = read_file_sql('sql_queries/2_ma_detail/cost_and_circulation_for_char_days.sql')
    data_to_analyze = sum_and_count_in_days.download_data_with_extra_replace(sql_file)
    sum_and_count_in_days.insert_data(data_to_analyze)

def download_data_about_cost_and_circulation_in_days(con, engine, test_mode=False) -> pd.DataFrame:
    """Funkcja tworzy obiekt klasy, który pobiera dane potrzebne do raportów w dniach od nadania dla mailingu adresowego."""
    table_name = 'dash_char_ma_data_cost_cir'
    sum_and_count_in_days = DataAboutSumAndCountInDays(con, engine, table_name, test_mode=test_mode)
    data_to_analyze = sum_and_count_in_days.download_data()
    return data_to_analyze
