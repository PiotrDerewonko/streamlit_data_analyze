import os

import pandas as pd
import streamlit as st


@st.cache_data(ttl=3600)
def download_data_intention_count(_con, refresh_data) -> pd.DataFrame:
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
        data = pd.read_sql_query(zapytanie, _con)
        data.to_csv('./pages/intentions/tmp_files/count_intentions.csv', index=False)
    else:
        data_to_return = pd.read_csv('./pages/intentions/tmp_files/count_intentions.csv')
        return data_to_return

@st.cache_data(ttl=3600)
def download_data_intention_money(_con, refresh_data) -> pd.DataFrame:
    """Zadaniem funkcji jest zwrócenie data frame zawierającego informacje na temat wpłat związanych z intencjami
    swietych i blogoslawionych. Istotne jest aby pokaznae bylo od jakich swietych i blogoslawionych przychodzily
    wplaty (jesli jest to mozliwe do zidentyfikowania)"""
    if refresh_data:
        sql_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         '../.././sql_queries/9_intention/money_intentions.sql'))
        with open(sql_file_path, 'r') as sql_file:
            zapytanie = sql_file.read()
        data = pd.read_sql_query(zapytanie, _con)
        data.to_csv('./pages/intentions/tmp_files/money_intentions.csv', index=False)
    else:
        data_to_return = pd.read_csv('./pages/intentions/tmp_files/money_intentions.csv')
        return data_to_return
