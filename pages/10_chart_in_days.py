import streamlit as st
from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.chart_in_days.ChooseOptionsOverwrite import ChooseOptionsOverwrite
from pages.ma_details_files.charts_in_days.charts_in_days_basic import ChartsInDays
from pages.ma_details_files.charts_in_days.helper_functions import CreatePivotTableAndChart
from pages.ma_details_files.column_order import distinct_columns
from pages.ma_details_files.line_charts_for_ma import change_list_to_string

with st.container():
    sorce_main = dotenv_values('.env')
    sorce_main = list(sorce_main.values())[0]
    mailings, con, engine = deaful_set(f'{sorce_main}')

    # wybor ktorych mailingow ma dotyczyc analiza
    class_options = ChooseOptionsOverwrite(con)
    qamp, years, type_of_campaign = class_options.choose_options()

    # wybor jakie dane maja znalesc sie na wykresie
    option_list = distinct_columns()
    choosed_options = st.multiselect(options=option_list, default=['grupa_akcji_2_wysylki', 'grupa_akcji_3_wysylki'],
                                     label='Wybierz dane do wykresu')
    przelicz_dane = st.button('Wygeneruj dane')

    # wybor opcji do wykresow
    ChartsInDaysBasic = ChartsInDays(mailings, con, years, False, engine)
    days_range, cumulative, new_old, chose_new_old, tab1, tab2, tab3, tab4, tab5, dict_user_choice = ChartsInDaysBasic.create_tabs()

    if przelicz_dane:
        ChartsInDaysBasic.download_data()
        ChartsInDaysBasic.filtr_data_by_user_choise(dict_user_choice)

        # tworze staly element tytulu
        title_basic = change_list_to_string(qamp, 'dla mailingów') + change_list_to_string(years, ' za lata')

        # tworzenie tabeli przestawnej dla kosztu
        CostAmount = CreatePivotTableAndChart(None, qamp, years, 1, 1,
                                              ChartsInDaysBasic.data_cost_and_circulation, False, new_old,
                                              chose_new_old, 'koszt',
                                              choosed_options)
        pivot_table_cost_amount, list_of_columns_cost_amount = CostAmount.create_pivot_table()

        # tworznie tabeli przestwnej dla nakladu
        CircAmount = CreatePivotTableAndChart(None, qamp, years, 1, 1,
                                              ChartsInDaysBasic.data_cost_and_circulation, False, new_old,
                                              chose_new_old, 'naklad',
                                              choosed_options)
        pivot_table_circ_amount, list_of_columns_circ_amount = CircAmount.create_pivot_table()

        # tworzenie tabeli przestwnej i wykresu dla sumy wplat
        SumAmount = CreatePivotTableAndChart(tab1, qamp, years, days_range[0], days_range[-1],
                                             ChartsInDaysBasic.data_sum_count,
                                             cumulative, new_old, chose_new_old, 'suma_wplat', choosed_options)
        pivot_table_sum_amount, list_of_columns_sum_amount = SumAmount.create_pivot_table()
        pivot_table_sum_amount = SumAmount.change_pivot_table(pivot_table_sum_amount, list_of_columns_sum_amount)
        pivot_table_sum_amount = SumAmount.customize_pivot_table_(pivot_table_sum_amount)
        title_sum_amount = ' Wykres sumy wpłat ' + title_basic
        sum_char = SumAmount.create_char_helper_custom(pivot_table_sum_amount, 'Suma wpłat', title_sum_amount,
                                                       pivot_table_circ_amount)
        SumAmount.put_data_into_streamlit(pivot_table_sum_amount, sum_char)

        # tworzenie tabeli przestwnej i wykresu dla liczby wplat
        CountAmount = CreatePivotTableAndChart(tab2, qamp, years, days_range[0], days_range[-1],
                                               ChartsInDaysBasic.data_sum_count,
                                               cumulative, new_old, chose_new_old, 'liczba_wplat', choosed_options)
        pivot_table_count_amount, list_of_columns_count_amount = CountAmount.create_pivot_table()
        pivot_table_count_amount = CountAmount.change_pivot_table(pivot_table_count_amount,
                                                                  list_of_columns_count_amount)
        pivot_table_count_amount = CountAmount.customize_pivot_table_(pivot_table_count_amount)
        title_count_amount = ' Wykres liczby wpłat ' + title_basic
        count_char = CountAmount.create_char_helper_custom(pivot_table_count_amount, 'Liczba wpłat',
                                                           title_count_amount, pivot_table_circ_amount)
        CountAmount.put_data_into_streamlit(pivot_table_count_amount, count_char)

        # tworzenie tabeli przestawnej dla SZLW
        SZLW = CreatePivotTableAndChart(tab3, qamp, years, None, None, None, None,
                                        None, None, None, choosed_options)
        szlw_pivot = SZLW.calculation_roi_or_szlw(pivot_table_count_amount, pivot_table_circ_amount, 'div')
        title_szlw_amount = ' Wykres stopy zwrotu liczby wpłat ' + title_basic
        szlw_char = SZLW.create_char_helper_custom_wo_pivot_class(szlw_pivot, 'Stopa zwrotu liczby wpłat',
                                                                  title_szlw_amount, pivot_table_circ_amount)
        SZLW.put_data_into_streamlit(szlw_pivot, szlw_char)

        # tworzenie tabeli przestawnej dla ROI
        ROI = CreatePivotTableAndChart(tab4, qamp, years, None, None, None, None,
                                       None, None, None, choosed_options)
        roi_pivot = ROI.calculation_roi_or_szlw(pivot_table_sum_amount, pivot_table_cost_amount, 'div')
        title_roi_amount = ' Wykres ROI ' + title_basic
        roi_char = ROI.create_char_helper_custom_wo_pivot_class(roi_pivot, 'ROI',
                                                                title_roi_amount, pivot_table_circ_amount)
        ROI.put_data_into_streamlit(roi_pivot, roi_char)

        # tworzenie tabeli przestawnej dla profitu
        profit = CreatePivotTableAndChart(tab5, qamp, years, None, None, None, None,
                                          None, None, None, choosed_options)
        profit_pivot = profit.calculation_roi_or_szlw(pivot_table_sum_amount, pivot_table_cost_amount, 'subtract')
        title_profit_amount = ' Wykres profitu ' + title_basic
        profit_char = profit.create_char_helper_custom_wo_pivot_class(profit_pivot, 'Profit',
                                                                      title_profit_amount, pivot_table_circ_amount)
        profit.put_data_into_streamlit(profit_pivot, profit_char)
