import pandas as pd
import streamlit as st

import pages.ma_details_files.char_options.advance_options as ch_2
import pages.ma_details_files.char_options.basic_options as ch_1


def char_options_part1():
    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        axis_1 = ['Oś główna', 'Oś pomocnicza']
        axis_2 = ['Oś pomocnicza', 'Oś główna']
        char_1 = ['Wykres Słupkowy', 'Wykres liniowy']
        char_2 = ['Wykres liniowy', 'Wykres Słupkowy']
        list_of_objects =[[c1, 'suma_wplat', 'Suma wpłat', 'swax', 'Oś dla sumy wpłat', axis_1,
                           'swchar', 'Rodzaj wykresu dla Sumy wpłat', char_1, True],
                          [c2, 'liczba_wplat', 'Liczba wpłat', 'lwax', 'Oś dla liczby wpłat', axis_2,
                           'lwchar', 'Rodzaj wykresu dla Liczby wpłat', char_2, True],
                          [c3, 'koszt', 'Koszt', 'kcax', 'Oś dla kosztu', axis_1,
                           'kcchar', 'Rodzaj wykresu dla Kosztu', char_1, True],
                          [c4, 'naklad', 'Nakład', 'ncax', 'Oś dla nakładu', axis_2,
                           'ncchar', 'Rodzaj wykresu dla Nakładu', char_2, True]]

        for x in list_of_objects:
            if x[1] not in st.session_state:
                st.session_state[x[1]] = x[9]
            if x[3] not in st.session_state:
                st.session_state[x[3]] = x[5][0]
            if x[6] not in st.session_state:
                st.session_state[x[6]] = x[8][0]
        with c1:
            sw_dict, sw_df = ch_1.options_col1_suma_wplat(axis_1, char_1)
        with c2:
            lw_dict, lw_df = ch_1.options_col1_liczba_wplat(axis_1, char_1)
        with c3:
            n_dict, n_df = ch_1.options_col1_naklad(axis_1, char_1)
        with c4:
            k_dict, k_df = ch_1.options_col1_koszt(axis_1, char_1)

        test_df = pd.DataFrame()
        test_df = pd.concat([test_df, sw_df, lw_df, n_df, k_df])
        return test_df

def char_options_part2():
    with st.container():
        axis_1 = ['Oś główna', 'Oś pomocnicza']
        axis_2 = ['Oś pomocnicza', 'Oś główna']
        char_1 = ['Wykres Słupkowy', 'Wykres liniowy']
        char_2 = ['Wykres liniowy', 'Wykres Słupkowy']
        c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)
        list_of_objects =[[c1, 'ROI', 'ROI', 'roiax', 'Oś dla ROI', axis_1,
                           'roichar', 'Rodzaj wykresu dla ROI', char_1, False],
                          [c2, 'SZLW', 'Stopa zwrtur lw', 'szlwax', 'Oś dla SZLW', axis_1,
                           'szlwchar', 'Rodzaj wykresu dla SZLW', char_1, False],
                          [c3, 'Pierwszy_percentyl', '1 percentyl', 'pier_pax', 'Oś dla 1 percentyl', axis_2,
                           'pier_pchar', 'Rodzaj wykresu dla 1 percentylu', char_2, False],
                          [c4, 'mediana', 'Mediana', 'medax', 'Oś dla Mediany', axis_2,
                           'medchar', 'Rodzaj wykresu dla Medainy', char_2, False],
                          [c5, 'Trzeci_percentyl', '3 percentyl', 'trzec_pax', 'Oś dla 3 Percentyl', axis_2,
                           'trzec_pchar', 'Rodzaj wykresu dla 3 percentyl', char_2, False],
                          [c6, 'Odchylenie', 'Odchylenie std', 'stdax', 'Oś dla Odchylenie Std', axis_2,
                           'stdchar', 'Rodzaj wykresu dla Odchylenie Std', char_2, False],
                          [c7, 'średnia', 'Średnia wpłata', 'avgax', 'Oś dla Średniej',
                           axis_2,
                           'avgchar', 'Rodzaj wykresu dla Średniej', char_2, False],
                          [c8, 'Koszt_na_głowę', 'Koszt na głowę', 'kngdax', 'Oś dla Kosztu na głowę',
                           axis_2,
                           'kngchar', 'Rodzaj wykresu dla Kosztu na głowę', char_2, False]
                          ]
        for x in list_of_objects:
            if x[1] not in st.session_state:
                st.session_state[x[1]] = x[9]
            if x[3] not in st.session_state:
                st.session_state[x[3]] = x[5][0]
            if x[6] not in st.session_state:
                st.session_state[x[6]] = x[8][0]

        with c1:
            roi_dict, roi_df = ch_2.options_col1_roi(axis_1, char_1)
        with c2:
            szlw_dict, szlw_df = ch_2.options_col1_szlw(axis_1, char_1)
        with c3:
            pier_perc_dict, pier_perc_df = ch_2.options_col1_1_perc(axis_1, char_1)
        with c4:
            mediana_dict, mediana_df = ch_2.options_col1_mediana(axis_1, char_1)
        with c5:
            trzeci_per_dict, trzeci_per_df = ch_2.options_col1_3_perc(axis_1, char_1)
        with c6:
            std_dict, std_df = ch_2.options_col1_std(axis_1, char_1)
        with c7:
            avg_dict, avg_df = ch_2.options_col1_avg(axis_1, char_1)
        with c8:
            kng_dict, kng_df = ch_2.options_col1_kng(axis_1, char_1)

        test_df = pd.DataFrame()
        test_df = pd.concat([test_df, roi_df, szlw_df, pier_perc_df, mediana_df, trzeci_per_df, std_df, avg_df,
                                 kng_df])
        return test_df
