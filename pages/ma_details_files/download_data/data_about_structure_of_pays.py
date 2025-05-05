from pages.main_diractor.download_data_main import DownloadDataMain
import pandas as pd
import os


class DataAboutStructureOfPays(DownloadDataMain):
    """Klasa generuje dane na temat struktury wpłat z mailingów adresowych."""

    @staticmethod
    def add_bins(data) -> pd.DataFrame:
        """Metoda dodaje przedziały wpłat dla wpłat z mailingów adresowych."""
        bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 200, 10000000]
        labels = ['[00-010)', '[010-020)', '[020-030)', '[030-040)', '[040-050)', '[050-060)', '[060-070)', '[070-080)',
                  '[080-090)',
                  '[090-100)', '[100-110)', '[110-120)', '[120-200)', '[200-maks)']
        data['przedzialy'] = pd.cut(data['suma_wplat'], bins, right=False, labels=labels)
        return data


def generate_data_about_structure_of_pays(con, engine, test_mode=False) -> None:
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    csv_path = csv_path + '/tmp_file/people_camp_pay_individual.csv'
    structure_of_pays = DataAboutStructureOfPays(con, engine, csv_path, test_mode=test_mode)
    data_to_analyze = structure_of_pays.get_data_from_sql('sql_queries/2_ma_detail/paymant_from_mailing.sql')
    data_to_analyze = structure_of_pays.add_bins(data_to_analyze)
    structure_of_pays.insert_data(data_to_analyze)

def download_data_about_structure_of_pays(con, engine, test_mode=False) -> pd.DataFrame:
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    csv_path = csv_path + '/tmp_file/people_camp_pay_individual.csv'
    structure_of_pays = DataAboutStructureOfPays(con, engine, csv_path, test_mode=test_mode)
    data_to_analyze = structure_of_pays.download_data()
    return data_to_analyze