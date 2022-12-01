from datetime import datetime

import pandas as pd

from functions_pandas.short_mailings_names import change_name


def download_data_about_people(con, refresh_data, limit, filtr_column):
    if refresh_data == 'True':
        # tutaj dajemy specjalne warunki np ile ma dziesiatek rozanca, czy jest w modliwtie itp
        list_of_sql = [['''select id_korespondenta, 'jest w \n
        modlitwie różańcowej' as modlitwa_rozancowa from 
        t_tajemnice_rozanca_korespondenci where czy_aktywny=True''', '''nie jest \n
        w modlitwie różańcowej'''],
                       ['''select id_korespondenta, 'posiada ' ||count(id_materialu)::text||' dziesiątek' as ilosc_dziesiatek from 
                (select distinct id_korespondenta, id_materialu from t_akcje_korespondenci tak
                left outer join t_akcje_materialy tam
                on tam.id_akcji=tak.id_akcji where tam.id_materialu in (694, 673, 652, 625, 620)) dzies
                group by id_korespondenta''', '''nie ma \n
                żadnej dziesiątki'''],
                       ['''select id_korespondenta, 'dawne wojewodzkie' as typ_miejscowosci 
                       from v_darczyncy_do_wysylki_z_poprawnymi_adresami_jeden_adres_all
                       where miejscowosc in ( 'BIAŁA PODLASKA'	,
 'BIAŁYSTOK'	,
 'BIELSKO-BIAŁA'	,
 'BYDGOSZCZ'	,
 'CHEŁM'	,
 'CIECHANÓW'	,
 'CZĘSTOCHOWA'	,
 'ELBLĄG'	,
 'GDAŃSK'	,
 'GORZÓW WIELKOPOLSKI'	,
 'JELENIA GÓRA'	,
 'KALISZ'	,
 'KATOWICE'	,
 'KONIN'	,
 'KOSZALIN'	,
 'KRAKÓW'	,
 'KROSNO'	,
 'LEGNICA'	,
 'LESZNO'	,
 'LUBLIN'	,
 'ŁOMŻA'	,
 'ŁÓDŹ'	,
 'NOWY SĄCZ'	,
 'OLSZTYN'	,
 'OPOLE'	,
 'OSTROŁĘKA'	,
 'PIŁA'	,
 'PIOTRKÓW TRYBUNALSKI'	,
 'PŁOCK'	,
 'POZNAŃ'	,
 'PRZEMYŚL'	,
 'RADOM'	,
 'RZESZÓW'	,
 'SIEDLCE'	,
 'SIERADZ'	,
 'SKIERNIEWICE'	,
 'SŁUPSK'	,
 'SUWAŁKI'	,
 'SZCZECIN'	,
 'TARNOBRZEG'	,
 'TARNÓW'	,
 'TORUŃ'	,
 'WAŁBRZYCH'	,
 'WARSZAWA'	,
 'WŁOCŁAWEK'	,
 'ZAMOŚĆ'	,
 'ZIELONA GÓRA'	)''', 'pozostałe'],['''select id_korespondenta,
       case
           when okreg_pocztowy = 0 then 'warszawski'
           when okreg_pocztowy = 1 then 'olsztyński'
           when okreg_pocztowy = 2 then 'lubelski'
           when okreg_pocztowy = 3 then 'krakowski'
           when okreg_pocztowy = 4 then 'katowicki'
           when okreg_pocztowy = 5 then 'wrocławski'
           when okreg_pocztowy = 6 then 'poznański'
           when okreg_pocztowy = 7 then 'szczeciński'
           when okreg_pocztowy = 8 then 'gdański'
           when okreg_pocztowy = 9 then 'łódzki'
           end as okreg_pocztowy       from (
select id_korespondenta , substring( kod_pocztowy, 1, 1)::int as okreg_pocztowy from v_darczyncy_do_wysylki_z_poprawnymi_adresami_jeden_adres_all) a''', 'brak'
], ['''select id_korespondenta, grupa_akcji_1 as grupa_akcji_1_dodania, grupa_akcji_2 as grupa_akcji_2_dodania, grupa_akcji_3 as grupa_akcji_3_dodania ,
 date_part('year', data ) as rok_dodania from v_akcja_dodania_korespondenta2''',
    '']]

        data_tmp_1 = pd.read_sql_query('select id_korespondenta from t_korespondenci', con)
        for j in list_of_sql:
            sql = j[0]
            data_tmp_2 = pd.read_sql_query(sql, con)
            data_tmp_1 = data_tmp_1.merge(data_tmp_2, on='id_korespondenta', how='left')
            try:
                data_tmp_1[data_tmp_2.columns[1]].fillna(j[1], inplace=True)
            except:
                a=""
        # okreslenie typu korespondenta
        try:
            rok = datetime.now().year
            liczba_lat = 3
            for i in range(rok-liczba_lat-1, rok+1):
                sql = f'''select id_korespondenta, count(kwota) as liczba_wplat_{i} from t_transakcje where data_wplywu_srodkow between '{i}-01-01' and '{i}-12-31'
                    group by id_korespondenta'''
                data_tmp_3 = pd.read_sql_query(sql, con)
                data_tmp_1 = data_tmp_1.merge(data_tmp_3, on='id_korespondenta', how='left')
                data_tmp_1[f'liczba_wplat_{i}'].fillna(0, inplace=True)
            # dane do okreslenia typu darczyncy biezacego
            data_tmp_1['liczba_lat_placacych'] = 0
            data_tmp_1['laczna_liczba_wplat'] = 0
            for i in range(rok - liczba_lat, rok+1):
                data_tmp_1['liczba_lat_placacych'].loc[data_tmp_1[f'liczba_wplat_{i}']>=1] = data_tmp_1['liczba_lat_placacych'] + 1
                data_tmp_1['laczna_liczba_wplat'] = data_tmp_1['laczna_liczba_wplat'] + data_tmp_1[f'liczba_wplat_{i}']
            data_tmp_1['średnia_liczba_wplat'] = data_tmp_1['laczna_liczba_wplat']/data_tmp_1['liczba_lat_placacych']
            data_tmp_1['TYP DARCZYŃCY BIEŻĄCY'] ='pozostali'
            data_tmp_1['TYP DARCZYŃCY BIEŻĄCY'].loc[(data_tmp_1['średnia_liczba_wplat']>=2) &
                                            (data_tmp_1['rok_dodania']<=rok-liczba_lat+1) &
                                            (data_tmp_1['liczba_lat_placacych']==4)] = 'lojalny darczyńca'
            data_tmp_1['TYP DARCZYŃCY BIEŻĄCY'].loc[(data_tmp_1['średnia_liczba_wplat']<2) & (data_tmp_1['średnia_liczba_wplat']>=1) &
                                            (data_tmp_1['rok_dodania']<=rok-liczba_lat+1) &
                                            (data_tmp_1['liczba_lat_placacych']==4)] = 'systematyczny darczyńca'
            data_tmp_1['TYP DARCZYŃCY BIEŻĄCY'].loc[(data_tmp_1['rok_dodania']==rok)] = 'nowy darczyńca'
            #dane do określenia typu darczyncy na dany rok
            data_tmp_1['liczba_lat_placacych_bis'] = 0
            data_tmp_1['laczna_liczba_wplat_bis'] = 0
            for i in range(rok - liczba_lat-1, rok):
                data_tmp_1['liczba_lat_placacych_bis'].loc[data_tmp_1[f'liczba_wplat_{i}'] >= 1] = data_tmp_1[
                                                                                                   'liczba_lat_placacych_bis'] + 1
                data_tmp_1['laczna_liczba_wplat_bis'] = data_tmp_1['laczna_liczba_wplat_bis'] + data_tmp_1[f'liczba_wplat_{i}']
            data_tmp_1['średnia_liczba_wplat_bis'] = data_tmp_1['laczna_liczba_wplat_bis']/data_tmp_1['liczba_lat_placacych_bis']

            data_tmp_1[f'TYP DARCZYŃCY NA {rok}'] ='pozostali'
            data_tmp_1[f'TYP DARCZYŃCY NA {rok}'].loc[(data_tmp_1['średnia_liczba_wplat_bis']>=2) &
                                            (data_tmp_1['rok_dodania']<=rok-liczba_lat) &
                                            (data_tmp_1['liczba_lat_placacych_bis']==4)] = 'lojalny darczyńca'
            data_tmp_1[f'TYP DARCZYŃCY NA {rok}'].loc[(data_tmp_1['średnia_liczba_wplat_bis']<2) & (data_tmp_1['średnia_liczba_wplat_bis']>=1) &
                                            (data_tmp_1['rok_dodania']<=rok-liczba_lat) &
                                            (data_tmp_1['liczba_lat_placacych_bis']==4)] = 'systematyczny darczyńca'
            data_tmp_1[f'TYP DARCZYŃCY NA {rok}'].loc[(data_tmp_1['rok_dodania']==rok)] = 'nowy darczyńca'


        except:
            a=""

        # tutaj dajemy tylko materialy z bazy
        sql = '''select id_materialu from public.t_materialy where id_typu_materialu in (8, 12)'''
        material = pd.read_sql_query(sql, con)
        list_material = material['id_materialu'].to_list()
        for i in list_material:
            print(f'dodawanie material o id {i}')
            name = pd.read_sql_query(f'''select kod_materialu from t_materialy where id_materialu = {i}''', con)
            name = name['kod_materialu'].iloc[0]
            sql_2 = f'''select distinct id_korespondenta, 'posiada \n'
            ||kod_materialu as "{name}" from t_akcje_korespondenci tak
            left outer join t_akcje_materialy tam on tam.id_akcji=tak.id_akcji
            left outer join t_materialy tm on tam.id_materialu = tm.id_materialu
            where tam.id_materialu = {i}'''
            tmp = pd.read_sql_query(sql_2, con)
            try:
                data_tmp_1 = data_tmp_1.merge(tmp, on='id_korespondenta', how='left')
                data_tmp_1[tmp.columns[1]].fillna(f'nie posiada \
                {name}', inplace=True)
                print(f'dodano material o id {i}')
            except:
                print(f'nie dodano materialu o id {i}')

        #dodanie do bazy danych utowroznej tyabeli
        data_tmp_1.to_csv('./pages/ma_details_files/tmp_file/people.csv')
    if limit == 0:
        data_to_return = pd.read_csv('./pages/ma_details_files/tmp_file/people.csv', index_col='Unnamed: 0',
                                 low_memory=False)
    else:
        data_to_return = pd.read_csv('./pages/ma_details_files/tmp_file/people.csv', index_col='Unnamed: 0',
                                     low_memory=False, nrows=limit)


    return data_to_return

