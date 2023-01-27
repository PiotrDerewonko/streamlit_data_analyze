import pandas as pd

def promise_gift():
    data_promise = pd.read_excel('./pages/ma_details_files/promise.xlsx', sheet_name='Arkusz1')
    data = pd.read_csv('./pages/ma_details_files/tmp_file/people_camp.csv', index_col='Unnamed: 0')

    data_fin = pd.merge(data, data_promise, on=['grupa_akcji_2_wysylki', 'grupa_akcji_3_wysylki'],
                         how='left')
    data_fin['Obiecany gift'].fillna('brak', inplace=True)
    data_fin['Rodzaj giftu'].fillna('brak', inplace=True)
    data_fin.to_csv('./pages/ma_details_files/tmp_file/people_camp.csv')