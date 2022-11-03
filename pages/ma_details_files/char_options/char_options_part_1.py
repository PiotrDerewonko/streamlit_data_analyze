import streamlit as st

def char_options_part1():
    with st.container():
        test = {'sw': True}

        def create_df(data_all, label, value):
            data_all[f'{label}'] = value
        c1, c2, c3, c4 = st.columns(4)
        list_of_objects =[[c1, 'sw', 'Suma wpłat', 'swax', 'Oś dla sumy wpłat', ['Oś główna', 'Oś pomocnicza'],
                           'swchar', 'Rodzaj wykresu dla Sumy wpłat', ['Słupkowy', 'Liniowy'], True],
                          [c2, 'lw', 'Liczba wpłat', 'lwax', 'Oś dla liczby wpłat', ['Oś pomocnicza', 'Oś główna'],
                           'lwchar', 'Rodzaj wykresu dla Liczby wpłat', ['Liniowy', 'Słupkowy'], True],
                          [c3, 'kc', 'Koszt', 'kcax', 'Oś dla kosztu', ['Oś główna', 'Oś pomocnicza'],
                           'kcchar', 'Rodzaj wykresu dla Kosztu', ['Słupkowy', 'Liniowy'], True],
                          [c4, 'nc', 'Nakład', 'ncax', 'Oś dla nakładu', ['Oś pomocnicza', 'Oś główna'],
                           'ncchar', 'Rodzaj wykresu dla Nakładu', ['Liniowy', 'Słupkowy'], True]]

        for x in list_of_objects:
            if x[1] not in st.session_state:
                st.session_state[x[1]] = x[9]
        for i in list_of_objects:
            with i[0]:
                i[1] = st.checkbox(i[2], value=i[9], on_change=create_df(test, i[1], st.session_state.sw))
                i[3] = st.selectbox(i[4], i[5])
                i[6] = st.selectbox(i[7], i[8])

        st.markdown(test)


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