def download_data_about_people_camp_pay(con, refresh_data, engine):
    if refresh_data == 'True':
        sql = f'''select tak.id_korespondenta, sum(kwota) as suma_wplat, count(kwota) as liczba_wplat,
         grupa_akcji_2 as grupa_akcji_2_wplaty, grupa_akcji_3 as grupa_akcji_3_wplaty, kod_akcji as kod_akcji_wplaty
         from t_aktywnosci_korespondentow tak
        left outer join t_akcje ta
        on ta.id_akcji = tak.id_akcji
        left outer join public.t_transakcje tr
        on tr.id_transakcji = tak.id_transakcji
        left outer join t_grupy_akcji_1 gr1
        on gr1.id_grupy_akcji_1 = ta.id_grupy_akcji_1  
        left outer join t_grupy_akcji_2 gr2
        on gr2.id_grupy_akcji_2 = ta.id_grupy_akcji_2    
        left outer join t_grupy_akcji_3 gr3
        on gr3.id_grupy_akcji_3 = ta.id_grupy_akcji_3         
        where ta.id_grupy_akcji_2 in (9,10,11,12,24,67,101) and tak.id_transakcji is not null
        group by tak.id_korespondenta, grupa_akcji_2_wplaty, grupa_akcji_3_wplaty, kod_akcji_wplaty'''
        data = pd.read_sql_query(sql, con)

        data.to_csv('./pages/ma_details_files/tmp_file/people_camp_pay.csv')
    data = pd.read_csv('./pages/ma_details_files/tmp_file/people_camp_pay.csv', index_col='Unnamed: 0')
    return data

