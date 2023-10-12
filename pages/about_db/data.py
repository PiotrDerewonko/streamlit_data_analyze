import datetime

import pandas as pd
import streamlit as st


def add_data_about_peaopl_in_camp(con, cur):
    year_now = datetime.datetime.now()
    year_now = year_now.year + 1
    sql = ''' delete from raporty.t_baza'''
    cur.execute(sql)
    con.commit()
    sql = ''' delete from raporty.t_raport_z_przyrastania_bazy'''
    cur.execute(sql)
    con.commit()
    sql = ''' delete from raporty.t_zwroty'''
    cur.execute(sql)
    con.commit()
    for i in range(2008, year_now):
        sql = f'''insert into raporty.t_baza (id_korespondenta, rok)  (select id_korespondenta,{i}
from (select id_korespondenta from t_akcje_korespondenci where id_akcji in (select id_akcji from t_akcje where id_grupy_akcji_2=12 and id_grupy_akcji_3 in (select id_grupy_akcji_3 from t_grupy_akcji_3 where grupa_akcji_3={i}::character varying))
union
select id_korespondenta from v_data_dodania_korespondenta where data_dodania between ({i}||'-01-01')::date and ({i}||'-12-31')::date
)a 
where id_korespondenta in (select id_korespondenta from t_korespondenci where id_typu_korespondenta in (1,9))
);'''
        cur.execute(sql)
        con.commit()
        sql = f'''insert into raporty.t_raport_z_przyrastania_bazy (id_korespondenta, rok, rodzaj )  (select distinct id_korespondenta,{i}, 'baza'
        from raporty.t_baza
        where id_korespondenta in (select id_korespondenta from t_korespondenci except select id_korespondenta from raporty.t_raport_z_przyrastania_bazy where rok={i})and rok={i}
        )'''
        cur.execute(sql)
        con.commit()
        sql = f'''insert into raporty.t_raport_z_przyrastania_bazy (id_korespondenta, rok, rodzaj) (select id_korespondenta, {i},'ograniczenie' from raporty.t_ogrzeniczenie_korespondenci where rok<= {i});'''
        cur.execute(sql)
        con.commit()
        sql =f'''update raporty.t_raport_z_przyrastania_bazy set wplata='wplata' where rok={i} and id_korespondenta in (select id_korespondenta from t_transakcje where data_wplywu_srodkow between ({i}||'-01-01')::date and ({i}||'-12-31')::date);'''
        cur.execute(sql)
        con.commit()
        sql = f'''insert into raporty.t_zwroty (id_korespondenta, przyczyna_zwrotu, data_zwrotu, rok ) (select id_korespondenta, pz.przyczyna_zwrotu, wazny_do, date_part ('year', wazny_do)as rok from t_adresy a left outer join t_przyczyny_zwrotow pz on pz.id_przyczyny_zwrotu=a.id_przyczyny_zwrotu where wazny_do is not null

 and id_korespondenta in (select id_korespondenta from t_korespondenci where id_typu_korespondenta in (1,9)));'''
        cur.execute(sql)
        con.commit()
        sql = f'''insert into raporty.t_raport_z_przyrastania_bazy (id_korespondenta, rok, rodzaj) (select id_korespondenta, {i},'zwroty' from raporty.t_zwroty where rok <={i});'''
        cur.execute(sql)
        con.commit()
        sql = f'''delete from raporty.t_raport_z_przyrastania_bazy where rodzaj='ograniczenie' and
                                                       rok = {i}
and id_korespondenta in (select id_korespondenta from raporty.t_raport_z_przyrastania_bazy where rok ={i} and rodzaj='baza')'''
        cur.execute(sql)
        con.commit()
    sql_fin = '''select * from raporty.t_raport_z_przyrastania_bazy'''
    data = pd.read_sql_query(sql_fin, con)
    return data

@st.cache_data(ttl=7200)
def download_data(_con, refresh_data):
    if refresh_data == 'True':
        cur = _con.cursor()
        data = add_data_about_peaopl_in_camp(_con, cur)
        data['wplata'].fillna('brak wplaty', inplace=True)
        data_type = pd.read_csv('./pages/ma_details_files/tmp_file/people_camp.csv', index_col='Unnamed: 0', low_memory=False)
        data_type = data_type[['id_korespondenta', 'grupa_akcji_3_wysylki', 'TYP DARCZYŃCY']]
        data_type.drop_duplicates(inplace=True)
        data_final = pd.merge(data, data_type, how='left', left_on=['id_korespondenta', 'rok'],
                              right_on=['id_korespondenta', 'grupa_akcji_3_wysylki'])
        data_final.drop('grupa_akcji_3_wysylki', inplace=True, axis=1)
        data.to_csv('./pages/about_db/tmp_file/data_db.csv')
    data = pd.read_csv('./pages/about_db/tmp_file/data_db.csv', index_col='Unnamed: 0', low_memory=False)
    return data