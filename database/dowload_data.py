import pandas as pd
def download_first_data(con):
    sql = f'''select kod_akcji, grupa_akcji_1, grupa_akcji_2, grupa_akcji_3, sum(kwota) as suma_wplat, count(kwota) as liczba_wplat, sum(koszt_calkowity) as koszt_wysylki,
           sum(naklad_calkowity) as naklad
    from t_aktywnosci_korespondentow tak
    left outer join t_akcje ta on tak.id_akcji = ta.id_akcji
    left outer join t_grupy_akcji_1 t1 on ta.id_grupy_akcji_1 = t1.id_grupy_akcji_1
    left outer join t_grupy_akcji_2 t on ta.id_grupy_akcji_2 = t.id_grupy_akcji_2
    left outer join t_grupy_akcji_3 a on ta.id_grupy_akcji_3 = a.id_grupy_akcji_3
    left outer join t_transakcje tt on tak.id_transakcji = tt.id_transakcji
    left outer join v_akcje_naklad_koszt_calkowity vankc on tak.id_akcji = vankc.id_akcji
    group by kod_akcji, grupa_akcji_1, grupa_akcji_2, grupa_akcji_3'''
    data = pd.read_sql_query(sql, con)
    return data

