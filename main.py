import pandas as pd

import streamlit as st
from database.source_db import deaful_set
from database.dowload_data import download_first_data, download_second_data, download_dash_address_data
from functions.pivot_table import pivot_table_w_subtotals
from functions.plot_cam_adr_dash import pivot_for_dash
from datetime import datetime as date

#podstawowe ustawienia strony z raportami
st.set_page_config(page_title="Moduł raportowania dla firmy FSAPS",
                   page_icon=':bar_chart:',
                   layout='wide')

# pobieram dane z bazy dabych w zaleznosci od lokalizacji
mailings, con = deaful_set('local')

#pobieram dane podstawowe
#data = download_second_data(con)
#data.to_csv('./database/dane.csv')
#data = pd.read_csv('./database/dane.csv')
#dodaje sidebary z mozlowoscia wyboru mailingow i lat
def style_button_row(clicked_button_ix, n_buttons):
    def get_button_indices(button_ix):
        return {
            'nth_child': button_ix,
            'nth_last_child': n_buttons - button_ix + 1
        }

with st.sidebar:
    year_range_slider = st.slider('Proszę wybrać lata', min_value=2008, max_value=date.now().year,
                                  value=[date.now().year - 4, date.now().year])
    st.write('Działy:')
    st.button('Malingi Adresowe')
    st.button('Malingi Bezadresowe')
    st.button('Korelacje')

year_from = year_range_slider[0]
year_to = year_range_slider[1]

data = download_dash_address_data(con)
data_to_show = data.loc[(data['grupa_akcji_3'] >=year_from) & (data['grupa_akcji_3'] <=year_to)]

a1, a2 = st.columns(2)
a1.dataframe(data_to_show)
#data_to_show.set_index(['grupa_akcji_3','grupa_akcji_2'], inplace=True)
cam_adr_plot = pivot_for_dash(data_to_show[['grupa_akcji_3','grupa_akcji_2', 'suma_wplat']])
a2.bokeh_chart(cam_adr_plot)
#st.bokeh_chart(cam_adr_plot, use_container_width=True)
