import os.path
import pandas as pd
from pages.main_diractor.download_data_main import DownloadDataMain


class DownloadDataForIntentionCharts(DownloadDataMain):
    """Klasa generuje dane potrzebne do raportów z wpłat i przesłanych intencji."""


def generate_data_for_intention_report_money(con, engine, test_mode=False) -> None:
    """Funkcje tworzy obiekt klasy, która generuje dane potrzebne do raportu z intencji."""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp_files/money_intentions.csv"))
    intention_report_generator = DownloadDataForIntentionCharts(con, engine, csv_path, test_mode=test_mode)
    data_from_generator = intention_report_generator.get_data_from_sql('sql_queries/9_intention/money_intentions.sql')
    intention_report_generator.insert_data(data_from_generator)

def download_data_for_intention_report_money(con, engine, test_mode=False) -> pd.DataFrame:
    """Funkcje tworzy obiekt klasy, która pobiera dane potrzebne do raportu z intencji."""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp_files/money_intentions.csv"))
    intention_report_downloader = DownloadDataForIntentionCharts(con, engine, csv_path, test_mode=test_mode)
    data_to_return = intention_report_downloader.download_data()
    return data_to_return

def generate_data_for_intention_report_count(con, engine, test_mode=False) -> None:
    """Funkcje tworzy obiekt klasy, która generuje dane potrzebne do raportu z intencji."""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp_files/count_intentions.csv"))
    intention_report_generator = DownloadDataForIntentionCharts(con, engine, csv_path, test_mode=test_mode)
    data_from_generator = intention_report_generator.get_data_from_sql('sql_queries/9_intention/count_intention.sql')
    intention_report_generator.insert_data(data_from_generator)

def download_data_for_intention_report_count(con, engine, test_mode=False) -> pd.DataFrame:
    """Funkcje tworzy obiekt klasy, która pobiera dane potrzebne do raportu z intencji."""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp_files/count_intentions.csv"))
    intention_report_downloader = DownloadDataForIntentionCharts(con, engine, csv_path, test_mode=test_mode)
    data_to_return = intention_report_downloader.download_data()
    return data_to_return


