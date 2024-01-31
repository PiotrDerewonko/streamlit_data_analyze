import pandas as pd
import streamlit as st

def column_options(con):
    #sql = 'select * from raporty.people_data limit 1'
    #tmp = pd.read_sql_query(sql, con)
    tmp = pd.read_csv('./pages/ma_details_files/tmp_file/people.csv', index_col='Unnamed: 0', nrows=1)
    list_options = tmp.columns.to_list()
    list_options = sorted(list_options)

    #tu dopisuje dodatkowe elementy ktore maja znalesc sie na listach
    list_options.append('grupa_akcji_2_wysylki')
    list_options.append('grupa_akcji_3_wysylki')
    list_options.append('kod_akcji_wysylki')
    list_options.append('powod_otrzymania_giftu')
    list_options.append('akcja_glowna_mailingu')
    list_options.append('akcja_mailingu')
    list_options.append('Obiecany gift')
    list_options.append('Rodzaj giftu')
    #todo tu ma sie pobierac z automatu a nie z palca
    list_options.append('GIFT')
    list_options.append('KSIĄŻECZKA Z DNIA SKUPIENIA')
    list_options.append('KARTY')
    list_options.append('KOLOR KARTY')
    list_options.append('WPŁATA')
    list_options.append('TYP DARCZYŃCY')
    list_options.append('karta_na_mailing')
    list_options.append('laczna_ilosc_zamowien')
    list_options.append('przedzial_wieku')
    list_options.append('vip')
    final_option_list = ['']
    if 'text_key' not in st.session_state:
        st.session_state.text_key = ''
    if 'text_key_1' not in st.session_state:
        st.session_state.text_key_1 = ''
    if 'test_list' not in st.session_state:
        st.session_state.test_list = ''
    final_option_list.append(st.session_state.test_list)
    #todo przerobic ten kod na docelowy
    def test():
        a = st.session_state.text_key
        for ii in range(0, len(a)):
            final_option_list.append(a[ii])

    def test_1():
        a = st.session_state.text_key_1
        for ii in range(0, len(a)):
            final_option_list.append(a[ii])

    columns_options = st.multiselect(options=list_options, default=['grupa_akcji_2_wysylki', 'grupa_akcji_3_wysylki'],
                                     label='Prosze wybrac gift')
    corr_method = st.selectbox(options=['spearman', 'pearson'], label='Metoda korelacji')

    return columns_options, corr_method

