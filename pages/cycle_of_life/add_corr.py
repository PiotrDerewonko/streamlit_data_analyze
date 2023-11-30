import os

import pandas as pd

'''pobieram dane kazdego korespondenta z kazdego roku i multiplikuje te dane tak aby kazdy korespodent byl tyle razy
ile lat jest juz w bazie danych'''


def download_correspondent_data(con, aktualny_rok, data_all) -> pd.DataFrame:
    for i in range(2008, aktualny_rok):
        numbers_of_years = aktualny_rok - i
        sql_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), f'../.././sql_queries/7/people_from_year.sql'))
        with open(sql_file_path, 'r') as sql_file_2:
            sql_file = sql_file_2.read()
        sql_file = sql_file.replace('{rok}', str(i))
        data_tmp = pd.read_sql_query(sql_file, con)
        data_tmp['aktualny_rok'] = i
        data_tmp['aktualny_numer_roku'] = 1
        data_all = pd.concat([data_all, data_tmp])
        for j in range(0, numbers_of_years):
            data_tmp['aktualny_rok'] += 1
            data_tmp['aktualny_numer_roku'] += 1
            data_all = pd.concat([data_all, data_tmp])
        data_tmp['aktualny_numer_roku_int'] = data_tmp['aktualny_numer_roku']
        data_tmp['aktualny_numer_roku'] = data_tmp['aktualny_numer_roku'].astype(str)
        data_tmp['aktualny_numer_roku'].loc[data_tmp['aktualny_numer_roku_int'] < 10] = (
                '0' + data_tmp['aktualny_numer_roku'])
        data_tmp.drop(['aktualny_numer_roku_int'], inplace=True)
    return data_all


def download_pay_data(con, data_all, aktualny_rok) -> pd.DataFrame:
    all_data_pay = pd.DataFrame()
    for i in range(2008, aktualny_rok):
        sql_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), f'../.././sql_queries/7/pay_on_year.sql'))
        with open(sql_file_path, 'r') as sql_file_2:
            sql_file = sql_file_2.read()
        sql_file = sql_file.replace('{rok}', str(i))
        data_tmp = pd.read_sql_query(sql_file, con)
        data_tmp['aktualny_rok'] = i
        all_data_pay = pd.concat([all_data_pay, data_tmp])
    data_all = pd.merge(left=data_all, right=all_data_pay, on=['id_korespondenta', 'aktualny_rok'], how='left')
    data_all['wplata'].fillna('brak_wpłaty', inplace=True)
    data_all['miesiac_pierwszej_wplaty_w_roku'].fillna(0, inplace=True)
    return data_all


def download_mailings(con, data_all, aktualny_rok) -> pd.DataFrame:
    all_data_pay = pd.DataFrame()
    for i in range(2008, aktualny_rok):
        sql_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), f'../.././sql_queries/7/mailing.sql'))
        with open(sql_file_path, 'r') as sql_file_2:
            sql_file = sql_file_2.read()
        sql_file = sql_file.replace('{rok}', str(i))
        data_tmp = pd.read_sql_query(sql_file, con)
        data_tmp['aktualny_rok'] = i
        all_data_pay = pd.concat([all_data_pay, data_tmp])
    data_all = pd.merge(left=data_all, right=all_data_pay, on=['id_korespondenta', 'aktualny_rok'], how='left')
    data_all['udzial'].fillna('nie_brał_udziału', inplace=True)
    return data_all


def download_good_adress(con, data_all) -> pd.DataFrame:
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), f'../.././sql_queries/7/good_adress.sql'))
    with open(sql_file_path, 'r') as sql_file_2:
        sql_file = sql_file_2.read()
    data_tmp = pd.read_sql_query(sql_file, con)
    data_all = pd.merge(left=data_all, right=data_tmp, on=['id_korespondenta'], how='left')
    data_all['adres'].fillna('adres_niepoprawny', inplace=True)
    return data_all


def modificate_data(data_all) -> pd.DataFrame:
    data_all['poprawki'] = ''
    # todo to do sprawdzenia jak dziala
    index_change_adress = data_all.loc[(data_all['adres'] == 'adres_niepoprawny') &
                                       (data_all['udzial'] == 'brał_udział')].index
    data_all['adres'].loc[index_change_adress] = 'poprawny_adres'
    data_all['poprawki'].loc[index_change_adress] = data_all['poprawki'] + 'poprawwiony adres '
    index_change_mailings = data_all.loc[(data_all['udzial'] == 'nie_brał_udziału') &
                                         (data_all['adres'] == 'poprawny_adres') &
                                         (data_all['rok_dodania'] == data_all['aktualny_rok'])].index
    data_all['udzial'].loc[index_change_mailings] = 'brał_udział'
    data_all['poprawki'].loc[index_change_mailings] = data_all['poprawki'] + 'poprawiony mailing '
    return data_all
