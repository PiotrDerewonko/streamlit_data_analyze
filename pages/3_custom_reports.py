import streamlit as st
from dotenv import dotenv_values

from database.source_db import deaful_set
from functions_pandas.plot_cam_adr_dash import pivot_and_chart_for_dash
from pages.custom_reports_files.distance_between_first_and_second_pay.distance import \
    distance_between_first_and_second_pay

with st.container():
    sorce_main = dotenv_values('.env')
    sorce_main = list(sorce_main.values())[0]
    mailings, con, engine = deaful_set(f'{sorce_main}')
    refresh_data = 'False'

    st.header("Odległość między pierwszą a drugą wpłatą")

    multindex = st.multiselect(options=['grupa_akcji_1', 'grupa_akcji_2', 'grupa_akcji_3', 'status_first_pay',
                                        'date_part', 'plec', 'okreg_pocztowy', 'good_address'],
                                     label='Prosze wybrac index',
                                     default=['grupa_akcji_1', 'status_first_pay', 'plec'])

    data = distance_between_first_and_second_pay(con, engine, refresh_data)
    default_gr1 = data['grupa_akcji_1'].drop_duplicates()
    gr1 = st.multiselect(options=default_gr1,
                                     label='Prosze wybrac zawezenie danych',
                                     default=default_gr1)
    min_int_sl = 2008
    max_int_sl = int(data['date_part'].max())
    if len(gr1) >= 1:
        data = data[data['grupa_akcji_1'].isin(gr1)]
    year_add_slider = st.slider('Prosze wybrać lata pozyskania korespondentów', min_value=min_int_sl,
                                max_value=max_int_sl, value=[max_int_sl-2, max_int_sl])
    data = data.loc[(data['date_part'] >= year_add_slider[0]) & (data['date_part'] <= year_add_slider[1])]

    last_mailing = st.checkbox(label='Tylko osoby z ostatnim mailingiem Q', value=True)
    positive_adr = st.checkbox(label='Tylko osoby z poprawnym adresem', value=True)
    #TODO TU znalesc dlaczego wysiwtyela sie ten indeks
    if last_mailing == True:
        data = data.loc[data['last_mailing']==True]

    if positive_adr == True:
        data = data.loc[data['good_address']=='poprawny_adres']

    data.dropna(subset=['grupa_akcji_1'], inplace=True)
    data['date_part'] = data['date_part'].astype(int)
    data['date_part'] = data['date_part'].astype(str)
    char, pivot = pivot_and_chart_for_dash(data, multindex, 'dist',
                                           'Odstęp czasu między pierwszą a drugą wpłatą dla osób pozyskanych z lat ',
                                           'źródlo pozyskania', {}, [], [])
    char_stack, pivot_stack = pivot_and_chart_for_dash(data, multindex, 'dist2',
                                           'Odstęp czasu między pierwszą a drugą wpłatą dla osób pozyskanych z lat ',
                                           'źródlo pozyskania', {})
    st.header('Wykres do 100 %')
    st.bokeh_chart(char_stack)
    st.header('Tabela z danymi')
    st.dataframe(pivot)
    st.header('Wykres ilościowy')
    st.bokeh_chart(char)

