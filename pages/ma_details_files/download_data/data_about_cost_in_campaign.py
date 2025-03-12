import os
import pandas as pd
from pages.main_diractor.download_data_main import DownloadDataMain


class DataAboutCostInCampaign(DownloadDataMain):
    """Klasa generuje dane potrzebne do wyliczenia kosztów kampanii adresowych. Dane tu uzyskane są wykorzystywane
    do wyliczenia kosztów """

    @staticmethod
    def prepare_data(data) -> pd.DataFrame:
        """Metoda uzupełnia puste komórki w określonych kolumnach oraz oznacza rekordy z kosztami giftów."""
        list_to_fillna = ['koszt_wysylki_na_polske_bez_warszawy', 'koszt_wysylki_na_warszawe',
                          'koszt_wysylki_zagranica']
        for i in list_to_fillna:
            data[i] = data[i].fillna(0)
        data['final_post_cost'] = data['koszt_wysylki_na_polske_bez_warszawy'] + data['koszt_wysylki_na_warszawe'] + \
                                  data['koszt_wysylki_zagranica']
        data['if_gifts'] = 0
        data['if_gifts'].loc[data['koszt_giftow'] > 0] = 1
        return data


def generate_data_about_cost_in_campaign(con, engine, test_mode=False) -> None:
    """Funkcja generuje dane dotyczące kosztów mailingu adresowego"""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    csv_path = csv_path + '/tmp_file/camp_cost.csv'
    about_cost_in_campaign = DataAboutCostInCampaign(con, engine, csv_path, test_mode)
    data_to_analyze = about_cost_in_campaign.get_data_from_sql('sql_queries/2_ma_detail/big_cost.sql')
    data_to_analyze = about_cost_in_campaign.prepare_data(data_to_analyze)
    about_cost_in_campaign.insert_data(data_to_analyze)


def download_data_about_cost_in_campaign(con, engine, test_mode=False) -> pd.DataFrame:
    """Funkcja tworzy obiekt klasy, który pobiera dane na temat kosztów mailingu."""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    csv_path = csv_path + '/tmp_file/people_camp_pay.csv'
    about_cost_in_campaign = DataAboutCostInCampaign(con, engine, csv_path, test_mode)
    data_to_analyze = about_cost_in_campaign.download_data()
    return data_to_analyze
