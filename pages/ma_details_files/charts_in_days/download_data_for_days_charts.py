import copy
import os

import pandas as pd


def download_data_for_days_charts(con, engine, refresh_data, table_name, file_name):
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'../..' ,f'chart_in_days/tmp_file/{table_name}.csv'))
    if refresh_data == 'True':
        data = download_data(con, file_name)
        data['dzien_po_mailingu'].fillna(999, inplace=True)
        data['dzien_po_mailingu'] = data['dzien_po_mailingu'].astype(int)
        data.to_csv(csv_path)
    else:
        data = pd.read_csv(csv_path, index_col='Unnamed: 0', low_memory=False)
    return data


def download_data(con, text) -> pd.DataFrame:
    list_of_id_gr2 = pd.read_sql_query('''select id from fsaps_dictionary_action_group_two 
    where is_for_billing = True order by text''', con)
    list_of_id_gr2 = list_of_id_gr2['id'].tolist()
    list_of_years = pd.read_sql_query('''select id::int from fsaps_dictionary_action_group_three 
    where id <>7 order by text''', con)
    list_of_years = list_of_years['id'].tolist()
    data = pd.DataFrame()
    a = os.path.join(os.path.dirname(__file__))
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     f'../../../sql_queries/{text}.sql'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()

    # zmienna pomocnicza konieczna do okreslenia roku poprzedniego, poniewaz w bazie danych jest jedna wartosc
    # nie liczbowa
    tmp = 0
    for j in list_of_years:
        for i in list_of_id_gr2:
            zapytanie_copy = copy.copy(zapytanie)
            zapytanie_copy = zapytanie_copy.replace("#A#", str(i))
            zapytanie_copy = zapytanie_copy.replace("#B#", str(j))
            if tmp > 0:
                zapytanie_copy = zapytanie_copy.replace("#C#", str(list_of_years[tmp - 1]))
            else:
                zapytanie_copy = zapytanie_copy.replace("#C#", str(list_of_years[tmp]))
            data_tmp = pd.read_sql_query(zapytanie_copy, con)
            data = pd.concat([data, data_tmp])
        tmp += 1
    return data
