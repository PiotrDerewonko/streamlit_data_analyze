import pandas as pd
import streamlit as st

from functions_pandas.data_to_100_percent import data_to_100_percent
from functions_pandas.plot_cam_adr_dash import pivot_and_chart_for_dash
from pages.ma_details_files.get_cost_data import get_costs


def structure(con, mailing, years, engine):
    data_with_info = get_costs(con, 'False', engine)
    if len(data_with_info) >= 1:
        list_index = []
        if len(years) >= 1:
            list_index.append('grupa_akcji_3')
            data_with_info = data_with_info.loc[data_with_info['grupa_akcji_3'].isin(years)]
        if len(mailing) >= 1:
            list_index.append('grupa_akcji_2')
            data_with_info = data_with_info.loc[data_with_info['grupa_akcji_2'].isin(mailing)]
        table_witch_costs = data_with_info.pivot_table(index=list_index, values=['id_korespondenta', 'final_post_cost',
                                                                                 'koszt_drukow', 'koszt_giftow',
                                                                                 'if_gifts',
                                                                                 'koszt_konfekcjonowania',
                                                                                 'koszt_personalizacji'],
                                                       aggfunc={'id_korespondenta': 'count', 'final_post_cost': 'sum',
                                                                'koszt_drukow':
                                                                    'sum', 'koszt_giftow': 'sum', 'if_gifts': 'sum',
                                                                'koszt_personalizacji': 'sum',
                                                                'koszt_konfekcjonowania': 'sum'})
        df_with_costs = pd.DataFrame(table_witch_costs.to_records())
        df_with_costs.set_index(list_index, inplace=True)
        # Średnie koszty
        df_with_costs['avg_post_cost'] = 0
        df_with_costs['avg_post_cost'] = df_with_costs['final_post_cost'] / df_with_costs['id_korespondenta']
        df_with_costs['avg_conf_cost'] = 0
        df_with_costs['avg_conf_cost'] = df_with_costs['koszt_konfekcjonowania'] / df_with_costs['id_korespondenta']
        df_with_costs['avg_gift_cost'] = 0
        df_with_costs['avg_gift_cost'] = df_with_costs['koszt_giftow'] / df_with_costs['if_gifts']
        df_with_costs['avg_printing_cost'] = 0
        df_with_costs['avg_printing_cost'] = df_with_costs['koszt_drukow'] / df_with_costs['id_korespondenta']
        df_with_costs['avg_perso_cost'] = 0
        df_with_costs['avg_perso_cost'] = df_with_costs['koszt_personalizacji'] / df_with_costs['id_korespondenta']
        df_with_costs.drop(
            ['koszt_konfekcjonowania', 'id_korespondenta', 'koszt_drukow', 'final_post_cost', 'koszt_giftow',
             'if_gifts', 'koszt_personalizacji'], axis=1, inplace=True)
        df_with_costs.rename(columns={'avg_post_cost': 'koszt_poczty', 'avg_conf_cost': 'koszt_konfekcjonowania',
                                      'avg_gift_cost': 'koszt_giftów',
                                      'avg_printing_cost': 'koszt_drukow', 'avg_perso_cost': 'koszt_personalizacji'},
                             inplace=True)
        temp_df = pd.DataFrame(data={'Nazwa parametru': ['koszt_poczty', 'koszt_konfekcjonowania', 'koszt_giftów',
                                                         'koszt_drukow', 'koszt_personalizacji'],
                                     'oś': ['Oś główna', 'Oś główna', 'Oś główna', 'Oś główna', 'Oś główna'],
                                     'Opcje': ['Wykres Słupkowy Skumulowany', 'Wykres Słupkowy Skumulowany',
                                               'Wykres Słupkowy Skumulowany',
                                               'Wykres Słupkowy Skumulowany', 'Wykres Słupkowy Skumulowany']
                                     }, index=[0, 1, 2, 3, 4])
        dict_of_oriantation = {'major': 'vertical', 'group': 'vertical', 'sub_group': 'vertical'}

        # srednie koszty oraz ich struktura
        char_cost, a = pivot_and_chart_for_dash(data_with_info, list_index, 'me_detail', 'Wykres ', 'Wybrane kolumny',
                                                {},
                                                df_with_costs, temp_df, 'Średni koszt z wybranych mailingów',
                                                dict_of_oriantation)
        df_with_costs_100 = data_to_100_percent(df_with_costs)
        char_cost_to_100, b = pivot_and_chart_for_dash(data_with_info, list_index, 'me_detail', 'Wykres ',
                                                       'Wybrane kolumny',
                                                       {},
                                                       df_with_costs_100, temp_df,
                                                       'Struktura średnich kosztów z wybranych mailingów',
                                                       dict_of_oriantation)
        table_witch_costs.rename(columns={'id_korespondenta': 'nakład', 'final_post_cost': 'koszt_poczty'},
                                 inplace=True)

        # koszty calkowite i struktura kosztow calkowitych
        temp_df_2 = pd.DataFrame(data={'Nazwa parametru': ['koszt_poczty', 'koszt_konfekcjonowania', 'koszt_giftow',
                                                           'koszt_drukow', 'koszt_personalizacji', 'nakład'],
                                       'oś': ['Oś główna', 'Oś główna', 'Oś główna', 'Oś główna',
                                              'Oś główna', 'Oś pomocnicza'],
                                       'Opcje': ['Wykres Słupkowy Skumulowany', 'Wykres Słupkowy Skumulowany',
                                                 'Wykres Słupkowy Skumulowany',
                                                 'Wykres Słupkowy Skumulowany', 'Wykres Słupkowy Skumulowany',
                                                 'Wykres liniowy']
                                       }, index=[0, 1, 2, 3, 4, 5])
        table_witch_costs_100 = data_to_100_percent(table_witch_costs[['koszt_poczty', 'koszt_drukow', 'koszt_giftow',
                                                                       'koszt_konfekcjonowania',
                                                                       'koszt_personalizacji']])
        table_witch_costs_100 = pd.merge(table_witch_costs_100, table_witch_costs[['nakład']], how='left',
                                         left_index=True, right_index=True)
        char_cost_values, a = pivot_and_chart_for_dash(data_with_info, list_index, 'me_detail', 'Wykres ',
                                                       'Wybrane kolumny', {},
                                                       table_witch_costs[
                                                           ['koszt_poczty', 'koszt_drukow', 'koszt_giftow', 'nakład',
                                                            'koszt_konfekcjonowania',
                                                            'koszt_personalizacji']],
                                                       temp_df_2, 'Całkowity koszt wybranych mailingów',
                                                       dict_of_oriantation)
        char_cost_values_100, a = pivot_and_chart_for_dash(data_with_info, list_index, 'me_detail', 'Wykres ',
                                                           'Wybrane kolumny', {},
                                                           table_witch_costs_100[
                                                               ['koszt_poczty', 'koszt_drukow', 'koszt_giftow',
                                                                'nakład',
                                                                'koszt_konfekcjonowania', 'koszt_personalizacji']],
                                                           temp_df_2,
                                                           'Struktura całkowitych kosztów wybranych mailingów',
                                                           dict_of_oriantation)
        tab1, tab2, tab3, tab4, tab5 = st.tabs(['Średnie koszty', 'Koszty całościowe', 'Struktura Średnich kosztów',
                                                'Struktura kosztów całkowitych', 'Zestawienie kosztów i materiałów'])
        with tab1:
            st.bokeh_chart(char_cost, use_container_width=True)
            with st.expander('Zobacz tabele z danymi'):
                st.dataframe(df_with_costs)
        with tab2:
            st.bokeh_chart(char_cost_values, use_container_width=True)
            with st.expander('Zobacz tabele z danymi'):
                st.dataframe(table_witch_costs[['koszt_poczty', 'koszt_drukow', 'koszt_giftow', 'nakład',
                                                'koszt_konfekcjonowania', 'koszt_personalizacji']])
        with tab3:
            st.bokeh_chart(char_cost_to_100, use_container_width=True)
            with st.expander('Zobacz tabele z danymi'):
                st.dataframe(df_with_costs_100)
        with tab4:
            st.bokeh_chart(char_cost_values_100, use_container_width=True)
            with st.expander('Zobacz tabele z danymi'):
                st.dataframe(table_witch_costs_100[['koszt_poczty', 'koszt_drukow', 'koszt_giftow', 'nakład',
                                                    'koszt_konfekcjonowania', 'koszt_personalizacji']])
        with tab5:
            checkbox = st.checkbox('Dane szczegółowe')
            sql = '''select distinct grupa_akcji_2, grupa_akcji_3, typ_materialu, kod_materialu, 
            sum(koszt_jednostkowy*akcje.naklad)/sum(akcje.naklad) as koszt_jednostkowy, case  
            WHEN tm.id_typu_materialu in (5, 7, 8, 12, 19, 27, 32, 30,31) then 'GIFT'
            WHEN tm.id_typu_materialu in (34) then 'PERSONALIZACJE'
            WHEN tm.id_typu_materialu in (4, 1, 2, 6, 9, 14, 15, 16, 20, 22, 23, 24, 25, 26, 13, 11, 10, 3,28,29,21,23, 33) then 'DRUKI'
            ELSE ''
            END AS zgrupowane_typy
             from t_akcje_materialy tam
left outer join t_akcje ta on tam.id_akcji = ta.id_akcji
left outer join t_grupy_akcji_2 t on ta.id_grupy_akcji_2 = t.id_grupy_akcji_2
left outer join t_grupy_akcji_3 a on ta.id_grupy_akcji_3 = a.id_grupy_akcji_3
left outer join t_materialy tm on tam.id_materialu = tm.id_materialu
left outer join t_typy_materialow ttm on tm.id_typu_materialu = ttm.id_typu_materialu
left outer join (select ta2.id_akcji, count(id_korespondenta) as naklad from t_akcje_korespondenci
left outer join t_akcje ta2 on t_akcje_korespondenci.id_akcji = ta2.id_akcji
left outer join t_grupy_akcji_2 tga2 on ta2.id_grupy_akcji_2 = tga2.id_grupy_akcji_2
left outer join t_grupy_akcji_3 tga3 on ta2.id_grupy_akcji_3 = tga3.id_grupy_akcji_3
    group by ta2.id_akcji) akcje
on akcje.id_akcji = ta.id_akcji
group by grupa_akcji_3, grupa_akcji_2, typ_materialu, kod_materialu, zgrupowane_typy
order by grupa_akcji_3, grupa_akcji_2, typ_materialu, kod_materialu

'''
            data_tmp = pd.read_sql_query(sql, con)
            if len(years) >= 1:
                data_tmp = data_tmp.loc[data_tmp['grupa_akcji_3'].isin(years)]
            if len(mailing) >= 1:
                data_tmp = data_tmp.loc[data_tmp['grupa_akcji_2'].isin(mailing)]
            to_show = ['zgrupowane_typy', 'typ_materialu']
            if checkbox:
                to_show.append('kod_materialu')
            pivot = pd.pivot_table(data=data_tmp, index=to_show, columns=list_index,
                                   values='koszt_jednostkowy', aggfunc={'koszt_jednostkowy': 'sum'})
            st.dataframe(pivot, use_container_width=True)
            st.download_button('Pobierz dane w formacie .csv', pivot.to_csv(decimal=','),
                               file_name='koszty_jednostkowe.csv', mime='text/csv')
