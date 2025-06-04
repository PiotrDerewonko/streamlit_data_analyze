import os
from datetime import datetime

import pandas as pd

from logger import get_logger
from pages.ma_details_files.download_data.data_about_people import download_data_about_people
from pages.main_diractor.download_data_main import DownloadDataMain

logger = get_logger('charakterystyka_bazy')


class DataAboutDonors(DownloadDataMain):
    """Klasa generuje dane na temat charakterystyki korespondentów. Dane sa wykorzystywane później w raporcie."""

    def loop_in_years(self) -> pd.DataFrame:
        """Metoda dopisuje do każdego korespondenta, w poszczególnych latach, w poszczególnych kampaniach ile miał lat"""
        data_all = pd.DataFrame()
        rok_biezacy = datetime.now().year
        for i in range(2008, rok_biezacy + 1):
            if i == rok_biezacy:
                campaign_group_list = [12, 11, 67, 10, 9, 24]
                for j in campaign_group_list:
                    data_tmp = self.get_data_from_sql_with_replace('sql_queries/6/age.sql',
                                                                   {'#A#': str(i),
                                                                    "action_group_two_id = 12": f"action_group_two_id = {j}"})
                    if data_tmp is not None:
                        self.logger.info(f'Podmieniam kampanię na {j}')
                        data_all = pd.concat([data_all, data_tmp])
                        break
            else:
                data_tmp = self.get_data_from_sql_with_replace('sql_queries/6/age.sql',
                                                               {'#A#': str(i)})
                data_all = pd.concat([data_all, data_tmp])
        return data_all


def generate_data_about_donor(con, engine, test_mode=False) -> None:
    """Funkcja tworzy obiekt klasy, który generuje dane na temat charakterystyki korespondentów. """
    logger.info('Generating data about donors')
    try:
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_files/data.csv'))
        donor_generator = DataAboutDonors(con, engine, test_mode=test_mode, table_name=csv_path, logger=logger)
        logger.info('Pętla w latach')
        data_about_age = donor_generator.loop_in_years()
        data_about_people = download_data_about_people(con, engine, test_mode=test_mode)
        data_about_people_short = data_about_people[['id_korespondenta', 'rok_dodania']]
        data_to_return = donor_generator.merge_data(data_about_age, [data_about_people_short], 'id_korespondenta')
        logger.info('Zapis danych')
        donor_generator.insert_data(data_to_return)
    except Exception as e:
        logger.error('Error generating data about donors')
        logger.error(e)

def download_data_about_donor(con, engine, test_mode=False) -> pd.DataFrame:
    """Funkcja tworzy obiekt klasy, który generuje dane na temat charakterystyki korespondentów. """
    logger.info('Download data about donors')
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_files/data.csv'))
    donor_generator = DataAboutDonors(con, engine, test_mode=test_mode, table_name=csv_path, logger=logger)
    data_to_return = donor_generator.download_data()
    return data_to_return