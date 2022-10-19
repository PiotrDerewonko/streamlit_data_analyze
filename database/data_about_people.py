import pandas as pd
def download_data_about_people(con, refresh_data, engine):
    if refresh_data == 'True':
        # tutaj dajemy specjalne warunki np ile ma dziesiatek rozanca, czy jest w modliwtie itp
        list_of_sql = [['''select id_korespondenta, 'jest w modlitwie różańcowej' as modlitwa_rozancowa from 
        t_tajemnice_rozanca_korespondenci where czy_aktywny=True''', 'nie jest w modlitwie różańcowej'],
                       ]

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
            except:
                test =''

        #dodanie do bazy danych utowroznej tyabeli
        data_tmp_1.to_sql('people_data', engine, schema='raporty', if_exists='replace', index=False)
    data_to_return = pd.read_sql_query('select * from raporty.people_data', con)

    return data_to_return

