import streamlit as st

from functions_pandas.plot_cam_adr_dash import pivot_and_chart_for_dash
from pages.deposite_range.download_data import download_data_for_deposite_range, create_pivot_table, \
    download_data_for_avg_number_per_year, add_extra_data_to_df_for_deposite_range
from pages.deposite_range.modificate_data import add_extra_filter
from pages.ma_details_files.create_df_for_char_options import create_df_for_char_options_structure


def create_chart_and_df_for_deposite_range(title_fin_, deposite_range, year_range, year_range_to_analize, con,
                                           refresh_data, index_to_pivot_table, list_to_loc) -> None:
    """Funkcja ktorej zadaniem jest swtorzenie wykresu struktury wplat dla ludzi ktorzy dokonali przynajmniej jednej wplaty
    w wybranym zakresie czasu. """
    with st.container(border=True):
        st.header('Wykres struktury wpłat')
        data = download_data_for_deposite_range(deposite_range, year_range, year_range_to_analize, con, refresh_data)
        data = add_extra_data_to_df_for_deposite_range(data, con, refresh_data)
        data = add_extra_filter(data, list_to_loc)
        pivot, pivot_to_100, char_options, pivot_with_margins = create_pivot_table(data, index_to_pivot_table)
        dict_of_oriantation = {'major': 'vertical', 'group': 'vertical', 'sub_group': 'vertical'}
        if len(title_fin_) < 1:
            title_fin_ = f'''Struktura wpłat z mailingów adresowych za lata {year_range_to_analize[0]} - {year_range_to_analize[1]} 
            (tylko osoby które dokonały przynajmniej jednej wpłaty w przedziale {deposite_range} w latach {year_range[0]} - {year_range[1]}'''
        char_structure, b = pivot_and_chart_for_dash(data, index_to_pivot_table, 'me_detail',
                                                     'Wykres ', 'Lata', {},
                                                     pivot_to_100, char_options, title_fin_,
                                                     dict_of_oriantation)
        st.bokeh_chart(char_structure, use_container_width=True)
        with st.expander(label='Dane tabelaryczne'):
            tab1, tab2 = st.tabs(['Dane wartościowe', 'Dane do 100%'])
            with tab1:
                st.dataframe(pivot_with_margins, use_container_width=True)
            with tab2:
                st.dataframe(pivot_to_100, use_container_width=True)


def create_chart_and_df_for_avg_pay_per_year(year_range_to_analize, con, refresh_data) -> None:
    """Funkcja ktorej zadaaniem jest stworzenie wykresu i tabeli przestwnej pokazujacej ile wynosi srednia liczba wplat
    w skali lat wybranych przez uzytkownika. Funkcja w przeciwienstwie do funkcji create_chart_and_df_for_deposite_range
    , ta funkcja pobiera wszystkie dane niezaleznie od tego skad byla dokonanana wplata """
    with st.container(border=True):
        st.header("Średnia liczba wpłat")
        data = download_data_for_avg_number_per_year(con, year_range_to_analize)
        data_copy = data.copy()
        data.set_index('rok_wplaty', inplace=True)
        dict_of_oriantation = {'major': 'vertical', 'group': 'vertical', 'sub_group': 'vertical'}
        title_fin = f'Średnia liczba wpłat od darczyńcow indywidualnych w latach {year_range_to_analize[0]} - {year_range_to_analize[1]}'
        char_options = create_df_for_char_options_structure(data)
        char_options['oś'].iloc[-1] = 'Oś pomocnicza'
        char_options['Opcje'].iloc[-1] = 'Wykres liniowy'
        char_options['Opcje'].iloc[0] = 'Wykres Słupkowy'
        char_structure, b = pivot_and_chart_for_dash(data_copy, ['rok_wplaty'], 'me_detail',
                                                     'Wykres ', 'Lata', {},
                                                     data, char_options, title_fin,
                                                     dict_of_oriantation)
        st.bokeh_chart(char_structure, use_container_width=True)
        with st.expander('Dane tabelaryczne'):
            st.dataframe(data, use_container_width=True)

