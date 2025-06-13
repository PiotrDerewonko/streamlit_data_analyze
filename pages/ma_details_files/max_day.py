import os

import pandas as pd


def check_max_day(refresh_data):
    if refresh_data == 'True':
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_file/people_camp_pay.csv'))
        data = pd.read_csv(csv_path, index_col='Unnamed: 0')
        tmp_df = pd.DataFrame()
        tmp_year = data['grupa_akcji_3_wplaty'].drop_duplicates()
        tmp_q = data['grupa_akcji_2_wplaty'].drop_duplicates()
        index = 0
        for i1, row1 in tmp_year.items():
            for i2, row2 in tmp_q.items():
                tmp = data.loc[(data['grupa_akcji_2_wplaty'] == row2) & (data['grupa_akcji_3_wplaty'] == row1)]
                tmp2 = tmp['dzien_po_mailingu'].max()
                # tmp_df2 = pd.DataFrame(data = (row2, row1, tmp2), columns=['grupa_akcji_2_wplaty', 'grupa_akcji_3_wplaty', 'dzien_po_nadaniu'])
                tmp_df2 = pd.DataFrame(
                    data={'grupa_akcji_2_wplaty': row2, 'grupa_akcji_3_wplaty': row1, 'dzien_po_mailingu': tmp2},
                    index=[index])
                index += 1

                tmp_df = pd.concat([tmp_df, tmp_df2])
        tmp_df.dropna(inplace=True)
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_file/days.xlsx'))
        tmp_df.to_excel(csv_path)
        print('zakonczono sprawdzanie dat')
