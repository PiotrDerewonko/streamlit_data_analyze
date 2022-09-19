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

def download_second_data(con):
    sql = f'''select tr.id_korespondenta,kod_akcji, kwota as suma_wplat,1 as liczba_wplat, 0 as koszt_calkowity, 0 as naklad, grupa_akcji_1, grupa_akcji_2, grupa_akcji_3
from t_transakcje tr
left outer join t_aktywnosci_korespondentow tak on tr.id_transakcji = tak.id_transakcji
left outer join t_akcje ta on tak.id_akcji = ta.id_akcji
left outer join t_grupy_akcji_1 t on ta.id_grupy_akcji_1 = t.id_grupy_akcji_1
left outer join t_grupy_akcji_2 a on ta.id_grupy_akcji_2 = a.id_grupy_akcji_2
left outer join t_grupy_akcji_3 tga3 on ta.id_grupy_akcji_3 = tga3.id_grupy_akcji_3
where ta.id_grupy_akcji_2 in (9,10,11,12,24,67)
union
select id_korespondenta, kod_akcji, 0,0, koszt, 1 ,grupa_akcji_1, grupa_akcji_2, grupa_akcji_3
 from v_koszt_korespondenta_w_akcjach tak
left outer join t_akcje ta on tak.id_akcji = ta.id_akcji
left outer join t_grupy_akcji_1 t on ta.id_grupy_akcji_1 = t.id_grupy_akcji_1
left outer join t_grupy_akcji_2 a on ta.id_grupy_akcji_2 = a.id_grupy_akcji_2
left outer join t_grupy_akcji_3 tga3 on ta.id_grupy_akcji_3 = tga3.id_grupy_akcji_3
where ta.id_grupy_akcji_2 in (9,10,11,12,24,67)'''
    data = pd.read_sql_query(sql, con)
    return data

def download_dash_address_data(con, refresh, engine, type):
    if type =='address':
        id_group_two = '(9,10,11,12,24,67,100)'
        extra = ''
        extra_group = ''
    else:
        id_group_two = '(1, 2, 5, 91, 93, 95, 96, 101, 102, 103, 104, 105)'
        extra = ', substring(ta.kod_akcji, 7,2) as miesiac'
        extra_group = ',miesiac'
    if refresh == 'True':
        # todo przerobic to na nowe tabele w nowej bazie danych
        # todo w przypadku danych bezadresowych dodac material ilosc pozyskanych osob
        sql = f'''select grupa_akcji_3,grupa_akcji_2, sum(kwota) as suma_wplat, count(tr.id_transakcji)
                 as liczba_wplat, 0 as koszt_calkowity, 0 as naklad_calkowity {extra} from public.t_aktywnosci_korespondentow tak
                left outer join public.t_transakcje tr
                on tr.id_transakcji = tak.id_transakcji
                left outer join t_akcje ta
                on ta.id_akcji=tak.id_akcji
                left outer join public.t_grupy_akcji_2 t on ta.id_grupy_akcji_2 = t.id_grupy_akcji_2
                left outer join public.t_grupy_akcji_3 a on ta.id_grupy_akcji_3 = a.id_grupy_akcji_3

                where tak.id_akcji in ( select id_akcji from t_akcje where  id_grupy_akcji_2 in {id_group_two} and t_akcje.id_grupy_akcji_3 !=7)
                group by --rok_i_mailing, 
                grupa_akcji_3,grupa_akcji_2{extra_group}
                union
                select distinct --grupa_akcji_2||' '|| grupa_akcji_3 as rok_i_mailing,
                grupa_akcji_3,grupa_akcji_2, 0, 0, sum(koszt_calkowity), sum(naklad_calkowity) {extra} from v_akcje_naklad_koszt_calkowity vankc
            left outer join t_akcje ta on vankc.id_akcji = ta.id_akcji
            left outer join t_grupy_akcji_2 t on ta.id_grupy_akcji_2 = t.id_grupy_akcji_2
            left outer join t_grupy_akcji_3 a on ta.id_grupy_akcji_3 = a.id_grupy_akcji_3
            where vankc.id_akcji in (select id_akcji from t_akcje where id_grupy_akcji_2 in {id_group_two} and t_akcje.id_grupy_akcji_3 !=7)
            group by --rok_i_mailing,
                grupa_akcji_3,grupa_akcji_2{extra_group}
                '''
        to_insert = pd.read_sql_query(sql, con)
        if type == 'address':
            to_insert.to_sql('dash_ma_data', engine, if_exists='replace', schema='raporty', index=False)
            print('dodano do bazy danych dane dla dashboard adresowy')

        else:
            to_insert.to_sql('dash_db_data', engine, if_exists='replace', schema='raporty', index=False)
            print('dodano do bazy danych dane dla dashboard bezadresowy')
    if type == 'address':
        sql = f'''select * from raporty.dash_ma_data'''
    else:
        sql = f'''select * from raporty.dash_db_data'''
    to_return = pd.read_sql_query(sql, con)
    to_return['grupa_akcji_3'] = to_return['grupa_akcji_3'].astype(int)

    return to_return

def download_increase_data(con, refresh, engine):
    if refresh == 'True':
        sql = f'''select date_part('year', adod.data) as rok_dodania, grupa_akcji_1, grupa_akcji_2, 
        date_part('month', adod.data) as miesiac_dodania, count(id_korespondenta) as ilosc
        from v_akcja_dodania_korespondenta2 adod
        group by rok_dodania, grupa_akcji_1, grupa_akcji_2, miesiac_dodania'''
        to_insert = pd.read_sql_query(sql, con)
        to_insert.to_sql('dash_increase_data', engine, if_exists='replace', schema='raporty', index=False)
        print('dodano do bazy danych dane dla dashboard przyrost')
    to_return = pd.read_sql_query('select * from raporty.dash_increase_data', con)
    return to_return
