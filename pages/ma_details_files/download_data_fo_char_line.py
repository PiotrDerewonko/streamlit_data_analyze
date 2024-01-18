import copy
import os

import pandas as pd


def down_data_sum_and_count(con, refresh_data, engine):
    if refresh_data == 'True':
        sql = '''select grupa_akcji_3, grupa_akcji_2, sum(kwota) as suma_wplat,count(kwota) as liczba_wplat, 
        days.dzien_po_mailingu 
        from public.t_transakcje tr
        left outer join t_aktywnosci_korespondentow tak
        on tak.id_transakcji = tr.id_transakcji
        left outer join t_akcje ta 
        on ta.id_akcji = tak.id_akcji
        left outer join raporty.t_dni_po_nadaniu_mailingow days
        on days.id_grupy_akcji_3 = ta.id_grupy_akcji_3 and days.id_grupy_akcji_2 = ta.id_grupy_akcji_2
        and tr.data_wplywu_srodkow = days.data_wplywu_srodkow
        left outer join t_grupy_akcji_2 gr2 on gr2.id_grupy_akcji_2 = ta.id_grupy_akcji_2
        left outer join t_grupy_akcji_3 gr3 on gr3.id_grupy_akcji_3 = ta.id_grupy_akcji_3
        group by grupa_akcji_3, grupa_akcji_2, dzien_po_mailingu'''
        data = pd.read_sql_query(sql, con)
        data.to_sql('dash_char_ma_data', engine, if_exists='replace', schema='raporty', index=False)
    data = pd.read_sql_query('''select * from raporty.dash_char_ma_data''', con)
    return data

def down_data_cost_and_circulation(con, refresh_data, engine):
    if refresh_data == 'True':
        list_of_id_gr2 = pd.read_sql_query('''select id from fsaps_dictionary_action_group_two 
        where is_for_billing = True order by text''', con)
        list_of_id_gr2 = list_of_id_gr2['id'].tolist()
        list_of_years = pd.read_sql_query('''select id::int from fsaps_dictionary_action_group_three 
        where id <>7 order by text''', con)
        list_of_years = list_of_years['id'].tolist()
        data = pd.DataFrame()
        sql_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), f'../.././sql_queries/2_ma_detail/cost_and_cirtulation_for_char_days.sql'))
        with open(sql_file_path, 'r') as sql_file:
            zapytanie = sql_file.read()

        #zmienna pomocnicza konieczna do okreslenia roku poprzedniego, poniewaz w bazie danych jest jedna wartosc
        #nie liczbowa
        tmp = 0
        for j in list_of_years:
            for i in list_of_id_gr2:
                zapytanie_copy = copy.copy(zapytanie)
                zapytanie_copy = zapytanie_copy.replace("#A#", str(i))
                zapytanie_copy = zapytanie_copy.replace("#B#", str(j))
                if tmp > 0:
                    zapytanie_copy = zapytanie_copy.replace("#C#", str(list_of_years[tmp-1]))
                else:
                    zapytanie_copy = zapytanie_copy.replace("#C#", str(list_of_years[tmp]))
                data_tmp = pd.read_sql_query(zapytanie_copy, con)
                data = pd.concat([data, data_tmp])
            tmp += 1

        data.to_sql('dash_char_ma_data_cost_cir', engine, if_exists='replace', schema='raporty', index=False)
    data = pd.read_sql_query('''select * from raporty.dash_char_ma_data_cost_cir''', con)
    return data