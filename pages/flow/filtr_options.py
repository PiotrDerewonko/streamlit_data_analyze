import os
from datetime import datetime

import pandas as pd
import streamlit as st

from pages.flow.add_fillter_by_columns import AddFillterByColumns


class FiltrOptions:
    """Zadaniem klasy jest stworzenia słownika z parametrami, na podstawie których zostanie odfiltrowane orginalna
    ramka danych."""

    def __init__(self):
        self.options = {}
        self.current_year = datetime.today().year

    def choose_years_of_add(self) -> None:
        """Metoda dodaje slider, w którym użytkownik określa, z jakiego przedziału lat mają zostać odfiltrowani
        darczyńcy."""
        years_of_add = st.slider(min_value=2008, max_value=self.current_year, label='Wybierz rok dodania darczyńcy',
                                 value=[2008, self.current_year], key='years_of_add')
        self.options['rok_dodania'] = years_of_add

    def choose_years_to_analyze(self) -> None:
        """Metoda dodaje slider, w którym użytkownik określa, które lata mają zostać poddane analizie."""
        years_of_live = st.slider(min_value=2008, max_value=self.current_year,
                                  label='Wybierz rok kalendarzowy do analizy',
                                  value=[2008, self.current_year])
        self.options['grupa_akcji_3_wysylki'] = years_of_live

    def add_other_options(self):
        """Metoda dodaje dwa dodatkowe filtry, pozwalające filtrować po wszystkich kolumnach w pliku"""
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ma_details_files/tmp_file/column_with_options.csv'))
        df = pd.read_csv(csv_path)
        filtr_1 = AddFillterByColumns(df, 'filtr_1', 'filtr_1_wartosc', self.options,
                                      'Filtr 1')
        filtr_1.init_session_state()
        self.options = filtr_1.add_fillter_by_columns()
        filtr_2 = AddFillterByColumns(df, 'filtr_2', 'filtr_2_wartosc', self.options,
                                      'Filtr 2')
        filtr_2.init_session_state()
        self.options = filtr_2.add_fillter_by_columns()

