import streamlit as st

from database.download_data_for_ma_details import data_for_sum_of_amount_in_days


def charts(data_to_show, mailing, con, years):
    with st.container():
        tab1, tab2, tab3, tab4, tab5 = st.tabs(['Suma Wpłat', 'Liczba Wpłat', 'Stopa zwrotu liczby wplat', 'ROI', 'Wybór dni'])
        with tab5:
            days_range = st.slider('Proszę wybrać dnia od nadania mailingu', min_value=1, max_value=60,
                                  value=[1, 60])
            pivot = data_for_sum_of_amount_in_days(mailing, years, days_range[0], days_range[-1], con, 'sum')
            st.dataframe(pivot)
