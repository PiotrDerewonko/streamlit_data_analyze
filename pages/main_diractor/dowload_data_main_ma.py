import pandas as pd

from pages.main_diractor.download_data_main import DownloadDataMain


def generate_data_main_ma(con, engine, test_mode=False) -> None:
    """Funkcja wywołuje klasę, która generuje dane do raportu z mailingów adresowych z zakładki main."""
    ma_data = DownloadDataMain(con, engine, 'dash_ma_data', test_mode=test_mode)
    data_ma_amount = ma_data.get_data_from_sql('sql_queries/1_main/ma_campaign.sql')
    data_ma_cost = ma_data.get_data_from_sql('sql_queries/1_main/cost_campaign.sql')
    list_to_merge = [data_ma_cost]
    data_all = ma_data.merge_data(data_ma_amount, list_to_merge, 'kod_akcji')
    ma_data.insert_data(data_all)

def download_data_main_ma(con, engine, test_mode=False) -> pd.DataFrame:
    """Funkcja zwraca dane do raportu z mailingów adresowych."""
    ma_data = DownloadDataMain(con, engine, 'dash_ma_data', test_mode=test_mode)
    data_to_return = ma_data.download_data()
    return data_to_return