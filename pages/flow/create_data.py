from typing import Dict

import pandas as pd

from database.source_db import mongo_connect


def download_data_about_flow(refresh_data) -> pd.DataFrame:
    """Funkcja tworzy dane do wykresu przeplywow, jej zadaniem jest przygotowanie danych z ktorych mozna odfiltrowac
     korespondentow po filtrach"""

    db = mongo_connect()
    collection = db['data_flow']

    if refresh_data:
        # pobranie orginlanych danych o kampaniach i ich odfiltorowanie
        data_original_campaing = pd.read_csv('../ma_details_files/tmp_file/people_camp.csv', index_col='Unnamed: 0',
                                             low_memory=False)
        data_original_campaing = data_original_campaing.sort_values(by=['id_korespondenta'])
        data_original_short = data_original_campaing[
            ['id_korespondenta', 'grupa_akcji_3_wysylki', 'TYP DARCZYŃCY']].drop_duplicates()
        data_original_short = data_original_short.iloc[0:10000]

        # pobieram orginalne dane na temat ludzi
        data_original_people = pd.read_csv('../ma_details_files/tmp_file/people.csv', index_col='Unnamed: 0',
                                           low_memory=False)
        data_original_people = data_original_people.sort_values(by=['id_korespondenta'])
        data_original_people_short = data_original_people.iloc[0:10000]

        # todo dodac odcietych i zablkowanych ludzi

        # zapisuje dane w bazie mongo
        data_all = pd.merge(data_original_short, data_original_people_short, how='left', on=['id_korespondenta'])

        # collection.delete_many({})
        collection.insert_many(data_all.to_dict('records'))

    else:
        # Pobierz wszystkie dokumenty z kolekcji
        documents = list(collection.find())

        # Zamień wynik na ramkę danych
        data = pd.DataFrame(documents)
        return data


def filtr_data_about_flow(data: pd.DataFrame, filtr: Dict) -> pd.DataFrame:
    # todo zrobic filttrowanie
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
