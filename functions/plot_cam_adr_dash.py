import pandas as pd
from bokeh.plotting import figure, ColumnDataSource
from bokeh.transform import dodge
from bokeh.models import LinearAxis, Range1d
from functions.short_mailings_names import change_name

def pivot_for_dash(data):
    'zmieniam typ kolumny z rokiem na tekst'
    data['grupa_akcji_3'] = data['grupa_akcji_3'].astype(str)

    gr3 = data['grupa_akcji_3'].drop_duplicates().to_list()
    gr3.sort()

    'pobieram zakres lat'
    from_ = gr3[0]
    to_ = gr3[-1]

    data = change_name(data)

    'dodaje zmienna multindex aby moc latwo zmieniac multindex w zarownw w atbeli przestwnej jak i ' \
    'grupowaniu do wykresu'
    multindex = ['grupa_akcji_3','grupa_akcji_2']
    pivot_table_ma = pd.pivot_table(data, index=multindex, values=['suma_wplat', 'koszt_calkowity', 'liczba_wplat',
                                                                   'naklad_calkowity'],
                                aggfunc='sum')
    index_for_char = data.groupby(multindex)
    source = ColumnDataSource(pivot_table_ma)

    p = figure(x_range=index_for_char,
               height=350,width=1300, title=f"Wyniki mailingow za lata {from_} - {to_}",
               toolbar_location='right',
               x_axis_label='Mailingi',
               y_axis_label='Suma wpłat/koszt')

    "dodaje druga os najpierw nazwe i zasieg potem layout i wykorzystuje nazwe i wkazuje strone"
    p.extra_y_ranges = {'secon_axis': Range1d(-100,pivot_table_ma['naklad_calkowity'].max())}
    p.add_layout(LinearAxis(y_range_name="secon_axis", axis_label = 'naklad/liczba wpłat'), 'right')

    'dodaje bwa wykresy słupkowe'
    p.vbar(x=dodge('grupa_akcji_3_grupa_akcji_2',0.0, range=p.x_range), top='suma_wplat', source=source, width=0.2, legend_label="Suma Wplat",)
    #p.line(x='grupa_akcji_3_grupa_akcji_2', y='koszt_calkowity_mean', legend_label="Temp.", line_width=2,source=source)
    p.vbar(x=dodge('grupa_akcji_3_grupa_akcji_2',-0.25, range=p.x_range), top='koszt_calkowity', source=source, color='red', width=0.2,
           legend_label="Koszt")
    p.line(pivot_table_ma.index.values, pivot_table_ma['liczba_wplat'], line_width=1, y_range_name='secon_axis',
           legend='Liczba wpłat', color="green")
    p.line(pivot_table_ma.index.values, pivot_table_ma['naklad_calkowity'], line_width=1, y_range_name='secon_axis',
           legend='Nakład całkowity',color="orange")
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.axis.minor_tick_line_color = None
    p.y_range.start = 0
    p.x_range.range_padding = 0.1


    return p





