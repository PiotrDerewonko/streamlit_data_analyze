import streamlit as st
from streamlit_functions.dashboard.create_df_for_pivot import create_df

# todo moze przerobic na funckej for z listy
def column_sum_amount(dictionary_options):
    sc = st.checkbox('Suma wpłat', value=True, on_change=create_df(dictionary_options, "sw",
                                                                   st.session_state.sw),
                     key="sw")
    sw_axis = st.selectbox(options=['Oś główna', 'Oś pomocnicza'],
                           label='Rodzaj wykresu dla sumy wpłat',
                           on_change=create_df(dictionary_options, "sw_axis",
                                               st.session_state.sw_axis),
                           key="sw_axis")
    sw_char = st.selectbox(options=['Wykres Słupkowy', 'Wykres liniowy'],
                           label='Oś dla sumy wplat',
                           on_change=create_df(dictionary_options, "sw_char",
                                               st.session_state.sw_char)
                           , key="sw_char")

def column_count_amount(dictionary_options):
    lc = st.checkbox('Liczba wpłat', value=True, on_change=create_df(dictionary_options, 'lw',
                                                                     st.session_state.lw), key='lw')
    lw_axis = st.selectbox(options=['Oś pomocnicza', 'Oś główna'],
                           label='Rodzaj wykresu dla liczby wpłat',
                           key='lw_axis',
                           on_change=create_df(dictionary_options, "lw_axis",
                                               st.session_state.lw_axis)
                           )
    lw_char = st.selectbox(options=['Wykres Słupkowy', 'Wykres liniowy'],
                           label='Oś dla liczby wplat',
                           key='lw_char',
                           on_change=create_df(dictionary_options, "lw_char",
                                               st.session_state.lw_char)
                           )

def circulation(dictionary_options):
    nc = st.checkbox('Nakład całkowity', value=True, on_change=create_df(dictionary_options, 'nc',
                                                                         st.session_state.nc),
                     key='nc')
    nc_axis = st.selectbox(options=['Oś pomocnicza', 'Oś główna'],
                           label='Rodzaj wykresu dla nakładu',
                           key='nc_axis',
                           on_change=create_df(dictionary_options, "nc_axis",
                                               st.session_state.nc_axis)
                           )
    nc_char = st.selectbox(options=['Wykres liniowy', 'Wykres Słupkowy'], label='Oś dla nakładu',
                           key='nc_char',
                           on_change=create_df(dictionary_options, "nc_char",
                                               st.session_state.nc_char))

def cost(dictionary_options):
    kc = st.checkbox('Koszt całkowity', value=True, on_change=create_df(dictionary_options, 'kc',
                                                                        st.session_state.kc),
                     key='kc')
    kc_axis = st.selectbox(options=['Oś główna', 'Oś pomocnicza'],
                           label='Rodzaj wykresu dla kosztu',
                           key='kc_axis',
                           on_change=create_df(dictionary_options, "kc_axis",
                                               st.session_state.kc_axis)
                           )
    kc_char = st.selectbox(options=['Wykres liniowy', 'Wykres Słupkowy'], label='Oś dla kosztu',
                           key='kc_char',
                           on_change=create_df(dictionary_options, "kc_char",
                                               st.session_state.kc_char)
                           )

def roi(dictionary_options):
    rc = st.checkbox('ROI', on_change=create_df(dictionary_options, 'roi', st.session_state.roi),
                     key='roi')
    roi_axis = st.selectbox(options=['Oś pomocnicza', 'Oś główna'], label='Rodzaj wykresu dla ROI',
                            key='roi_axis',
                            on_change=create_df(dictionary_options, "roi_axis",
                                                st.session_state.roi_axis))
    roi_char = st.selectbox(options=['Wykres liniowy', 'Wykres Słupkowy'], label='Oś dla ROI',
                            key='roi_char',
                            on_change=create_df(dictionary_options, "roi_char",
                                                st.session_state.roi_char))

def szlw(dictionary_options):
    rs = st.checkbox('Stopa Zwrotu L. Wpłat', on_change=create_df(dictionary_options, 'szlw',
                                                              st.session_state.szlw),
                 key='szlw')
    szlw_axis = st.selectbox(options=['Oś pomocnicza', 'Oś główna'],
                             label='Rodzaj wykresu dla SZLW',
                             key='szlw_axis',
                             on_change=create_df(dictionary_options, "szlw_axis",
                                                 st.session_state.szlw_axis)
                             )


    szlw_char = st.selectbox(options=['Wykres liniowy', 'Wykres Słupkowy'], label='Oś dla SZLW',
                         key='szlw_char',
                         on_change=create_df(dictionary_options, "szlw_char",
                                             st.session_state.szlw_char)
                         )