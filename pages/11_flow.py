import streamlit as st

from pages.flow.create_data import download_data_about_flow, create_filter, transform_data_about_flow, filtr_data
from pages.flow.create_flow_chart import create_flow_chart

with st.container():
    st.header("Wykres przepływu darczyńców")

    # tworze filtry
    dictionary = create_filter()

    title = st.text_input(label='Podaj tytuł wykresu')

    reload_data = st.button(label='Przelicz dane')

    tab1, = st.tabs(['Wykres'])


    # Funkcja do przetwarzania danych
    def on_click():
        # pobieram dane
        data_first = download_data_about_flow(False)

        # filtruje dane
        data_filtered = filtr_data(data_first, dictionary)

        # transformacja_danych
        data_to_pivot = transform_data_about_flow(data_filtered)

        # dodaje wykres
        chart = create_flow_chart(data_to_pivot, title)
        st.plotly_chart(chart, use_container_width=True)
        with st.expander('Dane tabelaryczne'):
            st.dataframe(data_to_pivot, hide_index=True)


    if reload_data:
        with tab1:
            on_click()
