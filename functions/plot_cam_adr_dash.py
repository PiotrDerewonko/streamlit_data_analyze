import pandas as pd
from bokeh.plotting import figure, ColumnDataSource
from bokeh.transform import dodge
from bokeh.models import LinearAxis, Range1d
from functions.short_mailings_names import change_name
import itertools
from bokeh.palettes import Dark2_5 as palette
from streamlit_functions.dashboard.operation_for_char import create_df, modifcate_data, create_pivot_table, \
    change_short_names, check_max_value

def pivot_and_chart_for_dash(data, multindex, type, title, x_label, y_label, y_sec_label, dict):
    temp_df = create_df(dict)
    # todo doknczyc przerabianie funckji tak aby pobirala tabele i na jej podstawie tworzyla wykres
    data, gr3, from_, to_ = modifcate_data(data, type, multindex)
    data = change_name(data)
    temp_df = change_short_names(temp_df)

    index_for_char = data.groupby(multindex)

    pivot_table_ma = create_pivot_table(data, multindex, type)

    max_value_for_y_prime = check_max_value(pivot_table_ma, temp_df, 'Oś główna')
    max_value_for_y_second = check_max_value(pivot_table_ma, temp_df, 'Oś pomocnicza')

    source = ColumnDataSource(pivot_table_ma)
    #todo dokonczyc tooltips tak aby po njaechaniu pokazywal wartosci
    TOOLTIPS = [
        ("index", "$index"),
        ('(x,y)', "($x, $y)")]

    #tworze figure do ktorej bede dolaczac wykresy
    p = figure(x_range=index_for_char,
               height=450, width=1500, title=f"{title}{from_} - {to_}",
               toolbar_location='right',
               x_axis_label=x_label,
               y_axis_label=y_label, tooltips=TOOLTIPS
               )
    p.title.text_font_size = '18pt'

    p.y_range = Range1d(-100, max_value_for_y_prime*1.1)

    if type != 'increase':
        "dodaje druga os najpierw nazwe i zasieg potem layout i wykorzystuje nazwe i wkazuje strone"
        p.extra_y_ranges = {'secon_axis': Range1d(-100, max_value_for_y_second*1.1)}
        p.add_layout(LinearAxis(y_range_name="secon_axis", axis_label=y_sec_label), 'right')
        p.yaxis.axis_label_text_font_size = "15pt"

    #wylaczam tryb naukowy, dzieki czemu pokazuja sie pelni liczby a nie ich potegi
    p.yaxis.formatter.use_scientific = False
    'petla w celu uwtorzenia polaczonych nazws kolumn multindexu potrzebnych do wykresu'
    str_mutlindex=''
    j = 0
    for i in multindex:
        if j == 0:
            str_mutlindex = i
            j += 1
        else:
            str_mutlindex = str_mutlindex + "_" + i

    'dodaje dwa wykresy słupkowe i dwa liniowe'
    if type != 'increase':
        p.vbar(x=dodge(str_mutlindex, 0.0, range=p.x_range), top='suma_wplat', source=source, width=0.2,
               legend_label="Suma Wplat",)
        p.vbar(x=dodge(str_mutlindex, -0.25, range=p.x_range), top='koszt_calkowity', source=source,
               color='red', width=0.2,
               legend_label="Koszt")
        p.line(pivot_table_ma.index.values, pivot_table_ma['liczba_wplat'], line_width=1, y_range_name='secon_axis',
               legend='Liczba wpłat', color="green")
        p.line(pivot_table_ma.index.values, pivot_table_ma['naklad_calkowity'], line_width=1, y_range_name='secon_axis',
               legend='Nakład całkowity', color="orange")
    else:
        pt_columns = pivot_table_ma.columns
        pt_columns = pt_columns.to_list()
        colors = itertools.cycle(palette)
        colors_fin = []
        for m, color in zip(range(len(pivot_table_ma.columns)), colors):
            colors_fin.append(color)
        p.vbar_stack(pivot_table_ma.columns, x=dodge(str_mutlindex, 0, range=p.x_range),  source=source,
                     width=0.2, legend_label=pt_columns, color=colors_fin)
        #p.vbar(x=dodge(str_mutlindex, -0.25, range=p.x_range), top='ilosc', source=source,
        #       color='red', width=0.2,
        #       legend_label="ilosc")
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    p.axis.minor_tick_line_color = None
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 'vertical'
    p.xaxis.subgroup_label_orientation = 'vertical'

    if type != 'increase':
        #dodanie dodatkowych pol do tabeli przestawnej

        pivot_table_ma = pivot_table_ma.style.format( na_rep='MISSING',
                    formatter={
                               ('suma_wplat'): lambda x: "{: .0f} zł".format(x),
                               ('naklad_calkowity'): lambda x: "{: .0f}".format(x),
                               ('ROI'): lambda x: "{:,.2f} zł".format(x),
                               ('Stopa zwrotu l.w.'): lambda x: "{: .2f} %".format(x),
                               ('Koszt na głowę'): lambda x: "{: .2f} zł".format(x),
                               ('koszt_calkowity'): lambda x: "{: .0f} zł".format(x)
                               })
    return p, pivot_table_ma





