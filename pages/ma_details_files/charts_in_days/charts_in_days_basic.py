import streamlit as st

from pages.ma_details_files.charts_in_days.download_data_for_days_charts import download_data_for_days_charts


class ChartsInDays:
    def __init__(self, mailing, con, years, refresh_data, engine):
        self.mailing = mailing
        self.con = con
        self.years = years
        self.refresh_data = refresh_data
        self.engine = engine
        self.data_cost_and_circulation = None
        self.data_sum_count = None

    def create_tabs(self) -> None:
        """Metoda tworzy zakladki potrzebne, w których wybieramy jakie dane mają znaleść się na wykresie. 
        Dodatkowo metoda umiesza wygenerowane wykresy i tabele przestawne """
        with st.container():
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
                ['Suma Wpłat', 'Liczba Wpłat', 'Stopa zwrotu liczby wplat', 'ROI',
                 'Profit', 'Ustawienia'])
            # with tab5:
            #     st.bokeh_chart(char_profit, use_container_width=True)
            #     with st.expander('Zobacz tabele z danymi'):
            #         st.dataframe(pivot_profit)
            # with tab4:
            #     st.bokeh_chart(char_roi, use_container_width=True)
            #     with st.expander('Zobacz tabele z danymi'):
            #         st.dataframe(pivot_roi)
            # with tab3:
            #     st.bokeh_chart(char_szlw, use_container_width=True)
            #     with st.expander('Zobacz tabele z danymi'):
            #         st.dataframe(pivot_szlw)
            # with tab2:
            #     st.bokeh_chart(char_count_of_amount, use_container_width=True)
            #     with st.expander('Zobacz tabele z danymi'):
            #         st.dataframe(pivot_count_amount)
            # with tab1:
            #     st.bokeh_chart(char_sum_of_amount, use_container_width=True)
            #     with st.expander('Zobacz tabele z danymi'):
            #         st.dataframe(pivot_sum_of_amount)

    def download_data(self):
        """Metoda pobiera dane niezbedne do analizy"""
        self.data_cost_and_circulation = download_data_for_days_charts(self, False, 'dash_char_ma_data',
                                                                       'count_and_sum_amount_char_for_days')
        st.dataframe(self.data_cost_and_circulation)
        # self.data_sum_count = down_data_sum_and_count(self.con, self.refresh_data, self.engine)
