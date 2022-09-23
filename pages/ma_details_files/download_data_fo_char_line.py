import pandas as pd
def down_data(con, refresh_data, engine):
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