import os

import pandas as pd


def download_data_intention_count(con, refresh_data) -> pd.DataFrame:
    """Funkcja pobiera dane na temat ilości przesłanych intencji. Jej wynikiem jest dataframe ktory w kolejnym kroku
    jest używany do wygenerowania raportu. Dane powinny zawierać informacje na temat intencji świętych i błogosławionych
    z możliwościa przyszłej rozbudowy o pozostałe typy. Dane tu zwrócne maja pozwolić na pokaznie jak w dniach
    spływały intencje oraz z jakich źródeł."""
    if refresh_data:
        sql_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         '../.././sql_queries/9_intention/count_intention.sql'))
        with open(sql_file_path, 'r') as sql_file:
            zapytanie = sql_file.read()
        data = pd.read_sql_query(zapytanie, con)
        data.to_csv('./pages/intentions/tmp_files/count_intentions.csv', index=False)
    else:
        data_to_return = pd.read_csv('./pages/intentions/tmp_files/count_intentions.csv', sep=';')
        return data_to_return


def download_data_intention_money(con, refresh_data) -> pd.DataFrame:
    """Zadaniem funkcji jest zwrocenie data frame zawierjacego informacje na temat wplat zwiaznych z intencjami
    swietych i blogoslawionych. Istotne jest aby pokaznae bylo od jakich swietych i blogoslawionych przychodzily
    wplaty (jesli jest to mozliwe do zidentyfikowania)"""
    #todo po dodaniu tabeli przez michala dodac infomacje o typie zamowienia
    if refresh_data:
        sql_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         '../.././sql_queries/9_intention/money_intentions.sql'))
        with open(sql_file_path, 'r') as sql_file:
            zapytanie = sql_file.read()
        data = pd.read_sql_query(zapytanie, con)
        data.to_csv('./pages/intentions/tmp_files/money_intentions.csv', index=False)
    else:
        data_to_return = pd.read_csv('./pages/intentions/tmp_files/money_intentions.csv')
        return data_to_return
