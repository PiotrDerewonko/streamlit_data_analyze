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
        rok_biezacy = datetime.now().year
        for i in range(2008, rok_biezacy + 1):
            zapytanie_copy = copy.copy(zapytanie)
            zapytanie_copy = zapytanie_copy.replace("#A#", str(i))
            if i == rok_biezacy:
                try:
                    sql = f'''select max(action_group_two_id) as id_gr2 from fsaps_campaign_campaign
                    where action_group_three_id in 
                    (select id from fsaps_dictionary_action_group_three where text = '{rok_biezacy}')
                    and action_group_two_id in (9,10,11,12,24,67)'''
                    id_gr_2 = pd.read_sql_query(sql, con)
                    id_gr_2 = id_gr_2['id_gr2'].iloc[0]
                    zapytanie_copy = zapytanie_copy.replace("action_group_two_id = 12",
                                                            f"action_group_two_id = {id_gr_2}")
                except Exception:
                    print(f'Brak mailingow w roku {rok_biezacy}')
            data_tmp_2 = pd.read_sql_query(zapytanie_copy, con)
            data_tmp = pd.concat([data_tmp, data_tmp_2])
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..', 'ma_details_files/tmp_file/people.csv'))
        data_about_peaople = pd.read_csv(csv_path, index_col='Unnamed: 0',
                                     low_memory=False)
        data_about_peaople = data_about_peaople[['id_korespondenta', 'rok_dodania']]
        data_tmp = pd.merge(data_tmp, data_about_peaople, on='id_korespondenta', how='left')
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_files/data.csv'))
        data_tmp.to_csv(csv_path)

    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_files/data.csv'))
    data = pd.read_csv(csv_path)

    return data
