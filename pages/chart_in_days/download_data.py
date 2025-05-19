import os.path

import pandas as pd

from logger import get_logger
from pages.main_diractor.download_data_main import DownloadDataMain

logger = get_logger('wykresy w dniach szczegółowe')
class DownloadDataForChartInDays(DownloadDataMain):
    """Klasa generuje dane potrzebne do szczegółowego wykresu wpłat w dniach"""

    def loop_in_year_and_campaigns(self, list_of_id_gr2, list_of_id_gr3, data_final, sql_query):
        number_of_years = 0
        self.logger.info('Rozpoczynam pętle ')
        for j in list_of_id_gr3:
            for i in list_of_id_gr2:
                if number_of_years > 0:
                    dictionary_to_replace = {"#A#": str(i), "#B#": str(j),
                                             "#C#": str(list_of_id_gr3[number_of_years - 1])}
                else:
                    dictionary_to_replace = {"#A#": str(i), "#B#": str(j),
                                             "#C#": str(list_of_id_gr3[number_of_years])}
                data_tmp = self.get_data_from_sql_with_replace(sql_query, dictionary_to_replace)
                data_final = pd.concat([data_final, data_tmp])
            number_of_years += 1
            if self.test_mode & (number_of_years == 3):
                break

        return data_final


def generate_data_for_days_charts_income(con, engine, test_mode=False) -> None:
    """Metoda tworzy obiekt klasy, który generuje dane do raportu wpłat w dniach ze szczegółami."""
    try:
        logger.info('Rozpoczynam generowanie danych')
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_file/dash_char_ma_data_by_id.csv'))
        chart_income_generator = DownloadDataForChartInDays(con, engine, csv_path, test_mode=test_mode, logger=logger)
        data_action_group_two = chart_income_generator.get_data_from_sql_with_out_limit(
            'sql_queries/10_chart_in_days/action_two_id.sql')
        list_of_id_gr2 = data_action_group_two['id'].tolist()
        data_action_group_three = chart_income_generator.get_data_from_sql_with_out_limit(
            'sql_queries/10_chart_in_days/action_three_id.sql')
        list_of_id_gr3 = data_action_group_three['id'].tolist()
        data_to_analyze = pd.DataFrame()
        data_to_analyze = chart_income_generator.loop_in_year_and_campaigns(list_of_id_gr2, list_of_id_gr3, data_to_analyze,
                                                                            'sql_queries/10_chart_in_days/count_and_sum_amount_for_char_days.sql')
        data_to_analyze['dzien_po_mailingu'].fillna(999, inplace=True)
        data_to_analyze['dzien_po_mailingu'] = data_to_analyze['dzien_po_mailingu'].astype(int)
        chart_income_generator.insert_data(data_to_analyze)
    except Exception as e:
        logger.exception(f'Nieoczekiwany błąd : {e}')


def download_data_for_days_charts_income(con, engine, test_mode=False) -> pd.DataFrame:
    """Metoda tworzy obiekt klasy, który pobiera dane do raportu wpłat w dniach ze szczegółami."""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_file/dash_char_ma_data_by_id.csv'))
    chart_income_downloader = DownloadDataForChartInDays(con, engine, csv_path, test_mode=test_mode)
    data_to_return = chart_income_downloader.download_data()
    return data_to_return


def generate_data_for_days_charts_cost(con, engine, test_mode=False) -> None:
    """Metoda tworzy obiekt klasy, który generuje dane do raportu wpłat w dniach ze szczegółami."""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_file/dash_char_ma_data_cost_cir_by_id.csv'))
    chart_cost_generator = DownloadDataForChartInDays(con, engine, csv_path, test_mode=test_mode)
    data_action_group_two = chart_cost_generator.get_data_from_sql_with_out_limit(
        'sql_queries/10_chart_in_days/action_two_id.sql')
    list_of_id_gr2 = data_action_group_two['id'].tolist()
    data_action_group_three = chart_cost_generator.get_data_from_sql_with_out_limit(
        'sql_queries/10_chart_in_days/action_three_id.sql')
    list_of_id_gr3 = data_action_group_three['id'].tolist()
    data_to_analyze = pd.DataFrame()
    data_to_analyze = chart_cost_generator.loop_in_year_and_campaigns(list_of_id_gr2, list_of_id_gr3, data_to_analyze,
                                                                      'sql_queries/10_chart_in_days/cost_and_cirtulation_for_char_days.sql')
    data_to_analyze['dzien_po_mailingu'].fillna(999, inplace=True)
    data_to_analyze['dzien_po_mailingu'] = data_to_analyze['dzien_po_mailingu'].astype(int)
    chart_cost_generator.insert_data(data_to_analyze)


def download_data_for_days_charts_cost(con, engine, test_mode=False) -> pd.DataFrame:
    """Metoda tworzy obiekt klasy, który pobiera dane do raportu wpłat w dniach ze szczegółami."""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_file/dash_char_ma_data_cost_cir_by_id.csv'))
    chart_cost_downloader = DownloadDataForChartInDays(con, engine, csv_path, test_mode=test_mode)
    data_to_return = chart_cost_downloader.download_data()
    return data_to_return
