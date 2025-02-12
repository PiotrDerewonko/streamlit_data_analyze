import os
from typing import Tuple, List

import pandas as pd
import streamlit as st


class ChooseOptions:
    options_gr1 = ['MAILING ADRESOWY', 'INTENCJE ŚWIĘTYCH']
    options_gr2 = ['KARDYNALSKA LUTY', 'MAILING Q1', 'MAILING Q2', 'KARDYNALSKA SIERPIEŃ',
                   'MAILING Q3 KUSTOSZ LIPIEC', 'MAILING Q3', 'MAILING Q4']
    default_gr1 = 'MAILING ADRESOWY'

    def __init__(self, con):
        self.con = con
        self.options_gr1 = ChooseOptions.options_gr1
        self.options_gr2 = ChooseOptions.options_gr2

    def find_last_mailing(self) -> Tuple[str, int]:
        """Metoda zwraca biezacy rok oraz mialing aresowy na podsatwie kwerendy."""
        sql_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         '../.././sql_queries/2_ma_detail/find_last_mailing.sql'))
        with open(sql_file_path, 'r') as sql_file:
            zapytanie = sql_file.read()
        data = pd.read_sql_query(zapytanie, self.con)
        default_camp = str(data['grupa_akcji_2'].iloc[0])
        current_year = int(data['grupa_akcji_3'].iloc[0])
        return default_camp, current_year

    def choose_options(self, count_of_years=-5) -> Tuple[List[str], List[str], List[str]]:
        """Metoda zwraca listy do odfiltrowania danych. W przypadku roku brany jest 5 ostatnich lat liczac
        od roku biezacego. """
        cls = self.__class__
        type_of_campaign = st.multiselect(options=cls.options_gr1, default=cls.default_gr1,
                                          label='Typ kampanii')
        default_camp, current_year = self.find_last_mailing()
        qamp = st.multiselect(options=cls.options_gr2,
                              label='Proszę wybrać mailing',
                              default=default_camp)
        years_options = []
        for i in range(2008, current_year + 1):
            years_options.append(str(i))
        years = st.multiselect(options=years_options, label='Proszę wybrać rok mailingu',
                               default=years_options[count_of_years:])
        return qamp, years, type_of_campaign