def download_data_about_people_camp(con, refresh_data, engine):
    if refresh_data == 'True':
        sql = f'''select tak.id_korespondenta, kod_akcji as kod_akcji_wysylki, grupa_akcji_2 as grupa_akcji_2_wysylki, 
        grupa_akcji_3 as grupa_akcji_3_wysylki, koszt.koszt , 1 as naklad
        from t_akcje_korespondenci tak
        left outer join t_akcje ta 
        on ta.id_akcji=tak.id_akcji
        left outer join t_grupy_akcji_2 gr2
        on gr2.id_grupy_akcji_2 = ta.id_grupy_akcji_2
        left outer join t_grupy_akcji_3 gr3
        on gr3.id_grupy_akcji_3 = ta.id_grupy_akcji_3
        left outer join public.v_koszt_korespondenta_w_akcjach koszt
        on koszt.id_korespondenta = tak.id_korespondenta and koszt.id_akcji = tak.id_akcji
        where ta.id_grupy_akcji_2 in (9,10,11,12,24,67,100)'''
        data = pd.read_sql_query(sql, con)
        data.fillna(0, inplace=True)
        data = change_name(data)
        data.to_csv('./pages/ma_details_files/tmp_file/people_camp.csv')
    data = pd.read_csv('./pages/ma_details_files/tmp_file/people_camp.csv', index_col='Unnamed: 0')
    return data

def distinct_options(refresh_data):
    if refresh_data == 'True':
        tmp = pd.read_csv('./pages/ma_details_files/tmp_file/people.csv', index_col='Unnamed: 0',
                                     low_memory=False)
        data_about_people = tmp.drop('id_korespondenta', axis=1)
        list = data_about_people.columns
        data_to_save = pd.DataFrame()
        for i in list:
            tmp_2 = tmp[i]
            tmp_2 = tmp_2.to_frame()
            tmp_2 = tmp_2.rename({"0": f"{i}"}, axis=1)
            tmp_2.drop_duplicates(inplace=True)
            data_to_save = pd.concat([data_to_save, tmp_2])
        data_to_save.to_csv('./pages/ma_details_files/tmp_file/column_with_options.csv')
    else:
        data_to_save = pd.read_csv('./pages/ma_details_files/tmp_file/column_with_options.csv')
        data_to_save[' '] = ' '
    return data_to_save




