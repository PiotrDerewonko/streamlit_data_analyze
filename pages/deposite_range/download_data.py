import os
from typing import Tuple

import pandas as pd

from functions_pandas.data_to_100_percent import data_to_100_percent
from pages.ma_details_files.create_df_for_char_options import create_df_for_char_options_structure
from pages.ma_details_files.data_about_people_and_campaign_pay import data_pay_all
from pages.ma_details_files.data_about_people_and_campaign_pay import download_data_about_people_camp


def download_data_for_deposite_range(deposite_range, year_range, year_range_to_analize, con,
                                     refresh_data) -> pd.DataFrame:
    """Funkcja ma za zadanie pobrac i odfiltrowac dane. W pierwszym kroku znajduje id osob ktore w podanym czasie
    dokonaly choc jednej wplaty w wybranym przedziale. W drugim, filtruje df tylko z osobami znalezionymi
    w kroku 1 i we wskaznym przez uzytkownika czasie"""
    data_about_pay_all = data_pay_all(con, refresh_data)
    data_filtered_id_kor = data_about_pay_all['id_korespondenta'].loc[
        (data_about_pay_all['grupa_akcji_3_wplaty'] >= year_range[0]) &
        (data_about_pay_all['grupa_akcji_3_wplaty'] <= year_range[1]) &
        (data_about_pay_all['przedzialy'] == deposite_range)].drop_duplicates().to_frame()
    data_filtered_id_kor['tmp_column'] = 'do_analizy'
    data_filtered_year = data_about_pay_all.loc[
        (data_about_pay_all['grupa_akcji_3_wplaty'] >= year_range_to_analize[0]) &
        (data_about_pay_all['grupa_akcji_3_wplaty'] <= year_range_to_analize[1])]
    data_to_return = pd.merge(data_filtered_year, data_filtered_id_kor, how='left', on='id_korespondenta').dropna(
        subset='tmp_column')
    return data_to_return


def create_pivot_table(data, index_for_pivot) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Funkcja ma za zadanie zwrocic tabele przestawna oraz slownik niezbedny do stworzenia wykresow """
    if 'grupa_akcji_3_wplaty' in index_for_pivot:
        data['grupa_akcji_3_wplaty'] = data['grupa_akcji_3_wplaty'].astype(str)
    pivot_table_with_margins = pd.pivot_table(data, index=index_for_pivot, columns='przedzialy',
                                              values='id_korespondenta',
                                              aggfunc='count', fill_value=0, dropna=False, margins=True,
                                              margins_name='Suma wpłat')
    pivot_table_without_margins = pivot_table_with_margins.drop(index=pivot_table_with_margins.index[-1],
                                                                columns=pivot_table_with_margins.columns[-1])
    pivot_table_to_100 = data_to_100_percent(pivot_table_without_margins)
    char_options = create_df_for_char_options_structure(pivot_table_without_margins)
    return pivot_table_without_margins, pivot_table_to_100, char_options, pivot_table_with_margins


def download_data_for_avg_number_per_year(con, year_range_to_analize) -> pd.DataFrame:
    """funckja pobiera wszystkie wplaty korespondentow w wybranych przez uzytkownika latach. Zapytanie nie pobiera
    wplat od kurii i parafii"""
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     f'../.././sql_queries/8/avg_count_per_year.sql'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()
    zapytanie = zapytanie.replace("#A#", str(year_range_to_analize[0]))
    zapytanie = zapytanie.replace("#B#", str(year_range_to_analize[1]))
    data_to_return = pd.read_sql(zapytanie, con)
    data_to_return['rok_wplaty'] = data_to_return['rok_wplaty'].astype(str)
    data_to_return.sort_values(by=['rok_wplaty'], inplace=True)
    return data_to_return


def add_extra_data_to_df_for_deposite_range(data, con, refresh_data) -> pd.DataFrame:
    """Zadaniem tej funkcji jest dodanie dodatkowych danych do pocztakowego zbioru. Nie beda zaciagane wszystkie dane
    jedynie wybrane ze wzgledu na optymalizacje zapytan"""
    data_about_peopla_in_camp = download_data_about_people_camp(con, refresh_data, None)
    data_about_peopla_in_camp = data_about_peopla_in_camp[
        ['id_korespondenta', 'przedzial_wieku', 'grupa_akcji_2_wysylki', 'grupa_akcji_3_wysylki']]
    data_about_peopla_in_camp['przedzial_wieku'].fillna('brak danych', inplace=True)
    data_to_return = pd.merge(data, data_about_peopla_in_camp, how='left',
                              left_on=['id_korespondenta', 'grupa_akcji_2_wplaty', 'grupa_akcji_3_wplaty'],
                              right_on=['id_korespondenta', 'grupa_akcji_2_wysylki', 'grupa_akcji_3_wysylki'])
    return data_to_return
