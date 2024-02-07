import copy
import os
from datetime import datetime

import pandas as pd


def download_data_about_age(con, refresh, engine) -> pd.DataFrame:
    if refresh == 'True':
        sql_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         '../.././sql_queries/6/age.sql'))
        with open(sql_file_path, 'r') as sql_file:
            zapytanie = sql_file.read()
        data_tmp = pd.DataFrame()
        for i in range(2008, datetime.now().year + 1):
            zapytanie_copy = copy.copy(zapytanie)
            zapytanie_copy = zapytanie_copy.replace("#A#", str(i))
            data_tmp_2 = pd.read_sql_query(zapytanie_copy, con)
            data_tmp = pd.concat([data_tmp, data_tmp_2])
        data_tmp.to_sql(schema='raporty', con=engine, if_exists='replace', name='age_in_years', index=False)

    data = pd.read_sql_query('''select * from raporty.age_in_years''', con)

    return data
