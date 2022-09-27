import streamlit as st

from database.source_db import deaful_set
from pages.custom_reports_files.distance_between_first_and_second_pay.distance import \
    distance_between_first_and_second_pay

with st.container():
    sorce_main = 'local'
    st.header("Odległość między pierwszą a drugą wpłatą")
    mailings, con, engine = deaful_set(f'{sorce_main}')
    refresh_data = 'True'
    distance_between_first_and_second_pay(con, engine, refresh_data)