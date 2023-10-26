import numpy as np
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
           when tk.id_typu_korespondenta in (7,8) then 'Zbiórka przykościelna'
else 'Pozostałe' end as typ
from t_transakcje tr
left outer join t_aktywnosci_korespondentow tak on tr.id_transakcji = tak.id_transakcji
left outer join t_akcje ta on tak.id_akcji = ta.id_akcji
left outer join t_grupy_akcji_1 t on ta.id_grupy_akcji_1 = t.id_grupy_akcji_1
left outer join t_grupy_akcji_2 a on a.id_grupy_akcji_2 = ta.id_grupy_akcji_2
left outer join t_grupy_akcji_3 gr3 on ta.id_grupy_akcji_3 = gr3.id_grupy_akcji_3
left outer join t_korespondenci tk on tr.id_korespondenta = tk.id_korespondenta
group by rok, miesiac, typ)a'''
    data = pd.read_sql_query(sql, con)
    list_options = list(data['typ'].drop_duplicates())

    with st.sidebar:
        year_range_slider = st.slider('Proszę wybrać lata', min_value=2008, max_value=date.now().year,
                                      value=[date.now().year - 4, date.now().year])
        month_range_slider = st.slider('Proszę wybrać miesiące', min_value=1, max_value=12, value=[1,12])
        choose_type = st.multiselect('Wybierz typ wpłaty', options=list_options, default=list_options)

    year_from = year_range_slider[0]
    year_to = year_range_slider[1]
    month_from = month_range_slider[0]
    month_to = month_range_slider[1]
    data['miesiac'] = data['miesiac'].astype(int)

    data = data.loc[(data['rok'] >= year_from) & (data['rok'] <= year_to) &
                    (data['miesiac'] >= month_from) & (data['miesiac'] <= month_to)]

    data['rok'] = data['rok'].astype(str)
    data['miesiac'] = data['miesiac'].astype(str)
    columns_options = st.multiselect(options=['rok', 'miesiac'], default=['rok'],
                                     label='Prosze wybrać dane do układu')
    pivot = pd.pivot_table(data.loc[data['typ'].isin(choose_type)], index=columns_options, values='suma_wplat', columns='typ', aggfunc='sum')
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

    char_options_df_weeks = pd.DataFrame(columns=['Nazwa parametru', 'oś', 'Opcje'])
    for i in range(0, len(pivot.columns)):
        tmp = pd.DataFrame(data={'Nazwa parametru': pivot.columns[i], 'oś': 'Oś główna', 'Opcje': 'Wykres Słupkowy Skumulowany'}, index=[i])
        char_options_df_weeks = pd.concat([char_options_df_weeks, tmp])
    dict_of_oriantation = {'major': 'vertical', 'group': 'vertical', 'sub_group': 'vertical'}

    char_finance, aa = pivot_and_chart_for_dash(data, columns_options, 'me_detail', 'test tytulu',
                                          'Rok/miesiąc', {}, pivot, char_options_df_weeks, 'Suma wpłat w podziale na źrodło darowizny',
                                               dict_of_oriantation
                                          )
    char_finance_to100, aaa = pivot_and_chart_for_dash(data, columns_options, 'me_detail', 'test tytulu',
                                          'Rok/miesiąc', {}, pivot_cum, char_options_df_weeks, 'Suma wpłat w podziale na źrodło darowizny',
                                               dict_of_oriantation
                                          )
    tab1, tab2, tab3 = st.tabs(['Suma wpłat', 'Struktura wpłat', 'ROI'])
    with tab1:
        st.bokeh_chart(char_finance, use_container_width=True)
        with st.expander('Kliknij i zobacz dane'):
            st.dataframe(pivot)
    with tab2:
        st.bokeh_chart(char_finance_to100)
        with st.expander('Kliknij i zobacz dane'):
            st.dataframe(pivot_cum, use_container_width=True)
    with tab3:
        switch = st.checkbox(label='Zamieś kolejność', value=True)
        if switch:
            switch_value = ['rok', 'typ']
        else:
            switch_value = ['typ', 'rok']
        sql ='''select koszt as suma_wplat, rok::int, typ from (
select sum(koszt_calkowity) as koszt, grupa_akcji_3 as rok,
       case when ta.id_grupy_akcji_2 in (9,10,11,12,24,67,100) then a.grupa_akcji_2
when ta.id_grupy_akcji_1 in (22, 24) then 'Druki i prawdopodobne druki'
           when ta.id_grupy_akcji_2 in (15) then 'Zbiórka przykościelna'
else 'Pozostałe' end as typ
from v_akcje_naklad_koszt_calkowity_szczegolowa tak
left outer join t_akcje ta on tak.id_akcji = ta.id_akcji
left outer join t_grupy_akcji_1 t on ta.id_grupy_akcji_1 = t.id_grupy_akcji_1
left outer join t_grupy_akcji_2 a on a.id_grupy_akcji_2 = ta.id_grupy_akcji_2
left outer join t_grupy_akcji_3 gr3 on ta.id_grupy_akcji_3 = gr3.id_grupy_akcji_3
group by rok,  typ)a'''
        cost_data = pd.read_sql_query(sql, con)
        cost_data.dropna(inplace=True)
        cost_data = cost_data.loc[(cost_data['rok'] >= year_from) & (cost_data['rok'] <= year_to)]
        cost_data['rok'] = cost_data['rok'].astype(str)
        pivot_pay_year = pd.pivot_table(data.loc[data['typ'].isin(choose_type)], index=switch_value, values='suma_wplat',
                                aggfunc='sum')
        pivot_cost_year = pd.pivot_table(cost_data.loc[cost_data['typ'].isin(choose_type)], index=switch_value, values='suma_wplat',
                                aggfunc='sum')
        pivot_cost_year.fillna(0, inplace=True)
        pivot_pay_year.fillna(0, inplace=True)
        pivot_dev = pivot_pay_year.div(pivot_cost_year)
        char_options_df_weeks = pd.DataFrame(columns=['Nazwa parametru', 'oś', 'Opcje'])
        pivot_dev.rename({'suma_wplat': 'ROI'}, axis=1, inplace=True)
        for i in range(0, len(pivot_dev.columns)):
            tmp = pd.DataFrame(
                data={'Nazwa parametru': pivot_dev.columns[i], 'oś': 'Oś główna', 'Opcje': 'Wykres Słupkowy'},
                index=[i])
            char_options_df_weeks = pd.concat([char_options_df_weeks, tmp])
        pivot_dev.replace([np.inf, -np.inf], 0, inplace=True)
        pivot_dev.reset_index(inplace=True)
        pivot_dev['rok'] = pivot_dev['rok'].astype(str)
        pivot_dev.set_index(switch_value, inplace=True)
        roi, aa = pivot_and_chart_for_dash(cost_data, switch_value, 'me_detail', 'test tytulu',
                                                    'Rok/miesiąc', {}, pivot_dev, char_options_df_weeks,
                                                    'Suma wpłat w podziale na źrodło darowizny',
                                                    dict_of_oriantation
                                                    )
        st.bokeh_chart(roi, use_container_width=True)
        with st.expander('Kiknij i zobacz dane'):
            st.dataframe(pivot_dev)