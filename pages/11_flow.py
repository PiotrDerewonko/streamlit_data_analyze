import streamlit as st

from pages.flow.create_data import download_data_about_flow, filtr_data_about_flow, transform_data_about_flow
from pages.flow.create_flow_chart import create_flow_chart

with st.container():
    #pobieram dane
    data_first = download_data_about_flow(False)

    #filtruje dane
    data_filtered = filtr_data_about_flow(data_first, {})

    #transformacja_danych
    data_to_pivot = transform_data_about_flow(data_filtered)

    st.dataframe(data_to_pivot, hide_index=True)

    #dodaje wykres
    chart = create_flow_chart(data_to_pivot)
    st.plotly_chart(chart, use_container_width=True)
