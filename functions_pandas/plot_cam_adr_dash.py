import itertools

import streamlit as st
from bokeh.models import LinearAxis, Range1d, Legend
from bokeh.palettes import Category20_20 as palette
from bokeh.plotting import figure, ColumnDataSource
from bokeh.transform import dodge

import streamlit_functions.adr_action_dash.objects_for_ma_dash.char as char_opt
from functions_pandas.short_mailings_names import change_name
from pages.ma_details_files.line_charts_for_ma import line_chart_for_m
from streamlit_functions.dashboard.operation_for_char import create_df, modifcate_data, create_pivot_table, \
    change_short_names_ma, change_short_names_db, check_max_value, label_of_axis


def pivot_and_chart_for_dash(data, multindex, type, title, x_label, dict, *args):
    if (type != 'increase') & (type != 'dist') & (type != 'dist2'):
        temp_df = create_df(dict)
    if (type != 'people_db'):
        data,  title_fin = modifcate_data(data, type, multindex, title)

    major = "vertical"
    group = "horizontal"
    sub_group = "horizontal"

    if type == 'nonaddress':
        if args[0] !='':
            title_fin = args[0]
        dict_of_oriantation = args[1]
        major = dict_of_oriantation['major_db']
        group = dict_of_oriantation['group_db']
        sub_group = dict_of_oriantation['sub_group_db']



    if (type != 'me_detail') and (type != 'people_db'):
        data = change_name(data)
    if type == 'address':
        temp_df = change_short_names_ma(temp_df)
    elif type =='nonaddress':
        temp_df = change_short_names_db(temp_df)

    y_label = 'Ilość pozyskanych'


    if (type != 'me_detail') and (type != 'people_db') and (type != 'cost_structure'):
        pivot_table_ma = create_pivot_table(data, multindex, type)
        if (type != 'increase') & (type != 'dist') & (type != 'dist2'):
            temp_df_fin_sec = True
        else:
            temp_df_fin_sec = False
    elif type == 'people_db':
        pivot_table_ma = args[0]
        pivot_table_ma.fillna(0, inplace=True)
        temp_df = args[1]
        title_fin = args[2]
        temp_df_fin_sec = False

    else:
        pivot_table_ma = args[0]
        pivot_table_ma.fillna(0, inplace=True)
        temp_df = args[1]
        title_fin = args[2]
        if len(temp_df.loc[temp_df['oś'] == 'Oś pomocnicza'])>0:
            temp_df_fin_sec = True
        else:
            temp_df_fin_sec = False
        dict_of_oriantation = args[3]
        major = dict_of_oriantation['major']
        group = dict_of_oriantation['group']
        sub_group = dict_of_oriantation['sub_group']

    pivot_table_ma.fillna(0, inplace=True)
    index_for_char = data.groupby(multindex, dropna=True)



    if ((type != 'increase') & (type != 'dist') & (type != 'dist2') & (type != 'people_db')) | (temp_df_fin_sec ==True):
        y_label, y_sec_label = label_of_axis(temp_df)

    if (type != 'increase') & (type != 'dist') & (type != 'dist2') & (type != 'people_db'):
        max_value_for_y_prime = check_max_value(pivot_table_ma
                                                , temp_df, 'Oś główna')
        try:
            max_value_for_y_second = check_max_value(pivot_table_ma, temp_df, 'Oś pomocnicza')
        except:
            max_value_for_y_second = 0
    elif (type == 'people_db'):
        max_value_for_y_prime = pivot_table_ma.max().max()
    pivot_table_ma.fillna(0, inplace=True)
    source = ColumnDataSource(pivot_table_ma)
    #todo dokonczyc tooltips tak aby po njaechaniu pokazywal wartosci

    'petla w celu uwtorzenia polaczonych nazws kolumn multindexu potrzebnych do wykresu'
    str_mutlindex=''
    j = 0
    for i in multindex:
        if j == 0:
            str_mutlindex = i
            j += 1
        else:
            str_mutlindex = str_mutlindex + "_" + i
    #tworze figure do ktorej bede dolaczac wykresy
    p = figure(x_range=index_for_char,
               height=700, width=1300,
               title=f"{title_fin}",
               #title=f"{title}{from_} - {to_}",
               toolbar_location='right',
               x_axis_label=x_label,
               y_axis_label=y_label)
    p.title.text_font_size = '12pt'
    p.add_layout(Legend(background_fill_alpha=0.3))

    p.xaxis.major_label_orientation = major
    p.xaxis.group_label_orientation = group
    p.xaxis.subgroup_label_orientation = sub_group

    #p.xaxis.major_label_orientation = "vertical"
    #p.yaxis.major_label_text_font_size = "18pt"
    #p.xaxis.major_label_text_font_size = "18pt"
    p.xaxis.major_label_text_font_size = "13pt"
    p.xaxis.axis_label_text_font_size = "13pt"
    p.yaxis.major_label_text_font_size = "13pt"
    p.xaxis.subgroup_text_font_size = "13pt"
    p.xaxis.group_text_font_size = "14pt"
    p.xaxis.major_label_orientation = major
    p.xaxis.group_label_orientation = group
    p.xaxis.subgroup_label_orientation = sub_group

    #p.background_fill_color = None
    #p.border_fill_color = None
    p.title.text_font_size = '18pt'



    if (type != 'increase') & (type != 'dist') & (type != 'dist2') & (temp_df_fin_sec ==True):
        p.y_range = Range1d(0, max_value_for_y_prime*1.1)

    if ((type != 'increase') & (type != 'dist') & (type != 'dist2') & (type != 'people_db')) and (max_value_for_y_second != 0):
        "dodaje druga os najpierw nazwe i zasieg potem layout i wykorzystuje nazwe i wkazuje strone"
        p.extra_y_ranges = {'secon_axis': Range1d(0, max_value_for_y_second*1.1)}
        p.add_layout(LinearAxis(y_range_name="secon_axis", axis_label=y_sec_label), 'right')
        p.yaxis.axis_label_text_font_size = "15pt"

    #wylaczam tryb naukowy, dzieki czemu pokazuja sie pelni liczby a nie ich potegi
    p.yaxis.formatter.use_scientific = False

    # tworze wykresy
    if (type != 'increase') & (type != 'dist') & (type != 'dist2') & (type != 'people_db'):
        char_opt.char_for_dash_ma_detail(temp_df, p, str_mutlindex, source, pivot_table_ma, type, index_for_char)
    elif (type == 'people_db'):
        p = line_chart_for_m(pivot_table_ma, title, 'zł', None, 'Miesiąc obecności w bazie')
    else:
        pt_columns = pivot_table_ma.columns
        pt_columns = pt_columns.to_list()
        colors = itertools.cycle(palette)
        colors_fin = []
        for m, color in zip(range(len(pivot_table_ma.columns)), colors):
            colors_fin.append(color)
        st.markdown(pivot_table_ma.columns)
        p.vbar_stack(pt_columns, x=dodge(str_mutlindex, 0, range=p.x_range),  source=source,
                     width=0.7, legend_label=pt_columns, color=colors_fin)

    #char_opt.char_options(p)

    if (type != 'increase') and (type != 'me_detail') and  (type != 'people_db'):
        #dodanie dodatkowych pol do tabeli przestawnej
        pivot_table_ma = pivot_table_ma.style.format(na_rep='MISSING',
                    formatter={
                               ('suma_wplat'): lambda x: "{: .0f} zł".format(x),
                               ('naklad_calkowity'): lambda x: "{: .0f}".format(x),
                               ('ROI'): lambda x: "{:,.2f} zł".format(x),
                               ('Stopa zwrotu l.w.'): lambda x: "{: .2f} %".format(x),
                                ('Stopa pozyskania'): lambda x: "{: .2f} %".format(x),
                               ('Koszt na głowę'): lambda x: "{: .2f} zł".format(x),
                               ('koszt_calkowity'): lambda x: "{: .0f} zł".format(x),
                        ('index_liczba_wplat'): lambda x: "{: .2f} %".format(x),
                        ('index_suma_wplat'): lambda x: "{: .2f} %".format(x),
                               })

    return p, pivot_table_ma





