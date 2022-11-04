import pandas as pd
import streamlit as st
from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.ma_details_files.char_options.char_options import char_options
from pages.ma_details_files.chars_for_days import charts
from pages.ma_details_files.chose_campaign import choose
from pages.ma_details_files.column_order import column_options
from pages.ma_details_files.pivot_table_for_ma import create_pivot_table

sorce_main = dotenv_values('.env')
sorce_main = list(sorce_main.values())[0]
mailings, con, engine = deaful_set(f'{sorce_main}')
refresh_data = 'False'

st.header('Analiza głównych mailingów adresowych ')
with st.container():
    qamp, years = choose()
    st.header('Wersje z wybranych mailingów ')
    tab1, tab2, tab3, tab4, tab5 = st.tabs(['Wykres', 'Tabela przestawna', 'Korelacje', 'Kolejność kolumn', 'Opcje wykresu'])
    with tab5:
        options_char = char_options()
    with tab4:
        columns_options, corr_method = column_options(con)

        def create_pivot():
            options_data_frame = pd.DataFrame(data=options_char)
            data, char_corr, data_values, char_default = create_pivot_table(con, refresh_data, engine, qamp, years,
                                                                            columns_options, corr_method, options_data_frame
                                                                            )
            st.dataframe(data)


            with tab3:
                st.pyplot(char_corr)
            with tab1:
                st.bokeh_chart(char_default)
        test = st.button('Przelicz dane')


    with tab2:
        if test:
            create_pivot()
    st.header('Wykresy w dniach od nadania')
    charts(qamp, con, years, refresh_data, engine)

    st.header('Struktura kosztów')
