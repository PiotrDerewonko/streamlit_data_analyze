import numpy as np
import pandas as pd
import streamlit as st

from functions_pandas.plot_cam_adr_dash import pivot_and_chart_for_dash


def change_type_and_label(pivot, index) -> [str, pd.DataFrame]:
    pivot.reset_index(inplace=True)
    index_str = ' '
    tmp = 1
    for i in index:
        if len(index) == 1:
            index_str == index[0]
        else:
            test = index[tmp]
            if tmp == 0:
                index_str += test
            else:
                index_str += test
                index_str += '/'
        tmp -= 1
        pivot[i] = pivot[i].astype(str)
    pivot.set_index(index, inplace=True)
    return index_str, pivot


def genarate_char(pivot, index, data, title_of_char) -> None:
    char_options = pd.DataFrame(columns=['Nazwa parametru', 'oś', 'Opcje'])

    for i in range(0, len(pivot.columns)):
        tmp = pd.DataFrame(
            data={'Nazwa parametru': pivot.columns[i], 'oś': 'Oś główna', 'Opcje': 'Wykres Słupkowy Skumulowany'},
            index=[i])
        char_options = pd.concat([char_options, tmp])
    pivot.replace([np.inf, -np.inf], 0, inplace=True)
    index_str, pivot = change_type_and_label(pivot, index)
    dict_of_oriantation = {'major': 'vertical', 'group': 'horizontal', 'sub_group': 'vertical'}
    char_value, aa = pivot_and_chart_for_dash(data, index, 'me_detail', 'test tytulu',
                                       index_str, {}, pivot, char_options,
                                       title_of_char,
                                       dict_of_oriantation
                                       )
    st.bokeh_chart(char_value, use_container_width=True)
    with st.expander('Kiknij i zobacz dane'):
        st.dataframe(pivot, use_container_width=True)
