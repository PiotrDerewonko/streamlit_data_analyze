import os

import pandas as pd

from logger import get_logger
from pages.flow.download_data import download_data_wrong_address
from pages.ma_details_files.download_data.data_about_people import download_data_about_people
from pages.ma_details_files.download_data.data_about_people_in_campaign import download_data_about_people_in_campaign
from pages.main_diractor.download_data_main import DownloadDataMain

logger = get_logger('flow_all_data')


class DataAboutFlow(DownloadDataMain):
    """Klasa generuje dane potrzebne do wykresu z przepływów"""

    @staticmethod
    def add_others_address(df, year, df_people):
        """Funkcja dodaje wszystkich korespondentow ktorzy byli w bazie danych w przekazanym roku lub wcześniej. Następnie
        usuwa duplikaty na bazie roku i id_korespondenta zachowując pierwotne wartości, a usuwając dodane. W efekcie
        uzyskujemy listę wszystkich korespondentów na dany rok"""
        people_by_year = df_people.loc[df_people.data_dodania <= (str(year) + '12-31')]
        people_by_year['grupa_akcji_3_wysylki'] = year
        people_by_year['TYP DARCZYŃCY'] = 'odcięci'
        df = pd.concat([df, people_by_year])
        df = df.drop_duplicates(subset=['id_korespondenta', 'grupa_akcji_3_wysylki'], keep='first')
        return df

    def add_cut_and_wrong_address(self, df, max_year, df_people):
        for i in range(2008, max_year + 1):
            df = self.add_wrong_address(df, i, df_people)
            df = self.add_others_address(df, i, df_people)
            df = self.update_new_people(df, i, df_people)
        return df

    def add_wrong_address(self, df, year, df_people):
        """Metoda pobiera dane o błędnych adresach, odfiltrowuje tylko te adresy, które zostały zablokowane w przekazanym
        roku lub wcześniej. Następnie dodaje te dane do pliku głównego,i usuwa duplikaty. Jeśli w danym roku
        korespondent otrzymał choć jeden mailing, ale przeszedł, też zwrot to w finalnym pliku będzie info tylko o typie
        z mailingu. Jeśli w danym roku korespondent nie dostał żadnego mailingu, a co za tym idzie, nie ma przypisanego typu,
        zostanie mu dopisany typ zwrot."""
        data_wrong_address = download_data_wrong_address(self.con, self.engine, self.test_mode)
        data_wrong_address = data_wrong_address.loc[data_wrong_address['blocked_at'] <= f'{year}-12-31']
        data_wrong_address = data_wrong_address.rename(columns={'correspondent_id': 'id_korespondenta'})
        data_wrong_address = data_wrong_address[['id_korespondenta']].drop_duplicates()  # Zostaw DataFrame
        people_by_year = df_people.loc[df_people.id_korespondenta.isin(data_wrong_address['id_korespondenta'])]
        people_by_year['grupa_akcji_3_wysylki'] = year
        people_by_year['TYP DARCZYŃCY'] = 'zwrot'
        df = pd.concat([df, people_by_year])
        df = df.drop_duplicates(subset=['id_korespondenta', 'grupa_akcji_3_wysylki'], keep='first')
        return df

    @staticmethod
    def update_new_people(df, year, df_people):
        """Metoda odfiltrowuje ludzie, którzy w roku swojego wejścia mają status odcięci, i sprawdza czy, w kolejnym roku
        mają status < 3 lata. Jeśli tak, podmienia im typ w roku wejścia."""
        data_new_cut = df.loc[(df['TYP DARCZYŃCY'] == 'odcięci') & (df['grupa_akcji_3_wysylki'] == year) &
                              (df['rok_dodania'] == year)]
        data_new_next_year = df_people.loc[
            (df['grupa_akcji_3_wysylki'] == year + 1) & (df['TYP DARCZYŃCY'] == '<3 lata w bazie')]
        data_to_update = data_new_cut.loc[data_new_cut.id_korespondenta.isin(data_new_next_year.id_korespondenta)]
        data_to_update = data_to_update.loc[data_to_update['TYP DARCZYŃCY'] == '<3 lata w bazie']
        df.loc[df.id_korespondenta.isin(data_to_update.id_korespondenta)] = '<3 lata w bazie'
        return df


def generate_data_about_flow(con, engine, test_mode=False, logger=logger) -> None:
    """Funkcja tworzy obiekt klasy, która generuje dane na temat przepływów."""
    logger.info('Generuje dane data about flow')
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_files/data_all.csv'))
    data_flow_generator = DataAboutFlow(con, engine, csv_path, test_mode)
    logger.info('Pobieram dane na temat ludzi w kampaniach')
    data_about_people_in_campaign = download_data_about_people_in_campaign(con, engine, test_mode)
    logger.info('Pobieram dane na temat ludzi')
    data_about_people = download_data_about_people(con, engine, test_mode)

    # fitruje i sortuje dane
    data_about_people_in_campaign_short = data_about_people_in_campaign[
        ['id_korespondenta', 'grupa_akcji_3_wysylki', 'TYP DARCZYŃCY']].drop_duplicates()
    data_about_people = data_about_people.sort_values(by=['id_korespondenta'])

    data_all = pd.merge(data_about_people_in_campaign_short, data_about_people, how='left', on=['id_korespondenta'])

    try:
        max_year = int(str(data_about_people['data_dodania'].dropna().max())[:4])
    except ValueError as e:
        logger.error('Nie znaleziono danych o roku')
        max_year = 2025

    logger.info('Dodaje adresy poprawne, niepoprawne i nowe')
    data_fin = data_flow_generator.add_cut_and_wrong_address(data_all, max_year, data_about_people)

    logger.info('Zapisuje dane')
    data_flow_generator.insert_data(data_fin)


def download_data_about_flow(con, engine, test_mode=False, logger=logger) -> pd.DataFrame:
    """Funkcja tworzy obiekt klasy która pobiera dane na temat przepływów"""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_files/data_all.csv'))
    data_flow_generator = DataAboutFlow(con, engine, csv_path, test_mode)
    data_to_return = data_flow_generator.download_data()
    return data_to_return
