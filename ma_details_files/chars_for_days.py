import streamlit as st

from database.download_data_for_ma_details import data_for_sum_of_amount_in_days
from pages.ma_details_files.download_data_fo_char_line import down_data
from pages.ma_details_files.line_charts_for_ma import line_chart_for_m


def charts(mailing, con, years, refresh_data, engine):
    with st.container():
        tab1, tab2, tab3, tab4, tab5 = st.tabs(['Suma Wpłat', 'Liczba Wpłat', 'Stopa zwrotu liczby wplat', 'ROI', 'Wybór dni'])
        with tab5:
            days_range = st.slider('Proszę wybrać dnia od nadania mailingu', min_value=1, max_value=60,
                                  value=[1, 60])
            cumulative = st.checkbox(label='Wykresy kumulacyjnie', value=True)
            data_sum_count = down_data(con, refresh_data, engine)
            pivot_sum_of_amount = data_for_sum_of_amount_in_days(mailing, years, days_range[0], days_range[-1],
                                                                 'sum', data_sum_count, cumulative)
            char_sum_of_amount = line_chart_for_m(pivot_sum_of_amount)
            pivot_count_amount = data_for_sum_of_amount_in_days(mailing, years, days_range[0], days_range[-1],
                                                                'count', data_sum_count, cumulative)
            char_count_of_amount = line_chart_for_m(pivot_count_amount)

        with tab2:
            st.bokeh_chart(char_count_of_amount)
            with st.expander('Zobacz tabele'):
                st.dataframe(pivot_count_amount)
        with tab1:
            st.bokeh_chart(char_sum_of_amount)
