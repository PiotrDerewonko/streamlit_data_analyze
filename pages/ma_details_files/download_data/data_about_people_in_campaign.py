import os

import pandas as pd

from functions_pandas.short_mailings_names import change_name
from pages.ma_details_files.data_about_peopla_year_and_vip import add_age_and_vip
from pages.main_diractor.download_data_main import DownloadDataMain


class DataAboutPeopleInCampaign(DownloadDataMain):
    """Klasa tworzy dane dotyczących korespondentów biorących udział w mailingach adresowych. Dane tu uzyskane
    są podstawą do wygenerowania raportu o efektywności mailingów adresowych w sekcji ma_details."""

    def prepare_data(self, data) -> pd.DataFrame:
        """Metoda wypełnia brakujące komórki, skraca nazwy mailingów oraz dodaje dane o wieku."""
        data['powod_otrzymania_giftu'].fillna('brak', inplace=True)
        data.fillna(0, inplace=True)
        data = change_name(data)
        data = add_age_and_vip(data, self.con)
        return data


def generate_data_about_people_in_campaign(con, engine, test_mode=False) -> None:
    """Funkcja tworzy klasę i generuje dane ludzi z mailingów adresowych do raportu."""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    csv_path = csv_path + '/tmp_file/people_camp.csv'
    data_about_people_in_campaign = DataAboutPeopleInCampaign(con, engine, csv_path, test_mode=test_mode)
    data_to_analyze = data_about_people_in_campaign.get_data_from_sql('sql_queries/2_ma_detail/people_camp_data.sql')
    data_to_analyze = data_about_people_in_campaign.prepare_data(data_to_analyze)
    data_about_people_in_campaign.insert_data(data_to_analyze)


def download_data_about_people_in_campaign(con, engine, test_mode=False) -> pd.DataFrame:
    """Funkcja pobiera dane o ludziach w mailingach adresowych do raportu."""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    csv_path = csv_path + '/tmp_file/people_camp.csv'
    data_about_people_in_campaign = DataAboutPeopleInCampaign(con, engine, csv_path, test_mode=test_mode)
    data_to_return = data_about_people_in_campaign.download_data()
    return data_to_return
