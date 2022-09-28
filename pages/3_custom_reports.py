import streamlit as st

from database.source_db import deaful_set
from functions_pandas.plot_cam_adr_dash import pivot_and_chart_for_dash
from pages.custom_reports_files.distance_between_first_and_second_pay.distance import \
    distance_between_first_and_second_pay

with st.container():
    sorce_main = 'local'
    st.header("Odległość między pierwszą a drugą wpłatą")
    mailings, con, engine = deaful_set(f'{sorce_main}')
    refresh_data = 'False'
    data = distance_between_first_and_second_pay(con, engine, refresh_data)
    pivot_table = data.pivot_table(values='id_korespondenta', aggfunc='count',
                                   index=['grupa_akcji_1', 'status_first_pay'], columns=['status_second_pay'])
    char, pivot = pivot_and_chart_for_dash(data, ['grupa_akcji_1', 'status_first_pay'], 'dist', 'test', 'text', {} )
    st.dataframe(pivot)
    st.bokeh_chart(char)
    print('test')