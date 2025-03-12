import os

import pandas as pd

from pages.main_diractor.download_data_main import DownloadDataMain


def generate_data_about_pay_in_campaign(con, engine, test_mode=False) -> None:
    """Funkcja tworzy obiekt klasy, który generuje dane na temat wpłat z mailingu."""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    csv_path = csv_path + '/tmp_file/people_camp_pay.csv'
    about_pay_in_campaign = DownloadDataMain(con, engine, csv_path, test_mode)
    data_to_analyze = about_pay_in_campaign.get_data_from_sql('sql_queries/2_ma_detail/payment_from_mailingv2.sql')
    about_pay_in_campaign.insert_data(data_to_analyze)

def download_data_about_pay_in_campaign(con, engine, test_mode=False) -> pd.DataFrame:
    """Funkcja tworzy obiekt klasy, który pobiera dane na temat wpłat z mailingu."""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    csv_path = csv_path + '/tmp_file/people_camp_pay.csv'
    about_pay_in_campaign = DownloadDataMain(con, engine, csv_path, test_mode)
    data_to_analyze = about_pay_in_campaign.download_data()
    return data_to_analyze
