import pandas as pd
import streamlit as st

from database.download_data_for_ma_details import data_for_sum_of_amount_in_days
from pages.ma_details_files.download_data_fo_char_line import down_data_sum_and_count, down_data_cost_and_circulation
from pages.ma_details_files.line_charts_for_ma import line_chart_for_m, change_list_to_string
from pages.ma_details_files.roi_szlw_for_ma import roi, profit


def charts(mailing, con, years, refresh_data, engine):
    with st.container():
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Suma Wpłat', 'Liczba Wpłat', 'Stopa zwrotu liczby wplat', 'ROI',
                                                      'Profit', 'Wybór dni'])
        with tab6:
            days_range = st.slider('Proszę wybrać dnia od nadania mailingu', min_value=1, max_value=60,
                                  value=[1, 60])
            cumulative = st.checkbox(label='Wykresy kumulacyjnie', value=True)
            mailings_string = change_list_to_string(mailing, 'dla mailingów')
            years_string = change_list_to_string(years, 'za lata')
            trends = st.selectbox(label='Wybierz mailing do linii trendu', options=[['test', 'test2'], ['test3', 'test4']])

            list_of_id_gr2 = pd.read_sql_query('''select id from fsaps_dictionary_action_group_two 
            where is_for_billing = True order by text''', con).values.tolist()
            list_of_years = pd.read_sql_query('select id from fsaps_dictionary_action_group_three order by text', con).values.tolist()

            #Tabela z nakladem przerzucona wyzej aby moc wyswietlic naklad w innych miejscach
            data_cost_and_circulation = down_data_cost_and_circulation(con, refresh_data, engine, list_of_id_gr2, list_of_years)
            pivot_circ = data_for_sum_of_amount_in_days(mailing, years, 0, 0, 'circ', data_cost_and_circulation,
                                                        cumulative)

            #dane, tabel i wkyres dla liczby wplat
            data_sum_count = down_data_sum_and_count(con, refresh_data, engine)
            pivot_sum_of_amount = data_for_sum_of_amount_in_days(mailing, years, days_range[0], days_range[-1],
                                                                 'sum', data_sum_count, cumulative)
            char_sum_of_amount = line_chart_for_m(pivot_sum_of_amount, f'''Wykres sumy wpłat {mailings_string} {years_string}''',
                                                  'Suma wpłat zł', pivot_circ)

            # dane, tabel i wkyres dla sumy wplat
            pivot_count_amount = data_for_sum_of_amount_in_days(mailing, years, days_range[0], days_range[-1],
                                                                'count', data_sum_count, cumulative)
            char_count_of_amount = line_chart_for_m(pivot_count_amount, f'''Wykres liczby wpłat {mailings_string} {years_string}'''
                                                    , 'Liczba wpłąt', pivot_circ)

            # dane, tabel i wkyres dla roi

            pivot_cost = data_for_sum_of_amount_in_days(mailing, years, 0, 0, 'cost', data_cost_and_circulation,
                                                        cumulative)
            pivot_roi = roi(pivot_sum_of_amount, pivot_cost)
            char_roi = line_chart_for_m(pivot_roi, f'''Wykres ROI {mailings_string} {years_string}''', 'ROI zł', pivot_circ)

            # dane, tabel i wkyres dla szlw

            pivot_szlw = roi(pivot_count_amount, pivot_circ)
            char_szlw = line_chart_for_m(pivot_szlw, f'''Wykres Stopy zwrotu liczby wpłat {mailings_string} {years_string}''',
                                         'Stopa zwrotu liczby wpłat %', pivot_circ)

            #tabela i wykres dla profitu
            pivot_profit = profit(pivot_sum_of_amount, pivot_cost)
            char_profit = line_chart_for_m(pivot_profit, f'''Wykres profitu {mailings_string} {years_string}''',
                                         'Profit zł', pivot_circ)
        with tab5:
            st.bokeh_chart(char_profit, use_container_width=True)
            with st.expander('Zobacz tabele z danymi'):
                st.dataframe(pivot_profit)
        with tab4:
            st.bokeh_chart(char_roi, use_container_width=True)
            with st.expander('Zobacz tabele z danymi'):
                st.dataframe(pivot_roi)
        with tab3:
            st.bokeh_chart(char_szlw, use_container_width=True)
            with st.expander('Zobacz tabele z danymi'):
                st.dataframe(pivot_szlw)
        with tab2:
            st.bokeh_chart(char_count_of_amount, use_container_width=True)
            with st.expander('Zobacz tabele z danymi'):
                st.dataframe(pivot_count_amount)
        with tab1:
            st.bokeh_chart(char_sum_of_amount, use_container_width=True)
            with st.expander('Zobacz tabele z danymi'):
                st.dataframe(pivot_sum_of_amount)
