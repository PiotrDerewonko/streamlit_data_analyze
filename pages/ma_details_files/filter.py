import streamlit as st

from pages.ma_details_files.data_about_people_and_campaign_pay import distinct_options


def filtr_options(con):
    refresh_data = False
    filter_value = distinct_options(refresh_data)
    list = filter_value.columns.to_list()
    list[0] = ' '
    c1, c2, c3, c4 = st.columns(4)
    list_values_1 = [' ']
    list_values_2 = [' ']
    list_values_3 = [' ']
    list_values_4 = [' ']
    list_of_final_filtr = [[], [], [], []]
    #inicjalizacja obiektow pierwszych
    list_of_objects = ['f1', 'f2', 'f3', 'f4']
    for x in list_of_objects:
        if x not in st.session_state:
            st.session_state[x] = ' '
    #inicjalizacja obiektow drugich
    list_of_objects_2 = ['f1_value', 'f2_value', 'f3_value', 'f4_value']
    for x in list_of_objects_2:
        if x not in st.session_state:
            st.session_state[x] = ' '
    # funkcje do zawezania listy opcji po wybraniu odpowiednije kolumny
    # todo dodac filtry z bazy danych
    def change_options_1(value):

        tmp = filter_value[value]
        tmp.dropna(inplace=True)

        for z, row in tmp.items():
            list_values_1.append(row)
    def change_options_2(value):
        tmp = filter_value[value]
        tmp.dropna(inplace=True)
        for z, row in tmp.items():
            list_values_2.append(row)
    def change_options_3(value):
        tmp = filter_value[value]
        tmp.dropna(inplace=True)
        for z, row in tmp.items():
            list_values_3.append(row)
    def change_options_4(value):
        tmp = filter_value[value]
        tmp.dropna(inplace=True)
        for z, row in tmp.items():
            list_values_4.append(row)
    # funkcje do tworzenie fina lnego slownika z filtrami
    def filtr_falue_1(value1, value2):
        list_of_final_filtr[0] = [value1, value2]
    def filtr_falue_2(value1, value2):
        list_of_final_filtr[1] = [value1, value2]
    def filtr_falue_3(value1, value2):
        list_of_final_filtr[2] = [value1, value2]
    def filtr_falue_4(value1, value2):
        list_of_final_filtr[3] = [value1, value2]
    with c1:
        st.selectbox(label="Pierwszy filtr", options=list, on_change=change_options_1(st.session_state.f1), key='f1')
        st.multiselect(label='Wartosc filtru 1', options=list_values_1,
                       on_change=filtr_falue_1(st.session_state.f1, st.session_state.f1_value), key='f1_value')
    with c2:
        st.selectbox(label="Drugi filtr", options=list, on_change=change_options_2(st.session_state.f2), key='f2')
        st.multiselect(label='Wartosc filtru 2', options=list_values_2,
                       on_change=filtr_falue_2(st.session_state.f2, st.session_state.f2_value), key='f2_value')
    with c3:
        st.selectbox(label="Trzeci filtr", options=list, on_change=change_options_3(st.session_state.f3), key='f3')
        st.multiselect(label='Wartosc filtru 3', options=list_values_3,
                       on_change=filtr_falue_3(st.session_state.f3, st.session_state.f3_value), key='f3_value')
    with c4:
        st.selectbox(label="Czwarty filtr", options=[' ', 'Taki sam zakres dni'], on_change=filtr_falue_4(st.session_state.f4,
                                                                                                     st.session_state.f4_value), key='f4_value')

    st.markdown(list_of_final_filtr)
    return list_of_final_filtr