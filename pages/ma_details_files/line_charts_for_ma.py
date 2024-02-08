import itertools

from bokeh.palettes import Category20_20 as palette
from bokeh.plotting import figure


def line_chart_for_m(pivot, title, y_axis_label, pivot_circ, *args) -> figure:
    if pivot_circ is not None:
        pivot_circ_trans = pivot_circ.transpose()
        x_label = 'Dzien po nadaniu mailingu'
        is_division_new_old = args[0]
        list_new_old = args[1]
    else:
        x_label = args[0]
        is_division_new_old = False
        list_new_old = ['pusto']

    p = figure(height=700, width=1300,
               toolbar_location='right',
               title=title, y_axis_label=y_axis_label, x_axis_label=x_label
               )
    colors_fin = []
    colors = itertools.cycle(palette)
    for m, color in zip(range(len(pivot.columns)), colors):
        colors_fin.append(color)
    # j to zmienna do podania ktory numer koloru dla zwyklego przypadku, a k gdy jest podzial nowy stary
    j = 0
    k = 0
    len_columns = len(pivot.columns)

    for i in pivot.columns:
        if pivot_circ is not None:
            tmp = f' naklad {int(pivot_circ_trans.iloc[j].values[0])}'
            if j == len_columns - 1:
                line_width = 7
                line_dash_value = []
            else:
                line_width = 4
                line_dash_value = "dashed"
        else:
            tmp = ''
            line_width = 4
            line_dash_value = "dashed"


        if (is_division_new_old == False) | ((is_division_new_old == True) & (len(list_new_old) == 1)):
            p.line(pivot.index.values,  pivot[i], line_width=line_width, legend=f'{i}{tmp}', color=colors_fin[j]
                   , line_dash=line_dash_value)
            p.circle(pivot.index.values, pivot[i], size=15, color=colors_fin[j], alpha=0.5)
        elif (is_division_new_old == True) & (len(list_new_old) == 2):
            final_colour_number = 0
            if j !=0:
                previous = pivot.columns[j-1]
                current = pivot.columns[j]
                previous = previous[:2]
                current = current[:2]
                if previous != current:
                    k += 1
                if (j == len_columns - 2) | (j == len_columns - 1):
                    line_dash_value = []
                    line_width = 7
                    p.circle(pivot.index.values, pivot[i], size=15, color=colors_fin[k], alpha=0.5)
                else:
                    p.triangle(pivot.index.values, pivot[i], size=12, color=colors_fin[k], alpha=1)
            p.line(pivot.index.values, pivot[i], line_width=line_width, legend=f'{i}{tmp}', color=colors_fin[k]
                       , line_dash=line_dash_value)


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
