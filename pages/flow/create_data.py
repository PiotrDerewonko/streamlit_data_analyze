import os
from typing import Dict, Tuple

import pandas as pd

# from database.source_db import mongo_connect
from pages.flow.add_cut_and_wrong_address import add_cut_and_wrong_address
from pages.flow.filtr_options import FiltrOptions


def download_data_about_flow(refresh_data) -> pd.DataFrame:
    """Funkcja tworzy dane do wykresu przeplywow, jej zadaniem jest przygotowanie danych z ktorych mozna odfiltrowac
     korespondentow po filtrach"""

    # db = mongo_connect()
    # collection = db['data_flow']

    if refresh_data =='True':
        # pobranie orginlanych danych o kampaniach i ich odfiltorowanie
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ma_details_files/tmp_file/people_camp.csv'))
        data_original_campaing = pd.read_csv(csv_path, index_col='Unnamed: 0',
                                             low_memory=False)
        data_original_campaing = data_original_campaing.sort_values(by=['id_korespondenta'])
        data_original_short = data_original_campaing[
            ['id_korespondenta', 'grupa_akcji_3_wysylki', 'TYP DARCZYŃCY']].drop_duplicates()
        # data_original_short = data_original_short.iloc[0:10000]
        data_original_short = data_original_short

        # pobieram orginalne dane na temat ludzi
        csv_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'ma_details_files/tmp_file/people.csv'))
        data_original_people = pd.read_csv(csv_path, index_col='Unnamed: 0',
                                           low_memory=False)
        data_original_people = data_original_people.sort_values(by=['id_korespondenta'])
        # data_original_people_short = data_original_people.iloc[0:10000]
        data_original_people_short = data_original_people

        # zapisuje dane w bazie mongo
        data_all = pd.merge(data_original_short, data_original_people_short, how='left', on=['id_korespondenta'])

        # dodaje wszystkich ludzi ktorzy weszli w danym
        max_year = int(str(data_original_people['data_dodania'].dropna().max())[:4])
        data_all = add_cut_and_wrong_address(data_all, max_year, data_original_people_short)

        # collection.delete_many({})
        # collection.insert_many(data_all.to_dict('records'))

        # todo po zainstlwoaniu mongo zmienic na mongo a nic csv
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_files/data_all.csv'))
        data_all.to_csv(csv_path, index=False)

    else:
        # Pobierz wszystkie dokumenty z kolekcji
        # documents = list(collection.find())

        # Zamień wynik na ramkę danych
        # data = pd.DataFrame(documents)
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_files/data_all.csv'))
        data = pd.read_csv(csv_path, low_memory=False)
        return data


def create_filter() -> Tuple[pd.DataFrame, Dict]:
    filtr_options = FiltrOptions()
    filtr_options.choose_years_of_add()
    filtr_options.choose_years_to_analyze()
    filtr_options.add_other_options()

    return filtr_options.options


def filtr_data(data, options) -> pd.DataFrame:
    """Metoda filtruje ramkę danych na podstawie przekazanego słownika z filtrami. Jeżeli jest przekazny tuple,
    wtedy znaczy to, że wartośc jest pobrana ze slajdera. Jeśli jest przekazana lista znaczy, że pochodzi od filtra
    użytkownika. """
    for i, j in options.items():
        if isinstance(j, tuple):
            data = data.loc[(data[i] >= j[0]) & (data[i] <= j[1])]
        elif isinstance(j, list):
            data = data.loc[data[i].isin(j)]
    return data


def transform_data_about_flow(data) -> pd.DataFrame:
    """zadaniem funkcji jest swtorzenie data frame ktory posluzy do stworzenia przeplywow. Wynikowa ramka danych
    ma wygladac w sposob source, target, ilosc."""

    data_to_return = pd.DataFrame()

    # pobieram liste lat z danych
    years_list = data['grupa_akcji_3_wysylki'].drop_duplicates().tolist()
    years_list.sort()

    for i in years_list:
        data_current_year = data[data['grupa_akcji_3_wysylki'] == i]
        data_next_year = data[data['grupa_akcji_3_wysylki'] == (i + 1)]
        data_compare = pd.merge(data_current_year, data_next_year, how='left', on=['id_korespondenta'],
                                suffixes=('_current', '_next'))
        data_compare_short = data_compare[['TYP DARCZYŃCY_current', 'TYP DARCZYŃCY_next', 'id_korespondenta']]
        data_compare_short['TYP DARCZYŃCY_current'] = str(i) + '_' + data_compare_short['TYP DARCZYŃCY_current']
        data_compare_short['TYP DARCZYŃCY_next'] = str(i + 1) + '_' + data_compare_short['TYP DARCZYŃCY_next']
        data_compare_short['typ_tmp'] = data_compare_short['TYP DARCZYŃCY_current'] + "#" + data_compare_short[
            'TYP DARCZYŃCY_next']
        tmp_pivot = data_compare_short.pivot_table(index=['typ_tmp'], values='id_korespondenta', aggfunc='count')
        data_to_return = pd.concat([data_to_return, tmp_pivot])

    # rozdzielam kolumne tymczasowa oraz ja usuwam
    data_to_return = data_to_return.reset_index()
    data_to_return[['source', 'target']] = data_to_return['typ_tmp'].str.split('#', expand=True)
    data_to_return = data_to_return.drop(columns=['typ_tmp'])
    data_to_return = data_to_return.rename(columns={'id_korespondenta': 'value'})
    return data_to_return
