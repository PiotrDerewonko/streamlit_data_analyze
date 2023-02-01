import streamlit as st

from streamlit_functions.dashboard.create_df_for_pivot import create_df


def column_sum_amount(dictionary_options):
    sc = st.checkbox('Suma wpłat', value=True, on_change=create_df(dictionary_options, "sw_db",
                                                                   st.session_state.sw_db),
                     key="sw_db")
    sw_axis = st.selectbox(options=['Oś główna', 'Oś pomocnicza'],
                           label='Rodzaj wykresu dla sumy wpłat',
                           on_change=create_df(dictionary_options, "sw_axis_db",
                                               st.session_state.sw_axis_db),
                           key="sw_axis_db")
    sw_char = st.selectbox(options=['Wykres Słupkowy', 'Wykres liniowy'],
                           label='Oś dla sumy wplat',
                           on_change=create_df(dictionary_options, "sw_char_db",
                                               st.session_state.sw_char_db)
                           , key="sw_char_db")

def column_count_amount(dictionary_options):
    lc = st.checkbox('Liczba wpłat', value=True, on_change=create_df(dictionary_options, 'lw_db',
                                                                     st.session_state.lw_db), key='lw_db')
    lw_axis = st.selectbox(options=['Oś pomocnicza', 'Oś główna'],
                           label='Rodzaj wykresu dla liczby wpłat',
                           key='lw_axis_db',
                           on_change=create_df(dictionary_options, "lw_axis_db",
                                               st.session_state.lw_axis_db)
                           )
    lw_char = st.selectbox(options=['Wykres Słupkowy', 'Wykres liniowy'],
                           label='Oś dla liczby wplat',
                           key='lw_char_db',
                           on_change=create_df(dictionary_options, "lw_char_db",
                                               st.session_state.lw_char_db)
                           )

def circulation(dictionary_options):
    nc = st.checkbox('Nakład całkowity', value=True, on_change=create_df(dictionary_options, 'nc_db',
                                                                         st.session_state.nc_db),
                     key='nc_db')
    nc_axis = st.selectbox(options=['Oś pomocnicza', 'Oś główna'],
                           label='Rodzaj wykresu dla nakładu',
                           key='nc_axis_db',
                           on_change=create_df(dictionary_options, "nc_axis_db",
                                               st.session_state.nc_axis_db)
                           )
    nc_char = st.selectbox(options=['Wykres liniowy', 'Wykres Słupkowy'], label='Oś dla nakładu',
                           key='nc_char_db',
                           on_change=create_df(dictionary_options, "nc_char_db",
                                               st.session_state.nc_char_db))

def cost(dictionary_options):
    kc = st.checkbox('Koszt całkowity', value=True, on_change=create_df(dictionary_options, 'kc_db',
                                                                        st.session_state.kc_db),
                     key='kc_db')
    kc_axis = st.selectbox(options=['Oś główna', 'Oś pomocnicza'],
                           label='Rodzaj wykresu dla kosztu',
                           key='kc_axis_db',
                           on_change=create_df(dictionary_options, "kc_axis_db",
                                               st.session_state.kc_axis_db)
                           )
    kc_char = st.selectbox(options=['Wykres liniowy', 'Wykres Słupkowy'], label='Oś dla kosztu',
                           key='kc_char_db',
                           on_change=create_df(dictionary_options, "kc_char_db",
                                               st.session_state.kc_char_db)
                           )

def roi(dictionary_options):
    rc = st.checkbox('ROI', on_change=create_df(dictionary_options, 'roi_db', st.session_state.roi_db),
                     key='roi_db')
    roi_axis = st.selectbox(options=['Oś pomocnicza', 'Oś główna'], label='Rodzaj wykresu dla ROI',
                            key='roi_axis_db',
                            on_change=create_df(dictionary_options, "roi_axis_db",
                                                st.session_state.roi_axis_db))
    roi_char = st.selectbox(options=['Wykres liniowy', 'Wykres Słupkowy'], label='Oś dla ROI',
                            key='roi_char_db',
                            on_change=create_df(dictionary_options, "roi_char_db",
                                                st.session_state.roi_char_db))

