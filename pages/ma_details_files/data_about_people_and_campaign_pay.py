import pandas as pd

from functions_pandas.short_mailings_names import change_name


def download_data_about_people(con, refresh_data, engine):
    if refresh_data == 'True':
        # tutaj dajemy specjalne warunki np ile ma dziesiatek rozanca, czy jest w modliwtie itp
        list_of_sql = [['''select id_korespondenta, 'jest w modlitwie różańcowej' as modlitwa_rozancowa from 
        t_tajemnice_rozanca_korespondenci where czy_aktywny=True''', 'nie jest w modlitwie różańcowej'],
                       ['''select id_korespondenta, 'posiada ' ||count(id_materialu)::text||' dziesiątek' as ilosc_dziesiatek from 
                (select distinct id_korespondenta, id_materialu from t_akcje_korespondenci tak
                left outer join t_akcje_materialy tam
                on tam.id_akcji=tak.id_akcji where tam.id_materialu in (694, 673, 652, 625, 620)) dzies
                group by id_korespondenta''', 'nie ma żadnej dziesiątki'],
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
 'ZIELONA GÓRA'	)''', 'pozostałe']]

        data_tmp_1 = pd.read_sql_query('select id_korespondenta from t_korespondenci', con)
        for j in list_of_sql:
            sql = j[0]
            data_tmp_2 = pd.read_sql_query(sql, con)
            data_tmp_1 = data_tmp_1.merge(data_tmp_2, on='id_korespondenta', how='left')
            data_tmp_1[data_tmp_2.columns[1]].fillna(j[1], inplace=True)


        # tutaj dajemy tylko materialy z bazy
        sql = '''select id_materialu from public.t_materialy where id_typu_materialu in (8, 12)'''
        material = pd.read_sql_query(sql, con)
        list_material = material['id_materialu'].to_list()
        for i in list_material:
            print(f'dodawanie material o id {i}')
            name = pd.read_sql_query(f'''select kod_materialu from t_materialy where id_materialu = {i}''', con)
            name = name['kod_materialu'].iloc[0]
            sql_2 = f'''select distinct id_korespondenta, 'posiada '||kod_materialu as "{name}" from t_akcje_korespondenci tak
            left outer join t_akcje_materialy tam on tam.id_akcji=tak.id_akcji
            left outer join t_materialy tm on tam.id_materialu = tm.id_materialu
            where tam.id_materialu = {i}'''
            tmp = pd.read_sql_query(sql_2, con)
            try:
                data_tmp_1 = data_tmp_1.merge(tmp, on='id_korespondenta', how='left')
                data_tmp_1[tmp.columns[1]].fillna(f'nie posiada {name}', inplace=True)
                print(f'dodano material o id {i}')
            except:
                print(f'nie dodano materialu o id {i}')

        #dodanie do bazy danych utowroznej tyabeli
        data_tmp_1.to_csv('./pages/ma_details_files/tmp_file/people.csv')
    data_to_return = pd.read_csv('./pages/ma_details_files/tmp_file/people.csv', index_col='Unnamed: 0',
                                 low_memory=False)
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


