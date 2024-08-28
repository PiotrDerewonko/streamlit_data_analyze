import copy
import os

import pandas as pd


def download_data(con, text) -> pd.DataFrame:
    list_of_id_gr2 = pd.read_sql_query('''select id from fsaps_dictionary_action_group_two 
    where is_for_billing = True order by text''', con)
    list_of_id_gr2 = list_of_id_gr2['id'].tolist()
    list_of_years = pd.read_sql_query('''select id::int from fsaps_dictionary_action_group_three 
    where id <>7 order by text''', con)
    list_of_years = list_of_years['id'].tolist()
    data = pd.DataFrame()
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     f'../.././sql_queries/{text}.sql'))
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

def down_data_sum_and_count(con, refresh_data, engine) -> pd.DataFrame:
    if refresh_data == 'True':
        data = download_data(con, '2_ma_detail/count_and_sum_amount_char_for_days')
        data['dzien_po_mailingu'].fillna(999, inplace=True)
        data['dzien_po_mailingu'] = data['dzien_po_mailingu'].astype(int)
        data.to_sql('dash_char_ma_data', engine, if_exists='replace', schema='raporty', index=False)
    data = pd.read_sql_query('''select * from raporty.dash_char_ma_data''', con)
    return data

def down_data_cost_and_circulation(con, refresh_data, engine) -> pd.DataFrame:
    if refresh_data == 'True':
        data = download_data(con, '2_ma_detail/cost_and_cirtulation_for_char_days')
        data.to_sql('dash_char_ma_data_cost_cir', engine, if_exists='replace', schema='raporty', index=False)
    data = pd.read_sql_query('''select * from raporty.dash_char_ma_data_cost_cir''', con)
    data['koszt'] = data['koszt'].astype(float)
    return data