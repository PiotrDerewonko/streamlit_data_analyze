import pandas as pd
import streamlit as st

@st.cache_resource(ttl=7200)
def get_costs(_con, refresh_data, _engine):
    if refresh_data == 'True':
        sql = f'''select akc.id_korespondenta, akc.id_akcji,gr3.grupa_akcji_3, gr2.grupa_akcji_2,miejscowosc, jest_zagranica, 
            druki.koszt as koszt_drukow, 
            gifty.koszt as koszt_giftow,
            perso.koszt as koszt_personalizacji,
               koszt_konfekcjonowania, koszt_wysylki_na_polske_bez_warszawy, koszt_wysylki_na_warszawe,
               koszt_wysylki_zagranica
        from t_akcje_korespondenci akc
        left outer join v_darczyncy_do_wyliczenia_kosztow_akcji vddwka on akc.id_korespondenta = vddwka.id_korespondenta
        left outer join (SELECT
        am.id_akcji,
        sum(am.koszt_jednostkowy*naklad) as koszt
        FROM
        t_akcje_materialy am
        LEFT JOIN
        t_materialy m on m.id_materialu = am.id_materialu
        WHERE
        m.id_typu_materialu IN (4, 1, 2, 6, 9, 14, 15, 16, 20, 22, 23, 24, 25, 26, 13, 11, 10, 3,28,29,21,23, 33)
         group by am.id_akcji) druki
        on druki.id_akcji = akc.id_akcji
        left outer join (SELECT
        am.id_akcji,
        sum(am.koszt_jednostkowy*naklad) as koszt
        FROM
        t_akcje_materialy am
        LEFT JOIN
        t_materialy m on m.id_materialu = am.id_materialu
        WHERE
        m.id_typu_materialu IN (34)
         group by am.id_akcji) perso
        on perso.id_akcji = akc.id_akcji
        left outer join (SELECT
        am.id_akcji,
        sum(am.koszt_jednostkowy*naklad) as koszt
        FROM
        t_akcje_materialy am
        LEFT JOIN
        t_materialy m on m.id_materialu = am.id_materialu
        WHERE
        m.id_typu_materialu IN (5, 7, 8, 12, 19, 27, 32, 30)
        GROUP BY am.id_akcji
        ) gifty on gifty.id_akcji = akc.id_akcji
        left outer join t_akcje ak
        on ak.id_akcji = akc.id_akcji
        left outer join public.t_grupy_akcji_3 gr3
        on ak.id_grupy_akcji_3 = gr3.id_grupy_akcji_3
        left outer join public.t_grupy_akcji_2 gr2
        on ak.id_grupy_akcji_2 = gr2.id_grupy_akcji_2
        
        where ak.id_grupy_akcji_2 in (9,10,11,12,24,67,101)
        '''
        data = pd.read_sql_query(sql, _con)
        tmp_action = data[
            ['id_akcji', 'koszt_wysylki_na_polske_bez_warszawy', 'koszt_wysylki_na_warszawe']].drop_duplicates()
        tmp_action['check'] = ''
        for i, row in tmp_action.iterrows():
            if row['koszt_wysylki_na_polske_bez_warszawy'] == row['koszt_wysylki_na_warszawe']:
                tmp_val = 'to samo'
            else:
                tmp_val = 'nie to samo'
            tmp_action.at[i, 'check'] = tmp_val
        tmp_action.drop('koszt_wysylki_na_polske_bez_warszawy', inplace=True, axis=1)
        tmp_action.drop('koszt_wysylki_na_warszawe', inplace=True, axis=1)
        data_with_info = pd.merge(data, tmp_action, on='id_akcji')
        data_with_info['final_post_cost'] = 0
        # wzaleznosci od warunkow dodaje rozny koszt poczty
        data_with_info['final_post_cost'].loc[(data_with_info['jest_zagranica'] == True)] = \
            data_with_info['koszt_wysylki_zagranica']
        data_with_info['final_post_cost'].loc[(data_with_info['jest_zagranica'] == False) &
                                              (data_with_info['check'] == 'to samo')] = \
            data_with_info['koszt_wysylki_na_polske_bez_warszawy']
        data_with_info['final_post_cost'].loc[(data_with_info['jest_zagranica'] == False) &
                                              (data_with_info['check'] == 'nie to samo') &
                                              (data_with_info['miejscowosc'] == 'WARSZAWA')] = \
            data_with_info['koszt_wysylki_na_warszawe']
        data_with_info['final_post_cost'].loc[(data_with_info['jest_zagranica'] == False) &
                                              (data_with_info['check'] == 'nie to samo') &
                                              (data_with_info['miejscowosc'] != 'WARSZAWA')] = \
            data_with_info['koszt_wysylki_na_polske_bez_warszawy']
        data_with_info['if_gifts'] = 0
        data_with_info['if_gifts'].loc[data_with_info['koszt_giftow'] > 0] = 1
        data_with_info.to_sql('streamlit_cost_structure', _engine, if_exists='replace', schema='raporty', index=False)
    to_return = pd.read_sql_query(f'''select * from raporty.streamlit_cost_structure''', _con)
    return to_return