import os
from datetime import datetime

import pandas as pd


def add_age_and_vip(data, _con) -> pd.DataFrame:
    year_now = datetime.now().year
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     '../.././sql_queries/2_ma_detail/age.sql'))
    with open(sql_file_path, 'r') as sql_file:
        age_sql = sql_file.read()

    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     '../.././sql_queries/2_ma_detail/is_vip_for_year.sql'))
    with open(sql_file_path, 'r') as sql_file:
        vip_sql = sql_file.read()


    data['przedzial_wieku'] = ''
    data['vip'] = ''
    data.set_index(['id_korespondenta', 'grupa_akcji_3_wysylki'], inplace=True)

    for k in range(2009, year_now + 1):
        age_sql_copy = age_sql.replace('#A#', str(k))
        vip_sql_copy = vip_sql.replace('#A#', str(k))
        vip_sql_copy = vip_sql_copy.replace('#B#', str(k - 1))
        age_data = pd.read_sql_query(age_sql_copy, _con)
        vip_data = pd.read_sql_query(vip_sql_copy, _con)
        age_data.set_index(['id_korespondenta', 'rok'], inplace=True)
        vip_data.set_index(['id_korespondenta', 'rok'], inplace=True)
        data.update(age_data)
        data.update(vip_data)

    data.reset_index(inplace=True)

    return data
