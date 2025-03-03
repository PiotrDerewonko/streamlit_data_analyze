import pandas as pd

from pages.main_diractor.download_data_main import DownloadDataMain


def generate_data_main_increase(con, engine, test_mode=False) -> None:
    """Funkcja wywołuję klasę, która generuje dane do raportu z pozyskanych korespondentów i dodaje ją do bazy"""
    increase_data = DownloadDataMain(con, engine, 'dash_increase_data', test_mode=test_mode)
    last_mailng = increase_data.get_data_from_sql_with_out_limit('sql_queries/1_main/last_mailing.sql')
    dict_to_replace = {'{default_camp}': last_mailng['grupa_akcji_2'].iloc[0],
                       '{default_year}': last_mailng['grupa_akcji_3'].iloc[0]}
    data_increase_peaople = increase_data.get_data_from_sql_with_replace(
        'sql_queries/1_main/increase_correspondents.sql', dict_to_replace)
    increase_data.insert_data(data_increase_peaople)

def download_data_main_increase(con, engine) -> pd.DataFrame:
    increase_data = DownloadDataMain(con, engine, 'dash_increase_data')
    data_to_return = increase_data.download_data()
    return data_to_return