def szlw(dictionary_options):
    rs = st.checkbox('Stopa Zwrotu L. Wpłat', on_change=create_df(dictionary_options, 'szlw_db',
                                                              st.session_state.szlw_db),
                 key='szlw_db')
    szlw_axis = st.selectbox(options=['Oś pomocnicza', 'Oś główna'],
                             label='Rodzaj wykresu dla SZLW',
                             key='szlw_axis_db',
                             on_change=create_df(dictionary_options, "szlw_axis_db",
                                                 st.session_state.szlw_axis_db)
                             )


    szlw_char = st.selectbox(options=['Wykres liniowy', 'Wykres Słupkowy'], label='Oś dla SZLW',
                         key='szlw_char_db',
                         on_change=create_df(dictionary_options, "szlw_char_db",
                                             st.session_state.szlw_char_db)
                         )
def szp(dictionary_options):
    st.checkbox('Stopa Zwrotu Poz.', on_change=create_df(dictionary_options, 'szp_db',
                                                              st.session_state.szp_db),
                 key='szp_db')
    st.selectbox(options=['Oś pomocnicza', 'Oś główna'],
                             label='Rodzaj wykresu dla SZP',
                             key='szp_axis_db',
                             on_change=create_df(dictionary_options, "szp_axis_db",
                                                 st.session_state.szp_axis_db)
                             )


    st.selectbox(options=['Wykres liniowy', 'Wykres Słupkowy'], label='Oś dla SZP',
                         key='szp_char_db',
                         on_change=create_df(dictionary_options, "szp_char_db",
                                             st.session_state.szp_char_db)
                         )

def column_total_sum_amount(dictionary_options):
    sct = st.checkbox('Łączna Suma wpłat', value=True, on_change=create_df(dictionary_options, "swt_db",
                                                                   st.session_state.swt_db),
                     key="swt_db")
    sct_axis = st.selectbox(options=['Oś główna', 'Oś pomocnicza'],
                           label='Rodzaj wykresu dla łącznej sumy wpłat',
                           on_change=create_df(dictionary_options, "swt_axis_db",
                                               st.session_state.swt_axis_db),
                           key="swt_axis_db")
    sct_char = st.selectbox(options=['Wykres Słupkowy', 'Wykres liniowy'],
                           label='Oś dla łącznej sumy wplat',
                           on_change=create_df(dictionary_options, "swt_char_db",
                                               st.session_state.swt_char_db)
                           , key="swt_char_db")

def cost_total(dictionary_options):
    kc = st.checkbox('Koszt całkowity', value=True, on_change=create_df(dictionary_options, 'kct_db',
                                                                        st.session_state.kct_db),
                     key='kct_db')
    kc_axis = st.selectbox(options=['Oś główna', 'Oś pomocnicza'],
                           label='Rodzaj wykresu dla kosztu',
                           key='kct_axis_db',
                           on_change=create_df(dictionary_options, "kct_axis_db",
                                               st.session_state.kct_axis_db)
                           )
    kc_char = st.selectbox(options=['Wykres liniowy', 'Wykres Słupkowy'], label='Oś dla kosztu',
                           key='kct_char_db',
                           on_change=create_df(dictionary_options, "kct_char_db",
                                               st.session_state.kct_char_db)
                           )
def acquisition(dictionary_options):
    poz = st.checkbox('Pozyskanie', value=True, on_change=create_df(dictionary_options, 'poz_db',
                                                                        st.session_state.poz_db),
                     key='poz_db')
    poz_axis = st.selectbox(options=['Oś główna', 'Oś pomocnicza'],
                           label='Rodzaj wykresu dla pozyskania',
                           key='poz_axis_db',
                           on_change=create_df(dictionary_options, "poz_axis_db",
                                               st.session_state.poz_axis_db)
                           )
    poz_char = st.selectbox(options=['Wykres liniowy', 'Wykres Słupkowy'], label='Oś dla kosztu',
                           key='poz_char_db',
                           on_change=create_df(dictionary_options, "poz_char_db",
                                               st.session_state.poz_char_db)
                           )