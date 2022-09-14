import streamlit as st
from functions.plot_cam_adr_dash import pivot_and_chart_for_dash
def a(data_to_show_ma):
    prime = st.container()
    with prime:
        tab1, tab2, tab3 = st.tabs(['Wykres', 'Tabela przestawna', 'Kolumny do wykresu'])
        with tab3:
            with st.container():
                levels_ma = st.multiselect(options=['grupa_akcji_3', 'grupa_akcji_2'],
                                           label='Proszę wybrać kolejność kolumn',
                                           default=['grupa_akcji_3', 'grupa_akcji_2'])
                cam_adr_plot_ma, test_pivot_ma = pivot_and_chart_for_dash(data_to_show_ma, levels_ma, 'address',
                                                                          'Wyniki mailingów adresowych za lata ',
                                                                          'Malingi', 'Suma wpłat/Koszt',
                                                                          'Nakład/Liczba wpłat')
                with st.container():
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.caption("Prosze wybrać parametry które maja znaleść sie na wykresie")
                        st.checkbox('Suma wpłat', value=True)
                        st.checkbox('Liczba wpłat', value=True)
                        st.checkbox('Nakład całkowity', value=True)
                        st.checkbox('Koszt całkowity', value=True)
                        st.checkbox('ROI')
                        st.checkbox('Stopa Zwrotu Liczby Wpłat')
                    with c2:
                        a = st.selectbox(options=['Oś pomocnicza', 'Oś główna'], label='a')
                        b = st.selectbox(options=['Oś pomocnicza', 'Oś główna'], label='b')
                        c = st.selectbox(options=['Oś pomocnicza', 'Oś główna'], label='c')

        with tab1:
            st.bokeh_chart(cam_adr_plot_ma)
        with tab2:
            st.dataframe(test_pivot_ma, 900, 400)
    return prime