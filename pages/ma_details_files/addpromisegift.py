import os

import pandas as pd


def promise_gift():
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'promise.xlsx'))
    data_promise = pd.read_excel(csv_path, sheet_name='Arkusz1')
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_file/people_camp.csv'))
    data = pd.read_csv(csv_path, index_col='Unnamed: 0')

    data_fin = pd.merge(data, data_promise, on=['grupa_akcji_2_wysylki', 'grupa_akcji_3_wysylki'],
                         how='left')
    data_fin['Obiecany gift'].fillna('brak', inplace=True)
    data_fin['Rodzaj giftu'].fillna('brak', inplace=True)
    data_fin.to_csv(csv_path)