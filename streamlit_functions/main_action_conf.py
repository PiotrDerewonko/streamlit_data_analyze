import pandas as pd
import streamlit as st
from functions.plot_cam_adr_dash import pivot_and_chart_for_dash
import xlsxwriter
from datetime import datetime
from streamlit_functions.create_df_for_pivot import create_df
from streamlit_functions.dashboard.initialization import create_dictionary, create_session_state_key

def a(data_to_show_ma):
    prime = st.container()
    with prime:
        tab1, tab2, tab3 = st.tabs(['Wykres', 'Tabela przestawna', 'Kolumny do wykresu'])
        with tab3:
            with st.container():
                levels_ma = st.multiselect(options=['grupa_akcji_3', 'grupa_akcji_2'],
                                           label='Proszę wybrać kolejność kolumn',
                                           default=['grupa_akcji_3', 'grupa_akcji_2'])

                with st.container():
                    st.caption("Prosze wybrać parametry które maja znaleść sie na wykresie")
                    c1, c2, c3, c4, c5, c6 = st.columns(6)
                    dictionary_options = create_dictionary()
                    create_session_state_key()
                    with c1:
                        sc = st.checkbox('Suma wpłat', value=True, on_change=create_df(dictionary_options, 'sw', st.session_state.sw), key='sw')
                        st.write(st.session_state.sw)
                        sw_axis = st.selectbox(options=['Oś główna', 'Oś pomocnicza'],
                                               label='Rodzaj wykresu dla sumy wpłat')
                        sw_char = st.selectbox(options=['Wykres Słupkowy', 'Wykres liniowy'],
                                               label='Oś dla sumy wplat')


                    with c2:
                        lc = st.checkbox('Liczba wpłat', value=True, on_change=create_df(dictionary_options, 'lw',
                                                                                         st.session_state.lw), key='lw')
                        st.write(st.session_state.lw)
                        lw_axis = st.selectbox(options=['Oś pomocnicza', 'Oś główna'], label='Rodzaj wykresu dla liczby wpłat')
                        lw_char = st.selectbox(options=['Wykres Słupkowy', 'Wykres liniowy'], label='Oś dla liczby wplat')
                    with c3:
                        nc = st.checkbox('Nakład całkowity', value=True, on_change=create_df(dictionary_options, 'nc',
                                                                                             st.session_state.nc), key='nc')
                        sw_axis = st.selectbox(options=['Oś pomocnicza', 'Oś główna'], label='Rodzaj wykresu dla nakładu')
                        sw_char = st.selectbox(options=['Wykres liniowy', 'Wykres Słupkowy'], label='Oś dla nakładu')
                    with c4:
                        kc = st.checkbox('Koszt całkowity', value=True, on_change=create_df(dictionary_options, 'kc',
                                                                                            st.session_state.kc), key='kc')
                        lw_axis = st.selectbox(options=['Oś pomocnicza', 'Oś główna'], label='Rodzaj wykresu dla kosztu')
                        lw_char = st.selectbox(options=['Wykres liniowy', 'Wykres Słupkowy'], label='Oś dla kosztu')
                    with c5:
                        rc = st.checkbox('ROI', on_change=create_df(dictionary_options, 'roi', st.session_state.roi),
                                         key='roi')
                        sw_axis = st.selectbox(options=['Oś pomocnicza', 'Oś główna'], label='Rodzaj wykresu dla ROI')
                        sw_char = st.selectbox(options=['Wykres liniowy', 'Wykres Słupkowy'], label='Oś dla ROI')
                    with c6:
                        rs = st.checkbox('Stopa Zwrotu L. Wpłat', on_change=create_df(dictionary_options, 'szlw',
                                                                                      st.session_state.szlw), key='szlw')
                        lw_axis = st.selectbox(options=['Oś pomocnicza', 'Oś główna'], label='Rodzaj wykresu dla SZLW')
                        lw_char = st.selectbox(options=['Wykres liniowy', 'Wykres Słupkowy'], label='Oś dla SZLW')
                st.markdown(dictionary_options)
                cam_adr_plot_ma, test_pivot_ma = pivot_and_chart_for_dash(data_to_show_ma, levels_ma, 'address',
                                                                          'Wyniki mailingów adresowych za lata ',
                                                                          'Malingi', 'Suma wpłat/Koszt',
                                                                          'Nakład/Liczba wpłat')

        with tab1:
            st.bokeh_chart(cam_adr_plot_ma)
        with tab2:
            st.dataframe(test_pivot_ma, 900, 400)
            label_of_file = f'dane mailing_adresowy.xlsx'

            @st.cache
            def save_file(df):
                df.to_excel(f'./generated_files/{label_of_file}', engine='xlsxwriter')

            data = save_file(test_pivot_ma)

            # todo do poprawienia aby plik nie generowal sie za kazdym razem
            with open(f"./generated_files/{label_of_file}", "rb") as file:
                btn = st.download_button(
                    label="Download xlsx",
                    data=file,
                    file_name="Tabela przestawna z mailingów adresowych.xlsx",
                    mime="image/png"
                )

    return prime
