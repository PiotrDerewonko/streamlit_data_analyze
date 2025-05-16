import os
from logger import get_logger
from pages.main_diractor.download_data_main import DownloadDataMain
import pandas as pd

logger = get_logger('flow')


class DownloadDataAboutWrongAddress(DownloadDataMain):
    """Klasa pobiera dane na temat złych adresów korespondentów. Te dane wykorzystywane są w raporcie z przepływów."""


def generate_data_wrong_address(con, engine, test_mode=False) -> None:
    """Funkcja tworzy obiekt klasy, która generuje dane na temat niepoprawnych adresów potrzebne do raportu z przepływów"""
    try:
        logger.info('Rozpoczynam generowanie danych')
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_files/data_wrong_address.csv'))
        wrong_address_generator = DownloadDataAboutWrongAddress(con, engine, csv_path, test_mode=test_mode, logger=logger)
        logger.info('Zaczynam pobiera dane z pierwszej kwerendy')
        data_to_analyze = wrong_address_generator.get_data_from_sql('sql_queries/11_flow/wrong_address.sql')
        wrong_address_generator.insert_data(data_to_analyze)
        logger.info('Koniec przeładowania danych')
    except Exception as e:
        logger.error(f'Nieoczekiwany błąd {e}')


def download_data_wrong_address(con, engine, test_mode=False) -> pd.DataFrame:
    """Funkcja tworzy obiekt klasy, która pobiera dane na temat niepoprawnych adresów potrzebne do raportu z przepływów"""
    logger.info('Rozpoczynam pobieranie danych ')
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_files/data_wrong_address.csv'))
    wrong_address_downloader = DownloadDataAboutWrongAddress(con, engine, csv_path, test_mode=test_mode)
    data_to_return = wrong_address_downloader.download_data()
    return data_to_return

