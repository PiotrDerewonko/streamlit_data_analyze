import pandas as pd
from bokeh.plotting import figure, ColumnDataSource
from bokeh.transform import dodge
from bokeh.models import LinearAxis, Range1d
from functions.short_mailings_names import change_name

def pivot_and_chart_for_dash(data, multindex, type):
    if type != 'increase':
        'zmieniam typ kolumny z rokiem na tekst w przeciwnym wypdaku przestaje dzialac'
        data['grupa_akcji_3'] = data['grupa_akcji_3'].astype(str)
    if type != 'increase':
        gr3 = data['grupa_akcji_3'].drop_duplicates().to_list()
    else:
        data['rok_dodania'] = data['rok_dodania'].astype(str)
        data['miesiac_dodania'] = data['miesiac_dodania'].astype(str)
        data['grupa_akcji_1'] = data['grupa_akcji_1'].astype(str)
        gr3 = data['rok_dodania'].drop_duplicates().to_list()
    gr3.sort()

    'pobieram zakres lat'
    from_ = gr3[0]
    to_ = gr3[-1]

    data = change_name(data)
    if type == 'increase':
        pivot_table_ma = pd.pivot_table(data, index=multindex, values=['ilosc'],
                                aggfunc='sum')
    else:
        pivot_table_ma = pd.pivot_table(data, index=multindex, values=['suma_wplat', 'koszt_calkowity', 'liczba_wplat',
                                                                   'naklad_calkowity'],
                                aggfunc='sum')
    index_for_char = data.groupby(multindex)
    print(index_for_char.head())
    source = ColumnDataSource(pivot_table_ma)

    TOOLTIPS = [
        ("index", "$index"),
        ('(x,y)', "($x, $y)")
    ]
    #todo do przerobienia tyytul i opisy osi w zaleznosci od tyopu
    p = figure(x_range=index_for_char,
               height=450, width=1500, title=f"Wyniki mailingow za lata {from_} - {to_}",
               toolbar_location='right',
               x_axis_label='Mailingi',
               y_axis_label='Suma wpłat/koszt'#, tooltips=TOOLTIPS
               )
    if type == 'increase':
        p.y_range = Range1d(-100, pivot_table_ma['ilosc'].max()*1.1)
    else:
        p.y_range = Range1d(-100, pivot_table_ma['suma_wplat'].max() * 1.1)

    if type != 'increase':
        "dodaje druga os najpierw nazwe i zasieg potem layout i wykorzystuje nazwe i wkazuje strone"
        p.extra_y_ranges = {'secon_axis': Range1d(-100, pivot_table_ma['naklad_calkowity'].max()*1.1)}
        p.add_layout(LinearAxis(y_range_name="secon_axis", axis_label='naklad/liczba wpłat'), 'right')

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
        p.vbar_stack(['grupa_akcji_1', 'ilosc'], x=dodge(str_mutlindex, -0.25, range=p.x_range),  source=source,
                     width=0.2, legend_label='ilosc')
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
        pivot_table_ma['ROI'] = pivot_table_ma['suma_wplat']/pivot_table_ma['koszt_calkowity']
        pivot_table_ma['Stopa zwrotu l.w.'] = (pivot_table_ma['liczba_wplat']/pivot_table_ma['naklad_calkowity'])*100
        pivot_table_ma['Koszt na głowę'] = pivot_table_ma['koszt_calkowity']/pivot_table_ma['naklad_calkowity']
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





