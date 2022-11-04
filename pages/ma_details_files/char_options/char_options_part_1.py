import pandas as pd
import streamlit as st

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
                           'kcchar', 'Rodzaj wykresu dla Kosztu', char_2, True],
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

        st.markdown(sw_dict)
        st.markdown(lw_dict)
        st.markdown(n_dict)
        test_df = pd.DataFrame()
        test_df = pd.concat([test_df, sw_df, lw_df, n_df, k_df])
        return test_df



        #for i in list_of_objects:
        #    with i[0]:
        #        i[10] = st.checkbox(i[2], value=i[9], on_change=create_df(test, i[1], st.session_state.sw), key=i[1])
        #        i[3] = st.selectbox(i[4], i[5])
        #        i[6] = st.selectbox(i[7], i[8])




def char_options_part2():
    with st.container():
        c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)
        list_of_objects =[[c1, 'roi', 'ROI', 'roiax', 'Oś dla ROI', ['Oś główna', 'Oś pomocnicza'],
                           'swchar', 'Rodzaj wykresu dla ROI', ['Słupkowy', 'Liniowy'], False],
                          [c2, 'szlw', 'Stopa zwrtur lw', 'szlwax', 'Oś dla SZLW', ['Oś pomocnicza', 'Oś główna'],
                           'lwchar', 'Rodzaj wykresu dla SZLW', ['Liniowy', 'Słupkowy'], False],
                          [c3, '1p', '1 percentyl', '1pax', 'Oś dla 1 percentyl', ['Oś główna', 'Oś pomocnicza'],
                           'kcchar', 'Rodzaj wykresu dla 1 percentylu', ['Słupkowy', 'Liniowy'], False],
                          [c4, 'med', 'Mediana', 'medax', 'Oś dla Mediany', ['Oś pomocnicza', 'Oś główna'],
                           'ncchar', 'Rodzaj wykresu dla Medainy', ['Liniowy', 'Słupkowy'], False],
                          [c5, '3p', '3 percentyl', '3pax', 'Oś dla 3 Percentyl', ['Oś pomocnicza', 'Oś główna'],
                           '3pchar', 'Rodzaj wykresu dla 3 percentyl', ['Liniowy', 'Słupkowy'], False],
                          [c6, 'std', 'Odchylenie std', 'stdax', 'Oś dla Odchylenie Std', ['Oś pomocnicza', 'Oś główna'],
                           'stdchar', 'Rodzaj wykresu dla Odchylenie Std', ['Liniowy', 'Słupkowy'], False],
                          [c7, 'avg', 'Średnia wpłata', 'avgax', 'Oś dla Średniej',
                           ['Oś pomocnicza', 'Oś główna'],
                           'avgchar', 'Rodzaj wykresu dla Średniej', ['Liniowy', 'Słupkowy'], False],
                          [c8, 'kng', 'Koszt na głowę', 'kngdax', 'Oś dla Kosztu na głowę',
                           ['Oś pomocnicza', 'Oś główna'],
                           'kngchar', 'Rodzaj wykresu dla Kosztu na głowę', ['Liniowy', 'Słupkowy'], False]
                          ]
        for i in list_of_objects:
            with i[0]:
                i[1] = st.checkbox(i[2], value=i[9])
                i[3] = st.selectbox(i[4], i[5])
                i[6] = st.selectbox(i[7], i[8])