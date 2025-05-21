import datetime
import os
from typing import NamedTuple, Optional, Any

import pandas as pd

from logger import get_logger
from pages.main_diractor.download_data_main import DownloadDataMain

logger = get_logger('people')


class SqlQuerySpec(NamedTuple):
    query: str
    column_name: Optional[str] = None
    fillna_value: Optional[Any] = None


class DataAboutPeopleDownloader(DownloadDataMain):
    """Klasa generuje dane na temat korespondentów, niezależnie od tego, w jakich kampaniach brali udział."""

    def add_many_sql(self, data) -> pd.DataFrame:
        """Metoda dodaje do przekazanych danych, wyniki z zapytań sql"""
        sql_list = [SqlQuerySpec('sql_queries/2_ma_detail/people_source.sql', None, None),
                    SqlQuerySpec('sql_queries/2_ma_detail/origin_material.sql', None, None),
                    SqlQuerySpec('sql_queries/2_ma_detail/is_in_rosary.sql', 'modlitwa_rozancowa',
                                 'nie jest \nw modlitwie różańcowej'),
                    SqlQuerySpec('sql_queries/2_ma_detail/chosen_city.sql', 'typ_miejscowosci', 'pozostałe'),
                    SqlQuerySpec('sql_queries/2_ma_detail/postal_districts.sql', 'okreg_pocztowy', 'brak'),
                    SqlQuerySpec('sql_queries/2_ma_detail/how_many_rosary_have.sql', 'ilosc_dziesiatek', 'nie ma \nżadnej dziesiątki'),
                    ]
        logger.info('Rozpoczynam dodawanie wielu kwerend do korespondentów')
        for spec in sql_list:
            data_tmp = self.get_data_from_sql(spec.query)
            if data_tmp is not None:
                data = pd.merge(data, data_tmp, how='left', on='id_korespondenta')
                if spec.column_name is not None:
                    data[f'{spec.column_name}'] = data[f'{spec.column_name}'].fillna(spec.fillna_value)
        data['rodzaj_materialu_pozyskania'].loc[~(data['grupa_akcji_1_dodania'] == 'DRUKI BEZADRESOWE')] = 'brak'
        data['material_pozyskania'].loc[~(data['grupa_akcji_1_dodania'] == 'DRUKI BEZADRESOWE')] = 'brak'
        logger.info('Zakończono dodawanie wielu kwerend do korespondentów')
        return data

    def add_data_about_materials(self, data) -> pd.DataFrame:
        """Metoda dodaje informacje na temat posiadanych giftów przez korespondenta."""
        data_of_products = self.get_data_from_sql('sql_queries/2_ma_detail/list_of_products.sql')
        for i, j in data_of_products.iterrows():
            logger.info(f"""Sprawdzam materiał {j['nazwa_materiału']}""")
            data_tmp = self.get_data_from_sql_with_replace('sql_queries/2_ma_detail/is_correspondent_has_product.sql',
                                                           {'#A#': j['nazwa_materiału']})
            if data_tmp is not None:
                data = pd.merge(data, data_tmp, how='left', on='id_korespondenta')
                data[f"""{j['nazwa_materiału']}"""] = data[f"""{j['nazwa_materiału']}"""].fillna(
                    f"""nie posiada {j['nazwa_materiału']}""")

        return data

    def add_count_of_pay_by_year(self, data) -> pd.DataFrame:
        """Metoda dodaje informacje na temat wpłat korespondentów w poszczególnych latach."""
        year = datetime.datetime.now().year
        logger.info('Rozpoczynam dodawanie liczby wpłat w poszczególnych latach')
        for i in range(2008, year + 1):
            logger.info(f'Dane za rok {i}')
            data_tmp = self.get_data_from_sql_with_replace('sql_queries/2_ma_detail/count_of_pays_in_year.sql',
                                                           {'#A#': str(i)})
            data = pd.merge(data, data_tmp, how='left', on='id_korespondenta')
            data[f'liczba_wplat_{i}'].fillna(0, inplace=True)
        return data


def generate_data_about_people(con, engine, test_mode=False) -> None:
    """Metoda tworzy obiekt klasy, który generuje dane na temat korespondentów. Dane wykorzystywane są w raporcie
    z mailingów adresowych."""
    try:
        logger.info('Zaczynam generowanie danych na temat ludzi')
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        csv_path = os.path.join(csv_path, 'tmp_file/data_about_people.csv')
        people_generator = DataAboutPeopleDownloader(con, engine, table_name=csv_path, test_mode=test_mode,
                                                     logger=logger)
        all_people = people_generator.get_data_from_sql('sql_queries/2_ma_detail/all_people.sql')
        all_people_with_extra_sql = people_generator.add_many_sql(all_people)
        all_people_with_extra_sql_and_count_in_years = people_generator.add_count_of_pay_by_year(
            all_people_with_extra_sql)
        all_people_with_materials = people_generator.add_data_about_materials(
            all_people_with_extra_sql_and_count_in_years)
        people_generator.insert_data(all_people_with_materials)
    except Exception as e:
        logger.error(f'Nie oczekiwany błąd: {e}')

def download_data_about_people(con, engine, test_mode=False) -> pd.DataFrame:
    """Metoda tworzy obiekt klasy, który pobiera dane na temat korespondentów. Dane wykorzystywane są w raporcie
    z mailingów adresowych."""
    try:
        logger.info('Zaczynam pobieranie danych na temat ludzi')
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        csv_path = os.path.join(csv_path, 'tmp_file/data_about_people.csv')
        people_downloader = DataAboutPeopleDownloader(con, engine, table_name=csv_path, test_mode=test_mode,
                                                     logger=logger)
        data_to_return = people_downloader.download_data()
        return data_to_return

    except Exception as e:
        logger.error(f'Nie oczekiwany błąd: {e}')