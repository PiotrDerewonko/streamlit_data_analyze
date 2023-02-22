import pandas as pd
import streamlit as st
from dateutil.relativedelta import relativedelta


@st.cache_data
def live_people_from_db(_con, refresh_data):
    if refresh_data == 'True':
        id_group_two = '(1, 2, 4,  5, 91, 93, 95, 96, 101, 102, 103, 104, 105, 82)'
        sql = f'''select id_akcji, kod_akcji from t_akcje where id_grupy_akcji_2 in {id_group_two} 
        and id_grupy_akcji_3>=8 order by id_akcji desc'''
        list_of_sub_actions = pd.read_sql_query(sql, _con)
        dataframe_costs = pd.read_sql_query('''select id_korespondenta, data, sum(koszt) as koszt_utrzymania
         from public.v_koszt_korespondenta_w_akcjach
         group by id_korespondenta, data''', _con)
        final_df = pd.DataFrame(data={'id_korespondenta': 1, 'data_dodania': '2008-01-01', 'suma_wplat': 0, 'koszt_utrzymania': 0}, index=[0])
        for i, row in list_of_sub_actions.iterrows():
            sql_2 = f'''select id_korespondenta, data as data_dodania, 0 as wplaty, 0 as koszt_utrzymania, id_akcji,
            1 as miesiac_obecnosci_w_bazie
             from v_akcja_dodania_korespondenta2 where id_akcji = {row['id_akcji']}'''
            tmp = pd.read_sql_query(sql_2, _con)
            tmp['data_tmp'] = tmp['data_dodania']
            fin_for_subaction = tmp.copy()
            for j in range(1, 24):
                tmp['data_tmp'] = tmp['data_tmp'] + relativedelta(months=1)
                tmp['miesiac_obecnosci_w_bazie'] = j + 1
                fin_for_subaction = pd.concat([fin_for_subaction, tmp], ignore_index=True)

            #wyciagam unikalna liste data dodania i zamieniam na pierwszy u osoatni dzien miesiaca w celu dalszych petli
            date = fin_for_subaction['data_tmp'].drop_duplicates().to_frame()
            date['last_day'] = date['data_tmp'] + relativedelta(day=31)
            date['first_day'] = date['data_tmp'] - relativedelta(day=1)
            date.drop(columns=['data_tmp'], inplace=True)
            date.drop_duplicates(subset=['first_day'], inplace=True)
            fin_for_subaction['data_tmp'] = fin_for_subaction['data_tmp'] - relativedelta(day=1)
            fin_for_subaction['year'] = fin_for_subaction['data_tmp'].astype(str).str[:4].astype(int)
            fin_for_subaction['month'] = fin_for_subaction['data_tmp'].astype(str).str[5:7].astype(int)

            #pobieram unikalan liste uzytkownikow
            list_of_id = tmp.drop_duplicates(subset=['id_korespondenta'])
            list_of_id2 = tuple(list_of_id['id_korespondenta'])
            if len(list_of_id2) == 1:
                list_of_id2 = '(' + str(list_of_id2[0]) + ')'

            #pobieram uniklan liste dat dodania (wszytskie jako 1 dzien miesiaca)
            uniq_data_of_add = tmp['data_dodania'].drop_duplicates().to_frame()
            uniq_data_of_add['first_day'] = tmp['data_dodania'] - relativedelta(day=1)
            uniq_data_of_add.drop(columns=['data_dodania'], inplace=True)
            uniq_data_of_add = uniq_data_of_add.drop_duplicates()
            uniq_data_of_add['last_day'] = uniq_data_of_add['first_day'] + relativedelta(day=31)
            uniq_data_of_add.sort_values(by='first_day', inplace=True)

            #petla dodajaca sume wplat w tabeli z datami
            print(f'''rozpoczynam dodawanie wplat {row['kod_akcji']}''')
            for j3, row3 in date.iterrows():
                rok = int(str(row3['first_day'])[:4])
                miesiac = int(str(row3['first_day'])[5:7])

                sql_3 = f"""select id_korespondenta, sum(kwota) as wplaty, {miesiac} as month
                , {rok} as year
                from t_transakcje where data_wplywu_srodkow
                between '{row3['first_day']}' and '{row3['last_day']}' and id_korespondenta in {list_of_id2}
                group by id_korespondenta"""
                data_tmp_pay = pd.read_sql_query(sql_3, _con)
                if len(data_tmp_pay)>=1:
                    data_tmp_pay.set_index(['id_korespondenta', 'year', 'month'], inplace=True)
                    fin_for_subaction.set_index(['id_korespondenta', 'year', 'month'], inplace=True)
                    fin_for_subaction.update(data_tmp_pay)
                    fin_for_subaction.reset_index(inplace=True)
                print(f'''dodano wplaty lp {j3} dla {row['kod_akcji']} za rok {rok} za miesiac {miesiac} ''')
            print(f'''zakonczono dodawanie wplat {row['kod_akcji']}''')


            # petla dodajaca koszt utrzymania w tabeli z datami
            print(f'''rozpoczynam dodawanie kosztow {row['kod_akcji']}''')
            for j5, row5 in date.iterrows():
                rok = int(str(row5['first_day'])[:4])
                miesiac = int(str(row5['first_day'])[5:7])
                tmp_cost = dataframe_costs.loc[(dataframe_costs['data'] >= row5['first_day']) &
                                               (dataframe_costs['data'] <= row5['last_day']) &
                                               (dataframe_costs['id_korespondenta'].isin(list_of_id2))]
                if len(tmp_cost)>=1:
                    tmp_cost['month'] = miesiac
                    tmp_cost['year'] = rok
                    tmp_pivot = pd.pivot_table(tmp_cost, index=['id_korespondenta', 'year', 'month'],
                                         values='koszt_utrzymania', aggfunc='sum')
                    fin_for_subaction.set_index(['id_korespondenta', 'year', 'month'], inplace=True)
                    fin_for_subaction.update(tmp_pivot)
                    fin_for_subaction.reset_index(inplace=True)
                print(f'''dodano koszty lp {j5} dla {row['kod_akcji']} za rok {rok} za miesiac {miesiac} ''')

            print(f'''zakonczono dodawanie kosztow {row['kod_akcji']}''')
            # dodanie kosztow pozyskania
            cost_of_add = pd.read_sql_query(f''' select k.id_akcji, sum(koszt_calkowity) * wspolczynnik as koszt_insertu,
            1 as miesiac_obecnosci_w_bazie from 
            v_akcje_naklad_koszt_calkowity k 
            left outer join t_akcje ta 
            on ta.id_akcji = k.id_akcji
            left outer join (select kod_akcji,  suma_wplat_nowi/suma_wplat as wspolczynnik from raporty.dash_db_data) cost
            on cost.kod_akcji = ta.kod_akcji 
            where k.id_akcji = {row['id_akcji']}
            group by k.id_akcji, wspolczynnik''', _con)

            # lacze utworzona tabela dla danej sub akcji w jedna wielka atbele ze wszystkimi subakcjiami
            final_df = pd.concat([final_df, fin_for_subaction, cost_of_add])
            final_df.fillna(0, inplace=True)

        # dodac grupy akcji 1,2,3
        tags = pd.read_sql_query('''select id_akcji, kod_akcji,  grupa_akcji_1, grupa_akcji_3, grupa_akcji_2 from t_akcje ta
        left outer join public.t_grupy_akcji_1 gr1
        on gr1.id_grupy_akcji_1 = ta.id_grupy_akcji_1
        left outer join public.t_grupy_akcji_2 gr2
        on gr2.id_grupy_akcji_2 = ta.id_grupy_akcji_2
        left outer join public.t_grupy_akcji_3 gr3
        on gr3.id_grupy_akcji_3 = ta.id_grupy_akcji_3''', _con)
        final_df = pd.merge(final_df, tags, on='id_akcji', how='left')


        #zapis do csv
        final_df.to_csv('./pages/db_analyze/tmp_file/db.csv')

    data = pd.read_csv('./pages/db_analyze/tmp_file/db.csv')

    return data



