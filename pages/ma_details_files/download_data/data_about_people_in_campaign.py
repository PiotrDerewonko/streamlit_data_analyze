import os
from datetime import datetime

import pandas as pd

from functions_pandas.short_mailings_names import change_name
from pages.ma_details_files.data_about_peopla_year_and_vip import add_age_and_vip
from pages.ma_details_files.download_data.data_about_people import download_data_about_people
from pages.main_diractor.download_data_main import DownloadDataMain


class DataAboutPeopleInCampaign(DownloadDataMain):
    """Klasa tworzy dane dotyczących korespondentów biorących udział w mailingach adresowych. Dane tu uzyskane
    są podstawą do wygenerowania raportu o efektywności mailingów adresowych w sekcji ma_details. Część danych tu
    zawartych odnosi się do momentu otrzymania mailingu (np. typ darczyńcy na dany rok kalendarzowy)"""

    def prepare_data(self, data) -> pd.DataFrame:
        """Metoda wypełnia brakujące komórki, skraca nazwy mailingów oraz dodaje dane o wieku."""
        data['powod_otrzymania_giftu'].fillna('brak', inplace=True)
        data.fillna(0, inplace=True)
        data = change_name(data)
        data = add_age_and_vip(data, self.con)
        return data

    def add_type_of_donor(self, people_camp) -> pd.DataFrame:
        """Metoda dodaje """
        rok = datetime.now().year
        liczba_lat = 3
        data_tmp_1 = download_data_about_people(self.con, self.engine, self.test_mode)
        people_camp['TYP DARCZYŃCY'] = 'pozostali'

        for year in range(2011, rok + 1):
            data_tmp_1[f'liczba_lat_placacych_do_{year}'] = 0
            data_tmp_1[f'laczna_liczba_wplat_do_{year}'] = 0
            for i in range(year - liczba_lat, year):
                data_tmp_1[f'liczba_lat_placacych_do_{year}'].loc[data_tmp_1[f'liczba_wplat_{i}'] >= 1] = \
                    data_tmp_1[f'liczba_lat_placacych_do_{year}'] + 1
                data_tmp_1[f'laczna_liczba_wplat_do_{year}'] = data_tmp_1[f'laczna_liczba_wplat_do_{year}'] + \
                                                               data_tmp_1[f'liczba_wplat_{i}']
            data_tmp_1[f'średnia_liczba_wplat_do_{year}'] = data_tmp_1[f'laczna_liczba_wplat_do_{year}'] / \
                                                            data_tmp_1[f'liczba_lat_placacych_do_{year}']

            data_tmp_1[f'TYP DARCZYŃCY NA {year}'] = 'pozostali'
            lojalni = data_tmp_1['id_korespondenta'].loc[(data_tmp_1[f'średnia_liczba_wplat_do_{year}'] >= 2) &
                                                         (data_tmp_1['rok_dodania'] <= year - liczba_lat) &
                                                         (data_tmp_1[f'liczba_lat_placacych_do_{year}'] == 3)]
            people_camp['TYP DARCZYŃCY'].loc[(people_camp['grupa_akcji_3_wysylki'] == year) &
                                             (people_camp['id_korespondenta'].isin(lojalni))] = 'lojalny'

            systematyczni = data_tmp_1['id_korespondenta'].loc[(data_tmp_1[f'średnia_liczba_wplat_do_{year}'] < 2) &
                                                               (data_tmp_1[
                                                                    f'średnia_liczba_wplat_do_{year}'] >= 1) &
                                                               (data_tmp_1['rok_dodania'] <= year - liczba_lat) &
                                                               (data_tmp_1[f'liczba_lat_placacych_do_{year}'] == 3)]
            people_camp['TYP DARCZYŃCY'].loc[(people_camp['grupa_akcji_3_wysylki'] == year) &
                                             (people_camp['id_korespondenta'].isin(
                                                 systematyczni))] = 'systematyczny'

            nowi = data_tmp_1['id_korespondenta'].loc[
                (data_tmp_1['rok_dodania'] >= year - liczba_lat + 1) & (data_tmp_1['rok_dodania'] <= year)]
            people_camp['TYP DARCZYŃCY'].loc[(people_camp['grupa_akcji_3_wysylki'] == year) &
                                             (people_camp['id_korespondenta'].isin(nowi))] = '<3 lata w bazie'

        # dodaje wszystkim z 3 pierwszych lat niej niz 3 lata w bazie
        people_camp['TYP DARCZYŃCY'].loc[(people_camp['grupa_akcji_3_wysylki'] == 2008)] = '<3 lata w bazie'
        people_camp['TYP DARCZYŃCY'].loc[(people_camp['grupa_akcji_3_wysylki'] == 2009)] = '<3 lata w bazie'
        people_camp['TYP DARCZYŃCY'].loc[(people_camp['grupa_akcji_3_wysylki'] == 2010)] = '<3 lata w bazie'

        return people_camp

def generate_data_about_people_in_campaign(con, engine, test_mode=False) -> None:
    """Funkcja tworzy klasę i generuje dane ludzi z mailingów adresowych do raportu."""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    csv_path = csv_path + '/tmp_file/people_camp.csv'
    data_about_people_in_campaign = DataAboutPeopleInCampaign(con, engine, csv_path, test_mode=test_mode)
    data_to_analyze = data_about_people_in_campaign.get_data_from_sql('sql_queries/2_ma_detail/people_camp_data.sql')
    data_to_analyze = data_about_people_in_campaign.prepare_data(data_to_analyze)
    data_to_analyze_with_types = data_about_people_in_campaign.add_type_of_donor(data_to_analyze)
    data_about_people_in_campaign.insert_data(data_to_analyze_with_types)


def download_data_about_people_in_campaign(con, engine, test_mode=False) -> pd.DataFrame:
    """Funkcja pobiera dane o ludziach w mailingach adresowych do raportu."""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    csv_path = csv_path + '/tmp_file/people_camp.csv'
    data_about_people_in_campaign = DataAboutPeopleInCampaign(con, engine, csv_path, test_mode=test_mode)
    data_to_return = data_about_people_in_campaign.download_data()
    return data_to_return
