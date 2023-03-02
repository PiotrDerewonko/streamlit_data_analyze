import itertools

from bokeh.palettes import Category20_20 as palette
from bokeh.plotting import figure


def line_chart_for_m(pivot, title, y_axis_label, pivot_circ, *args):
    if pivot_circ is not None:
        pivot_circ_trans = pivot_circ.transpose()
        x_label = 'Dzien po nadaniu mailingu'
    else:
        x_label = args[0]
    p = figure(height=700, width=1300,
               toolbar_location='right',
               title=title, y_axis_label=y_axis_label, x_axis_label=x_label
               )
    colors_fin = []
    colors = itertools.cycle(palette)
    for m, color in zip(range(len(pivot.columns)), colors):
        colors_fin.append(color)
    j = 0
    len_columns = len(pivot.columns)


    for i in pivot.columns:
        if pivot_circ is not None:
            tmp = f' naklad {int(pivot_circ_trans.iloc[j].values[0])}'
            if j == len_columns-1:
                line_width = 7
            else:
                line_width = 4
        else:
            tmp = ''
            line_width = 4

        p.line(pivot.index.values, pivot[i], line_width=line_width, legend=f'{i}{tmp}', color=colors_fin[j]
               )
        j += 1
    p.legend.location = 'top_left'
    p.yaxis.formatter.use_scientific = False
    p.background_fill_color = None
    p.border_fill_color = None
    p.title.text_font_size = '14pt'
    p.legend.label_text_font_size = '14pt'



    return p

def change_list_to_string(list, para):
    if len(list) >= 1:
        tmp = f'{para}'
        for i in range(0, len(list)):
            if i == 0:
                tmp = tmp + ' ' + list[i]
            else:
                tmp = tmp + ', ' + list[i]
    else:
        tmp = ''
    return tmp
