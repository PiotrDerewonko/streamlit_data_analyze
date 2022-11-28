import itertools

from bokeh.palettes import Dark2_5 as palette
from bokeh.transform import dodge


def char_ma_db_dash(temp_df, p, str_mutlindex, source, pivot_table_ma,*args):
    temp_df = temp_df.replace({'Oś główna': 'default', 'Oś pomocnicza': 'secon_axis'})
    len_y_prime_positions = len(temp_df.loc[temp_df['oś'] == 'default'])
    len_y_second_positions = len(temp_df.loc[temp_df['oś'] == 'secon_axis'])
    colors_fin = []
    colors = itertools.cycle(palette)
    #  todo dorobic mechanim automatycznego doboru grubosci kolumn i przesuniecia w zaleznosci od ilosc argumentow
    list_tmp = [0, -0.15, 0.15, -0.3, 0.30, -0.45, 0.450]
    for m, color in zip(range(len(temp_df)), colors):
        colors_fin.append(color)
    j = 0
    count_of_y_prime = 0
    count_of_y_second = 0
    for i, row in temp_df.iterrows():
        if row['oś'] == 'default':
            position = list_tmp[count_of_y_prime]
            count_of_y_prime += 1
        else:
            position = list_tmp[count_of_y_second]
            count_of_y_second += 1
        if row['Opcje'] == 'Wykres Słupkowy':
            p.vbar(x=dodge(str_mutlindex, position,
                           range=p.x_range), top=row['Nazwa parametru'], source=source,
                   width=0.15, legend_label=row['Nazwa parametru'], y_range_name=row['oś'], color=colors_fin[j])

        elif row['Opcje'] == 'Wykres liniowy':
            p.line(pivot_table_ma.index.values, pivot_table_ma[f'''{row['Nazwa parametru']}'''], line_width=1,
                   y_range_name=row['oś'],
                   legend=row['Nazwa parametru'], color=colors_fin[j])
            if row['Nazwa parametru']=='naklad':
                type = args[0]
                if type == 'me_detail':
                    index_for_char = args[1]
                    #labels = LabelSet(x = pivot_table_ma.index, y=100, text='naklad', source=source, render_mode='canvas')
                    #p.add_layout(labels)
                    #test = Label(x=index_for_char, y='naklad', text='naklad', source=source)
                    #p.add_layout(test)
            p.circle(pivot_table_ma.index.values, pivot_table_ma[f'''{row['Nazwa parametru']}'''],
                   y_range_name=row['oś'],
                   legend=row['Nazwa parametru'], color=colors_fin[j])
        j += 1

def char_options(p):
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    p.axis.minor_tick_line_color = None
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 'vertical'
    p.xaxis.subgroup_label_orientation = 'vertical'