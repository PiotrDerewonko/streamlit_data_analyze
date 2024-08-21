import streamlit as st
from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.ma_details_files.charts_in_days.charts_in_days_basic import ChartsInDays
from pages.ma_details_files.charts_in_days.helper_functions import CreatePivotTableAndChart
from pages.ma_details_files.choose_options import ChooseOptions
from pages.ma_details_files.column_order import distinct_columns

with st.container():
    sorce_main = dotenv_values('.env')
    sorce_main = list(sorce_main.values())[0]
    mailings, con, engine = deaful_set(f'{sorce_main}')

    # wybor ktorych mailingow ma dotyczyc analiza
    class_options = ChooseOptions(con)
    qamp, years, type_of_campaign = class_options.choose_options()

    # wybor jakie dane maja znalesc sie na wykresie
    option_list = distinct_columns()
    choosed_options = st.multiselect(options=option_list, default=['grupa_akcji_2_wysylki', 'grupa_akcji_3_wysylki'],
                                     label='Wybierz dane do wykresu')

    # wybor opcji do wykresow
    ChartsInDaysBasic = ChartsInDays(mailings, con, years, False, engine)
    days_range, cumulative, new_old, chose_new_old, tab1, tab2, tab3, tab4, tab5 = ChartsInDaysBasic.create_tabs()
    ChartsInDaysBasic.download_data()

    # tworzenie tabeli przestwnej i wykresu dla sumy wplat
    SumAmount = CreatePivotTableAndChart(tab1, qamp, years, days_range[0], days_range[-1],
                                         ChartsInDaysBasic.data_sum_count,
                                         cumulative, new_old, chose_new_old, 'suma_wplat')
    pivot_table_sum_amount, list_of_columns_sum_amount = SumAmount.create_pivot_table()
    pivot_table_sum_amount = SumAmount.change_pivot_table(pivot_table_sum_amount, list_of_columns_sum_amount)
    pivot_table_sum_amount = SumAmount.customize_pivot_table_(pivot_table_sum_amount)
    SumAmount.put_data_into_streamlit(pivot_table_sum_amount)

    # tworzenie tabeli przestwnej i wykresu dla liczby wplat
    CountAmount = CreatePivotTableAndChart(tab2, qamp, years, days_range[0], days_range[-1],
                                           ChartsInDaysBasic.data_sum_count,
                                           cumulative, new_old, chose_new_old, 'liczba_wplat')
    pivot_table_count_amount, list_of_columns_count_amount = CountAmount.create_pivot_table()
    pivot_table_count_amount = CountAmount.change_pivot_table(pivot_table_count_amount, list_of_columns_count_amount)
    pivot_table_count_amount = CountAmount.customize_pivot_table_(pivot_table_count_amount)
    CountAmount.put_data_into_streamlit(pivot_table_count_amount)

    # tworzenie tabeli przestawnej dla kosztu
    CostAmount = CreatePivotTableAndChart(None, qamp, years, 1, 1,
                                          ChartsInDaysBasic.data_cost_and_circulation, False, False, None, 'koszt')
    pivot_table_cost_amount, list_of_columns_cost_amount = CostAmount.create_pivot_table()

    #tworznie tabeli przestwnej dla nakladu
    CircAmount = CreatePivotTableAndChart(None, qamp, years, 1, 1,
                                          ChartsInDaysBasic.data_cost_and_circulation, False, False, None, 'naklad')
    pivot_table_circ_amount, list_of_columns_circ_amount = CircAmount.create_pivot_table()

    #tworzenie tabeli przestawnej dla SZLW
    SZLW = CreatePivotTableAndChart(tab3, qamp, years, None, None,None, None,
                                    None, None, None)
    szlw_pivot = SZLW.calculation_roi_or_szlw(pivot_table_count_amount, pivot_table_circ_amount, 'div')
    SZLW.put_data_into_streamlit(szlw_pivot)

    #tworzenie tabeli przestawnej dla ROI
    ROI = CreatePivotTableAndChart(tab4, qamp, years, None, None,None, None,
                                    None, None, None)
    szlw_pivot = ROI.calculation_roi_or_szlw(pivot_table_sum_amount, pivot_table_cost_amount, 'div')
    ROI.put_data_into_streamlit(szlw_pivot)

    #tworzenie tabeli przestawnej dla profitu
    profit = CreatePivotTableAndChart(tab5, qamp, years, None, None,None, None,
                                    None, None, None)
    profit_pivot = profit.calculation_roi_or_szlw(pivot_table_sum_amount, pivot_table_cost_amount, 'subtract')
    profit.put_data_into_streamlit(profit_pivot)


