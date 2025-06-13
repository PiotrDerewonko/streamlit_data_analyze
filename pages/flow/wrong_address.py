import os

import pandas as pd


def wrong_address(refresh, con):
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_files/data_wrong_address.csv'))
    if refresh == 'True':
        sql_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         f'../../sql_queries/11_flow/wrong_address.sql'))
        with open(sql_file_path, 'r') as sql_file:
            zapytanie = sql_file.read()
        data = pd.read_sql(zapytanie, con)
        data.to_csv(csv_path, index=False)
    else:
        data = pd.read_csv(csv_path)
    return data