import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

from logger import get_logger
from database.read_file_sql import read_file_sql

logger = get_logger()


class DownloadDataMain:
    def __init__(self, con, engine, table_name, test_mode=False, logger=None) -> None:
        self.con = con
        self.engine = engine
        self.table_name = table_name
        self.test_mode = test_mode
        self.logger = logger

    def get_data_from_sql(self, file_name: str) -> pd.DataFrame:
        """Metoda pobiera dane dotyczące wpływów z mailingów."""
        if self.logger:
            self.logger.info(f'rozpoczynam pobierania danych z pliku {file_name}')
        try:
            sql = read_file_sql(file_name)
        except FileNotFoundError:
            if self.logger:
                self.logger.info(f'File {file_name} not found')
            raise
        if self.test_mode:
            sql += ' limit 50'
        try:
            data = pd.read_sql(sql, con=self.con)
        except pd.errors.DatabaseError as e:
            if self.logger:
                self.logger.exception(f'Blad rzy pliku sql: {file_name} treść błędu {e}')
            raise
        if self.logger:
            self.logger.info(f'pobrano dane z {file_name}')
        return data

    def get_data_from_sql_with_out_limit(self, file_name) -> pd.DataFrame:
        """Metoda pobiera dane dotyczące wpływów z mailingów."""
        sql = read_file_sql(file_name)
        data = pd.read_sql(sql, con=self.con)
        print(f'pobrano dane z {file_name}')
        return data

    def get_data_from_sql_with_replace(self, file_name, dictionary) -> pd.DataFrame:
        """Metoda pobiera dane dotyczące wpływów z mailingów."""
        sql = read_file_sql(file_name)
        if self.test_mode:
            sql += ' limit 50'
        for i, j in dictionary.items():
            sql = sql.replace(i, j)
        data = pd.read_sql(sql, con=self.con)
        print(f'pobrano dane z {file_name}')
        return data

    @staticmethod
    def merge_data(main_df, list_of_df, name_to_marge) -> pd.DataFrame:
        """Metoda iteracyjnie merguje dane z główną ramką danych na podstawie przekazanej nazwy kolumny"""
        for i in list_of_df:
            print(f'merguje plik {main_df} z {i}')
            try:
                main_df = main_df.merge(i, how='left', on=name_to_marge)
            except KeyError as e:
                print(f'nie udało sie połączyć pliku {main_df} z {i}, rzucon błąd {e}')
        return main_df

    def insert_data(self, main_df):
        """Metoda na podstawie nazwy tabeli wstawia dane do bazy danych lub zapisuje do pliku csv."""
        if self.table_name.endswith(".csv"):
            try:
                main_df.to_csv(self.table_name, index=False)
            except OSError as e:
                if self.logger:
                    self.logger.exception(f'Bad file {e}')
        else:
            try:
                main_df.to_sql(self.table_name, self.engine, if_exists='replace', schema='raporty', index=False)
            except SQLAlchemyError as e:
                if self.logger:
                    self.logger.exception(f'Błąd zapisu danych do tabeli {self.table_name}, błąd: {e}')
                raise
        self.logger.info(f'zapisano dane do pliku/tabeli {self.table_name}')

    def download_data(self) -> pd.DataFrame:
        """Metoda do pobierania danych i zwrócenia data frame. W zależności od przekazanego parametru table_name
        pobiera dane z csv lub z bazy danych."""
        if self.table_name.endswith(".csv"):
            data_to_return = pd.read_csv(self.table_name)
        else:
            sql = f'''select * from raporty.{self.table_name}'''
            data_to_return = pd.read_sql_query(sql, self.con)
            data_to_return['grupa_akcji_3'] = data_to_return['grupa_akcji_3'].astype(int)
        return data_to_return
