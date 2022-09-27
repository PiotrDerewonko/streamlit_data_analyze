import pandas as pd

def down_data_about_cor(con, engine, refresh):
    if refresh == 'True':
        sql = '''select id_korespondenta, grupa_akcji_1, grupa_akcji_2, grupa_akcji_3, 
        date_part('year', data)
        from v_akcja_dodania_korespondenta2'''
        data = pd.read_sql_query(sql, con)
        data.to_sql('cr_distance_corr', engine, if_exists='replace', schema='raporty', index=False)
    data = pd.read_sql_query('''select * from raporty.cr_distance_corr''', con)
    return data

def down_data_about_pay(con, engine, refresh):
    if refresh == 'True':
        sql = '''select id_korespondenta, data_wplywu_srodkow, numer from (
        select id_korespondenta, data_wplywu_srodkow, row_number() over (PARTITION BY id_korespondenta
        order by id_korespondenta, data_wplywu_srodkow) as numer from t_transakcje
        )foo where numer <=2 '''
        data = pd.read_sql_query(sql, con)
        data.to_sql('cr_distance_pay', engine, if_exists='replace', schema='raporty', index=False)
    data = pd.read_sql_query('''select * from raporty.cr_distance_pay''', con)
    tmp = data['id_korespondenta'].drop_duplicates()
    tmp2 = data.loc[data['numer']==1]
    tmp2.rename(columns={'data_wplywu_srodkow': 'first_pay'})
    tmp = tmp.merge(tmp2, on='id_korespondenta')
    tmp2 = data.loc[data['numer']==2]
    tmp2.rename(columns={'data_wplywu_srodkow': 'second_pay'})
    tmp = tmp.merge(tmp2, on='id_korespondenta')
    return tmp