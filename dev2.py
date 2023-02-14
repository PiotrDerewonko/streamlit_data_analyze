import itertools

import pandas as pd
import streamlit as st
from bokeh.models import ColumnDataSource
from bokeh.palettes import Dark2_5 as palette
from bokeh.plotting import figure
from bokeh.transform import dodge

# utwórz DataFrame z multiindexem
#index = pd.MultiIndex.from_tuples([('A', 'foo'), ('A', 'bar'), ('B', 'baz')], names=['one', 'two'])
df = pd.DataFrame({'kod_akcji': ['Q3_22_10_DB_GN_P_ŚWIECA', 'Q4_22_11_DB_TT_KRZL'],'suma_wplat': [34064, 148983], 'koszt_insertu': [24910, 104664], 'pozyskanie': ['da', 'db'],
                  'koszt_utrzymania': [15000, 45000]})
multindex = ['kod_akcji', 'pozyskanie']
df_new = pd.pivot_table(df, values=['koszt_insertu', 'koszt_utrzymania'],index=multindex,  aggfunc='sum' )
df_new2 = pd.pivot_table(df,index=multindex, values=['suma_wplat'],  aggfunc='sum' )
#df_new.columns = ['_'.join(col) for col in df_new.columns.values]
df_new.fillna(0, inplace=True)
# utwórz ColumnDataSource z nowego DataFrame
source = ColumnDataSource(df_new)
source2 = ColumnDataSource(df_new2)

str_mutlindex = ''
j = 0
for i in multindex:
    if j == 0:
        str_mutlindex = i
        j += 1
    else:
        str_mutlindex = str_mutlindex + "_" + i
index_for_char = df.groupby(multindex, dropna=True)

colors = itertools.cycle(palette)
colors_fin = []
for m, color in zip(range(len(df_new.columns)), colors):
    colors_fin.append(color)
pt_columns = df_new.columns
pt_columns = pt_columns.to_list()
# utwórz wykres słupkowy
p = figure(x_range=index_for_char,
           height=700, width=1300,
           toolbar_location='right')
p.vbar_stack(df_new.columns, x=dodge(str_mutlindex, 0, range=p.x_range), source=source,
             width=0.3,  legend_label=pt_columns, color=colors_fin)

p.vbar(x=dodge(str_mutlindex, 0.3,
               range=p.x_range), top='suma_wplat', source=source2,
       width=0.3, legend_label='suma_wplat', color='red')
p_label = p.text(x=dodge(str_mutlindex, 0, range=p.x_range), y='koszt_insertu', source=source, text='koszt_insertu', text_font_size='10pt', x_offset=-20)
p_label2 = p.text(x=dodge(str_mutlindex, 0, range=p.x_range), y='koszt_utrzymania', source=source, text='koszt_utrzymania',text_font_size='10pt', x_offset=-20)
p_label3 = p.text(x=dodge(str_mutlindex, 0.3, range=p.x_range), y='suma_wplat', source=source2, text='suma_wplat', y_offset=100, x_offset=-25, text_font_size='10pt')

st.bokeh_chart(p)
st.dataframe(df_new)
st.dataframe(df_new2)