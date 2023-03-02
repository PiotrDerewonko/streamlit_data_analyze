import pandas as pd
import streamlit as st

from functions_pandas.plot_cam_adr_dash import pivot_and_chart_for_dash
from pages.ma_details_files.get_cost_data import get_costs


def structure(con, mailing, years, engine):
    data_with_info = get_costs(con, 'False', engine)
    list_index = []
    if len(years) >= 1:
        list_index.append('grupa_akcji_3')
        data_with_info = data_with_info.loc[data_with_info['grupa_akcji_3'].isin(years)]
    if len(mailing) >= 1:
        list_index.append('grupa_akcji_2')
        data_with_info = data_with_info.loc[data_with_info['grupa_akcji_2'].isin(mailing)]
    table_witch_costs = data_with_info.pivot_table(index=list_index, values=['id_korespondenta', 'final_post_cost',
                                                                        'koszt_drukow', 'koszt_giftow', 'if_gifts',
                                                                       'koszt_konfekcjonowania'],
                                        aggfunc={'id_korespondenta': 'count', 'final_post_cost': 'sum', 'koszt_drukow':
                                                 'sum', 'koszt_giftow': 'sum', 'if_gifts': 'sum', 'koszt_drukow': 'sum',
                                                 'koszt_konfekcjonowania': 'sum'})
    df_with_costs = pd.DataFrame(table_witch_costs.to_records())
    df_with_costs.set_index(list_index, inplace=True)
    #Średnie koszty
    df_with_costs['avg_post_cost'] = 0
    df_with_costs['avg_post_cost'] = df_with_costs['final_post_cost'] / df_with_costs['id_korespondenta']
    df_with_costs['avg_conf_cost'] = 0
    df_with_costs['avg_conf_cost'] = df_with_costs['koszt_konfekcjonowania'] / df_with_costs['id_korespondenta']
    df_with_costs['avg_gift_cost'] = 0
    df_with_costs['avg_gift_cost'] = df_with_costs['koszt_giftow'] / df_with_costs['if_gifts']
    df_with_costs['avg_printing_cost'] = 0
    df_with_costs['avg_printing_cost'] = df_with_costs['koszt_drukow'] / df_with_costs['id_korespondenta']
    df_with_costs.drop(['koszt_konfekcjonowania', 'id_korespondenta', 'koszt_drukow', 'final_post_cost', 'koszt_giftow',
                        'if_gifts'], axis=1, inplace=True)
    df_with_costs.rename(columns={'avg_post_cost': 'koszt_poczty', 'avg_conf_cost': 'koszt_konfekcjonowania' ,
                                  'avg_gift_cost' : 'koszt_giftów' ,
    'avg_printing_cost': 'koszt_drukow'}, inplace=True)
    temp_df = pd.DataFrame(data={'Nazwa parametru': ['koszt_poczty', 'koszt_konfekcjonowania', 'koszt_giftów', 'koszt_drukow'],
                                 'oś': ['Oś główna', 'Oś główna', 'Oś główna', 'Oś główna'],
                                 'Opcje': ['Wykres Słupkowy Skumulowany', 'Wykres Słupkowy Skumulowany', 'Wykres Słupkowy Skumulowany',
                                           'Wykres Słupkowy Skumulowany']
                                 }, index=[0,1,2,3])
    dict_of_oriantation = {'major': 'vertical', 'group': 'vertical', 'sub_group': 'vertical'}
    char_cost, a = pivot_and_chart_for_dash(data_with_info, list_index, 'me_detail', 'Wykres ', 'Wybrane kolumny', {},
                                       df_with_costs, temp_df,'Średni koszt z wybranych mailingów', dict_of_oriantation)
    table_witch_costs.rename(columns={'id_korespondenta': 'nakład', 'final_post_cost': 'koszt_poczty'}, inplace=True)
    temp_df_2 = pd.DataFrame(data={'Nazwa parametru': ['koszt_poczty', 'koszt_konfekcjonowania', 'koszt_giftow',
                                                       'koszt_drukow', 'nakład'],
                                 'oś': ['Oś główna', 'Oś główna', 'Oś główna', 'Oś główna', 'Oś pomocnicza'],
                                 'Opcje': ['Wykres Słupkowy Skumulowany', 'Wykres Słupkowy Skumulowany', 'Wykres Słupkowy Skumulowany',
                                           'Wykres Słupkowy Skumulowany', 'Wykres liniowy']
                                 }, index=[0,1,2,3, 4])
    char_cost_values, a = pivot_and_chart_for_dash(data_with_info, list_index, 'me_detail', 'Wykres ', 'Wybrane kolumny', {},
                                       table_witch_costs[['koszt_poczty', 'koszt_drukow', 'koszt_giftow','nakład',
                                                                       'koszt_konfekcjonowania']],
                                                temp_df_2,'Całkowity koszt wybranych mailingów', dict_of_oriantation)
    tab1, tab2 = st.tabs(['Średnie koszty', 'Koszty całościowe'])
    with tab1:
        st.bokeh_chart(char_cost, use_container_width=True)
        with st.expander('Zobacz tabele z danymi'):
            st.dataframe(df_with_costs)
    with tab2:
        st.bokeh_chart(char_cost_values, use_container_width=True)
        with st.expander('Zobacz tabele z danymi'):
            st.dataframe(table_witch_costs[['koszt_poczty', 'koszt_drukow', 'koszt_giftow','nakład',
                                                                       'koszt_konfekcjonowania']])