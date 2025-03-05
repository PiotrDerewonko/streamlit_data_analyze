import os

import pandas as pd

from pages.main_diractor.download_data_main import DownloadDataMain


class DownloadDataDistance(DownloadDataMain):
    """Klasa nadbudowuje do przekazanej klasy bazowej, metody odpowiedzialne, za wyliczenia danych do raportu."""

    @staticmethod
    def setup_data(data) -> pd.DataFrame:
        """Metoda ustawia określone kolumny na typ datetime"""
        list_to_change_type = ['second_pay', 'first_pay', 'data_dodania']
        for i in list_to_change_type:
            data[f'{i}'] = pd.to_datetime(data[f'{i}'])
        return data

    @staticmethod
    def check_first_pay(data) -> pd.DataFrame:
        """Metoda sprawdza, odległość między pierwszą wpłatą i datą dodania."""
        data['distance_add_to_fp'] = (data['first_pay'] - data['data_dodania']).dt.days
        data['distance_add_to_fp'].loc[data['distance_add_to_fp'] < 0] = 0
        data['distance_add_to_fp'].fillna(99999, inplace=True)
        data['status_first_pay'] = ''
        data['status_first_pay'].loc[data['distance_add_to_fp'] < 99999] = 'Dokonał pierwszej wpłaty'
        data['status_first_pay'].loc[data['distance_add_to_fp'] == 99999] = 'Brak pierwszej wpłaty'
        return data

    @staticmethod
    def check_second_pay(data) -> pd.DataFrame:
        """Metoda sprawdza, czy była druga wpłata, i jeśli tak, to jaka jest odległość między nimi"""
        data['distance_fp_to_sp'] = (data['second_pay'] - data['first_pay']).dt.days
        data['distance_fp_to_sp'].fillna(99999, inplace=True)
        data['status_second_pay'] = ''
        compartment = [(0, 180, '1) do pół roku'), (180, 365, '2) od pół roku do roku'),
                       (365, 730, '3) miedzy 1 a drugim rokiem'),
                       (730, 99998, '4) powyżej dwóch lat')]
        for i in compartment:
            data['status_second_pay'].loc[(data['distance_fp_to_sp'] >= i[0]) &
                                          (data['distance_fp_to_sp'] <= i[1])] = f'{i[2]}'
        data['status_second_pay'].loc[data['status_second_pay'] == ''] = 'Nie ponowił wpłaty'
        return data

    @staticmethod
    def app_data_to_pay_data(data) -> pd.DataFrame:
        """Metoda określa daty pierwszej i drugiej wpłaty"""
        tmp = data['id_korespondenta'].drop_duplicates().to_frame()
        tmp2 = data.loc[data['numer'] == 1]
        tmp2 = tmp2.rename(columns={'data_wplywu_srodkow': 'first_pay'})
        tmp = tmp.merge(tmp2, on='id_korespondenta', how='left')
        tmp2 = data.loc[data['numer'] == 2]
        tmp2 = tmp2.rename(columns={'data_wplywu_srodkow': 'second_pay'})
        tmp = tmp.merge(tmp2, on='id_korespondenta', how='left')
        return tmp


def generate_data_distance_first_nad_second_pay(con, engine, test_mode=False):
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    csv_path = csv_path + '/tmp_files/data_distance.csv'
    data_distance = DownloadDataDistance(con, engine, csv_path,
                                         test_mode=test_mode)
    last_mailing = data_distance.get_data_from_sql_with_out_limit('sql_queries/1_main/last_mailing.sql')
    dict_to_replace = {'{default_camp}': last_mailing['grupa_akcji_2'].iloc[0],
                       '{default_year}': last_mailing['grupa_akcji_3'].iloc[0]}
    data_about_corr = data_distance.get_data_from_sql_with_replace(
        'sql_queries/3_distance_1_and_second_pay/data_about_correspondents.sql', dict_to_replace)
    data_about_pay = data_distance.get_data_from_sql('sql_queries/3_distance_1_and_second_pay/data_about_pay.sql')
    data_about_pay = data_distance.app_data_to_pay_data(data_about_pay)
    data_all = data_distance.merge_data(data_about_corr, [data_about_pay], 'id_korespondenta')
    data_all = data_distance.setup_data(data_all)
    data_all = data_distance.check_first_pay(data_all)
    data_all = data_distance.check_second_pay(data_all)
    data_distance.insert_data(data_all)

def download_data_distance_first_nad_second_pay(con, engine, test_mode=False) -> pd.DataFrame:
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    csv_path = csv_path + '/tmp_files/data_distance.csv'
    data_distance = DownloadDataDistance(con, engine, csv_path,
                                         test_mode=test_mode)
    data_to_return = data_distance.download_data()
    return data_to_return


