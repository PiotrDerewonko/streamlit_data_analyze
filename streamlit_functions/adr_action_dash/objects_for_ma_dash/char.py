import itertools

from bokeh.palettes import Dark2_5 as palette
from bokeh.transform import dodge


def char_ma_db_dash(temp_df, p, str_mutlindex, source, pivot_table_ma,*args):
    temp_df = temp_df.replace({'Oś główna': 'default', 'Oś pomocnicza': 'secon_axis'})

    #sprawdzam ile jest wykresow słupkowych i ślukowych skumulowanych
    len_vbar = len((temp_df.loc[temp_df['Opcje'] == 'Wykres Słupkowy']))
    len_stock = len((temp_df.loc[temp_df['Opcje'] == 'Wykres Słupkowy Skumulowany']))
    len_vbar = len_vbar + len_stock
    colors_fin = []
    colors = itertools.cycle(palette)
    list_tmp = [0]
    tmp = 0
    value = round(0.9/len_vbar, 2)
    count = 1
    while tmp <= 1:
        list_tmp.append(count*value)
        list_tmp.append(count*value*-1)
        tmp += value
        count +=1

    for m, color in zip(range(len(temp_df)), colors):
        colors_fin.append(color)
    j = 0
    count_of_y_prime = 0
    count_of_y_second = 0
    temp_df.sort_values(['Opcje'], inplace=True)

    #wydzielam tylko te wiersze ktore maja wykres slupkowy skumolowany
    if len_stock >= 1:
        stock = temp_df.loc[temp_df['Opcje'] == 'Wykres Słupkowy Skumulowany']
        temp_df = temp_df.drop(stock.index)
        stock_default = stock.loc[stock['oś'] == 'default']
        stock_second_axis = stock.loc[stock['oś'] == 'secon_axis']
        if len(stock_default) >= 1:
#todo poprawic maksymalna wartosc osi
#todo dla wykresu slupkowego zrtobic osobne palety kolorow i palety zalezne od ilosci elementow

            position = list_tmp[count_of_y_prime]
            count_of_y_prime += 1
            test = pivot_table_ma[stock_default['Nazwa parametru'].to_list()].columns
            p.vbar_stack(test, x=dodge(str_mutlindex, position,
                           range=p.x_range),source=source, width=value,
                         legend_label=stock_default['Nazwa parametru'].to_list(), y_range_name='default', color=colors_fin[:len(stock_default)] )
            j += 1



    for i, row in temp_df.iterrows():

        if row['Opcje'] == 'Wykres Słupkowy':
            position = list_tmp[count_of_y_prime]
            count_of_y_prime += 1
            p.vbar(x=dodge(str_mutlindex, position,
                           range=p.x_range), top=row['Nazwa parametru'], source=source,
                   width=value, legend_label=row['Nazwa parametru'], y_range_name=row['oś'], color=colors_fin[j])


        elif row['Opcje'] == 'Wykres liniowy':
            p.line(pivot_table_ma.index.values, pivot_table_ma[f'''{row['Nazwa parametru']}'''], line_width=1,
                   y_range_name=row['oś'],
                   legend=row['Nazwa parametru'], color=colors_fin[j])
            p.circle(pivot_table_ma.index.values, pivot_table_ma[f'''{row['Nazwa parametru']}'''],
                   y_range_name=row['oś'],
                   legend=row['Nazwa parametru'], color=colors_fin[j])

        j += 1

def char_options(p):
    p.xgrid.grid_line_color = None
    #p.legend.location = "top_left"
    #p.legend.click_policy = "hide"

    p.axis.minor_tick_line_color = None
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 'vertical'
    p.xaxis.subgroup_label_orientation = 'vertical'