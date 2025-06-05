import pandas as pd
import streamlit as st

from database.change_types_of_columns import change_types_of_columns


@st.cache_resource(ttl=7200)
def down_data_about_cor(_con, _engine, refresh):
    if refresh == 'True':
        sql = '''select adod.id_korespondenta, grupa_akcji_1, grupa_akcji_2, grupa_akcji_3, data as data_dodania,
        last_mailing, date_part('year', data),plec, okreg_pocztowy, case when plc.id_korespondenta is not null then 
        'poprawny_adres' else 'niepoprawny' end as good_address 
        from v_akcja_dodania_korespondenta2 adod
        left outer join (select id_korespondenta, True as last_mailing  from t_akcje_korespondenci where id_akcji in (
        select id_akcji from t_akcje where id_grupy_akcji_2 in (
            select id_grupy_akcji_2 from t_akcje_korespondenci tak
left outer join t_akcje ta on tak.id_akcji = ta.id_akcji
where id_grupy_akcji_2 in (9,10,11,12) order by data desc limit 1
            )
and id_grupy_akcji_3 in (select id_grupy_akcji_3 from t_akcje_korespondenci tak
left outer join t_akcje ta on tak.id_akcji = ta.id_akcji
where id_grupy_akcji_2 in (9,10,11,12) order by data desc limit 1))
) last
on last.id_korespondenta = adod.id_korespondenta
left outer join (select id_korespondenta , 
 case 
 when substring(kod_pocztowy, 1, 1)::int=0 then 'warszawski'
 when substring(kod_pocztowy, 1, 1)::int=1 then 'olsztyński'
 when substring(kod_pocztowy, 1, 1)::int=2 then 'lubelski'
 when substring(kod_pocztowy, 1, 1)::int=3 then 'krakowski'
 when substring(kod_pocztowy, 1, 1)::int=4 then 'katowicki'
 when substring(kod_pocztowy, 1, 1)::int=5 then 'wrocłąwski'
 when substring(kod_pocztowy, 1, 1)::int=6 then 'poznański'
 when substring(kod_pocztowy, 1, 1)::int=7 then 'szczeciński'
 when substring(kod_pocztowy, 1, 1)::int=8 then 'gdański'
 when substring(kod_pocztowy, 1, 1)::int=9 then 'łódzki'
 else 'puste'
 end as okreg_pocztowy 
 from v_darczyncy_do_wysylki_z_poprawnymi_adresami_jeden_adres_all k 
left outer join t_tytuly tyt
on tyt.tytul=k.tytul_1) plc
on plc.id_korespondenta=adod.id_korespondenta
left outer join v_darczyncy_wszyscy kor
on kor.id_korespondenta=adod.id_korespondenta
left outer join (select tytul , case when id_plci=1 then 'mężczyźni'
 when id_plci=2 then 'kobiety'
 when id_plci=3 then 'mnogie' else 'mnogie'end as plec from t_tytuly) tyt
 on tyt.tytul=kor.tytul_1
'''
        data = pd.read_sql_query(sql, _con)
        data['last_mailing'].fillna(False, inplace=True)
        data = change_types_of_columns(data)
        data.to_sql('cr_distance_corr', _engine, if_exists='replace', schema='raporty', index=False)
        print('dodano cr_distance_corr')
    data = pd.read_sql_query('''select * from raporty.cr_distance_corr''', _con)
    data[['plec', 'okreg_pocztowy']].fillna('', inplace=True)
    return data

@st.cache_resource(ttl=7200)
def down_data_about_pay(_con, _engine, refresh):
    if refresh == 'True':
        #todo poporawic gdy druga wplata byla tego samego dnia to jej nie brac
        sql = '''select id_korespondenta, data_wplywu_srodkow, numer from (
        select id_korespondenta, data_wplywu_srodkow, row_number() over (PARTITION BY id_korespondenta
        order by id_korespondenta, data_wplywu_srodkow) as numer from (select distinct id_korespondenta
        , data_wplywu_srodkow from t_transakcje)a
        )foo where numer <=2 '''
        data = pd.read_sql_query(sql, _con)
        data = change_types_of_columns(data)
        data.to_sql('cr_distance_pay', _engine, if_exists='replace', schema='raporty', index=False)
        print('dodano cr_distance_pay')
    data = pd.read_sql_query('''select * from raporty.cr_distance_pay''', _con)
    tmp = data['id_korespondenta'].drop_duplicates().to_frame()
    tmp2 = data.loc[data['numer'] == 1]
    tmp2 = tmp2.rename(columns={'data_wplywu_srodkow': 'first_pay'})
    tmp = tmp.merge(tmp2, on='id_korespondenta', how='left')
    tmp2 = data.loc[data['numer'] == 2]
    tmp2 = tmp2.rename(columns={'data_wplywu_srodkow': 'second_pay'})
    tmp = tmp.merge(tmp2, on='id_korespondenta', how='left')
    return tmp