import pandas as pd
import streamlit as st
from dotenv import dotenv_values
sorce_main = dotenv_values('.env')
sorce_main = list(sorce_main.values())[0]
from functions_pandas.plot_cam_adr_dash import pivot_and_chart_for_dash
from database.source_db import deaful_set
mailings, con, engine = deaful_set(f'{sorce_main}')
refresh_data = 'False'
from datetime import datetime as date
with st.container():
    sql = '''select suma_wplat, rok, case when miesiac<10 then '0'||(miesiac)::text else miesiac::text end as miesiac, typ from (
select sum(kwota) as suma_wplat, date_part('year', data_wplywu_srodkow) as rok,
 date_part('month', data_wplywu_srodkow) as miesiac,
       case when ta.id_grupy_akcji_2 in (9,10,11,12,24,67,100) then a.grupa_akcji_2
when ta.id_grupy_akcji_1 in (22, 24) then 'Druki i prawdopodobne druki'
else 'Pozostałe' end as typ
from t_transakcje tr
left outer join t_aktywnosci_korespondentow tak on tr.id_transakcji = tak.id_transakcji
left outer join t_akcje ta on tak.id_akcji = ta.id_akcji
left outer join t_grupy_akcji_1 t on ta.id_grupy_akcji_1 = t.id_grupy_akcji_1
left outer join t_grupy_akcji_2 a on a.id_grupy_akcji_2 = ta.id_grupy_akcji_2
left outer join t_grupy_akcji_3 gr3 on ta.id_grupy_akcji_3 = gr3.id_grupy_akcji_3
group by rok, miesiac, typ)a'''
    data = pd.read_sql_query(sql, con)


    with st.sidebar:
        year_range_slider = st.slider('Proszę wybrać lata', min_value=2008, max_value=date.now().year,
                                      value=[date.now().year - 4, date.now().year])

    year_from = year_range_slider[0]
    year_to = year_range_slider[1]


    data = data.loc[(data['rok'] >= year_from) & (data['rok'] <= year_to)]

    data['rok'] = data['rok'].astype(str)
    data['miesiac'] = data['miesiac'].astype(str)
    columns_options = st.multiselect(options=['rok', 'miesiac'], default=['rok'],
                                     label='Prosze wybrać dane do układu')
    pivot = pd.pivot_table(data, index=columns_options, values='suma_wplat', columns='typ', aggfunc='sum')
    list_of_columns = pivot.columns
    pivot_cum = pivot.copy()
    pivot_cum.fillna(0, inplace=True)
    pivot_cum['sum'] = 0
    for j in list_of_columns:
        pivot_cum['sum'] = pivot_cum['sum'] + pivot_cum[j]
    for k in list_of_columns:
        pivot_cum[f'{k}_udzial'] = pivot_cum[k] / pivot_cum['sum']
        pivot_cum.drop(columns=[k], inplace=True)
        pivot_cum.rename(columns={f'{k}_udzial': k}, inplace=True)
    pivot_cum.drop(columns=['sum'], inplace=True)


    char_options_df_weeks = pd.DataFrame(data={'Nazwa parametru': pivot.columns,
                                          'oś': ['Oś główna', 'Oś główna' , 'Oś główna', 'Oś główna', 'Oś główna' ,
                                                 'Oś główna', 'Oś główna', 'Oś główna' , 'Oś główna'],
                                          'Opcje': ['Wykres Słupkowy Skumulowany', 'Wykres Słupkowy Skumulowany',
                                                    'Wykres Słupkowy Skumulowany','Wykres Słupkowy Skumulowany', 'Wykres Słupkowy Skumulowany',
                                                    'Wykres Słupkowy Skumulowany','Wykres Słupkowy Skumulowany', 'Wykres Słupkowy Skumulowany',
                                                    'Wykres Słupkowy Skumulowany']},
                                         index=[0,1,2,3,4,5,6,7,8])
    dict_of_oriantation = {'major': 'vertical', 'group': 'vertical', 'sub_group': 'vertical'}

    char_finance, aa = pivot_and_chart_for_dash(data, columns_options, 'me_detail', 'test tytulu',
                                          'Rok/miesiąc', {}, pivot, char_options_df_weeks, 'Suma wpłat w podziale na źrodło darowizny',
                                               dict_of_oriantation
                                          )
    char_finance_to100, aaa = pivot_and_chart_for_dash(data, columns_options, 'me_detail', 'test tytulu',
                                          'Rok/miesiąc', {}, pivot_cum, char_options_df_weeks, 'Suma wpłat w podziale na źrodło darowizny',
                                               dict_of_oriantation
                                          )
    tab1, tab2 = st.tabs(['Suma wpłat', 'Struktura wpłat'])
    with tab1:
        st.bokeh_chart(char_finance)
        with st.expander('Kliknij i zobacz dane'):
            st.dataframe(pivot)
    with tab2:
        st.bokeh_chart(char_finance_to100)
        with st.expander('Kliknij i zobacz dane'):
            st.dataframe(pivot_cum)