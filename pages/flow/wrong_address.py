import os

import pandas as pd


def wrong_address(refresh, con):
    if refresh == 'True':
        sql_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         f'../../sql_queries/11_flow/wrong_address.sql'))
        with open(sql_file_path, 'r') as sql_file:
            zapytanie = sql_file.read()
        data = pd.read_sql(zapytanie, con)
        data.to_csv('./pages/flow/tmp_files/data_wrong_address.csv', index=False)
    else:
        data = pd.read_csv('./pages/flow/tmp_files/data_wrong_address.csv')
    return data