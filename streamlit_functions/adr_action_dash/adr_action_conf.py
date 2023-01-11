import streamlit as st

import streamlit_functions.adr_action_dash.objects_for_ma_dash.tabs_for_ma_dash as tabs_ma


def main_action_config(data_to_show_ma, show_filter):
    prime = st.container()
    with prime:
        if show_filter == True:
            tab1, tab2, tab3, tab4, tab5 = st.tabs(['Wykres', 'Tabela przestawna', 'Kolumny do wykresu', 'Ustawienie wykresu',
                                    'Filtr danych'])
        else:
            tab1, tab2, tab3, tab4 = st.tabs(['Wykres', 'Tabela przestawna', 'Kolumny do wykresu', 'Ustawienie wykresu'])

        with tab4:
            dictionary_options = tabs_ma.char_options()
        if show_filter == True:
            with tab5:
                filtr_ma = tabs_ma.filtr_mailings(dictionary_options, data_to_show_ma)
        else:
            filtr_ma = []
        with tab3:
            cam_adr_plot_ma, test_pivot_ma = tabs_ma.columns_order(dictionary_options, data_to_show_ma, filtr_ma)
        with tab1:
            st.bokeh_chart(cam_adr_plot_ma, use_container_width=True)
        with tab2:
            st.dataframe(test_pivot_ma, 1200, 400)
            label_of_file = f'dane mailing_adresowy.xlsx'

            #@st.cache
            #def save_file(df):
            #    df.to_excel(f'./generated_files/{label_of_file}', engine='xlsxwriter')

            # todo do poprawienia aby plik nie generowal sie za kazdym razem
            #with open(f"./generated_files/{label_of_file}", "rb") as file:
            #    btn = st.download_button(
            #        label="Download xlsx",
            #        on_click=save_file(test_pivot_ma),
            #        data=file,
            #        file_name="Tabela przestawna z mailingów adresowych.xlsx",
            #        mime="image/png"
            #    )

    return prime
