
import bokeh
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import Plot, VBar, LinearAxis
import matplotlib.pyplot as plt
from bokeh.transform import dodge
from bokeh.models import LinearAxis, Range1d

def pivot_for_dash(data):
    'zmieniam typ kolumny z rokiem na tekst'
    data['grupa_akcji_3'] = data['grupa_akcji_3'].astype(str)

    gr3 = data['grupa_akcji_3'].drop_duplicates().to_list()
    gr3.sort()

    'pobieram zakres lat'
    from_ = gr3[0]
    to_ = gr3[-1]
    group = data.groupby(['grupa_akcji_3','grupa_akcji_2'])
    source = ColumnDataSource(data=group)
    print(group.describe())
    p = figure(x_range=group,
               height=350,width=1300, title=f"Wyniki mailingow za lata {from_} - {to_}",
               toolbar_location='right',
               x_axis_label='Mailingi',
               y_axis_label='Suma wpłat/koszt')
    "dodaje druga os najpierw nazwe i zasieg potem layout i wykorzystuje nazwe i wkazuje strone"
    p.extra_y_ranges = {'secon_axis': Range1d(-100,200)}
    p.add_layout(LinearAxis(y_range_name="secon_axis", axis_label = 'naklad/liczba wpłat'), 'right')
    p.vbar(x=dodge('grupa_akcji_3_grupa_akcji_2',0.0, range=p.x_range), top='suma_wplat_mean', source=source, width=0.2, legend_label="Suma Wplat",)
    #p.line(x='grupa_akcji_3_grupa_akcji_2', y='koszt_calkowity_mean', legend_label="Temp.", line_width=2,source=source)
    p.vbar(x=dodge('grupa_akcji_3_grupa_akcji_2',-0.25, range=p.x_range), top='koszt_calkowity_mean', source=source, color='red', width=0.2,
           legend_label="Koszt")
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.axis.minor_tick_line_color = None
    p.y_range.start = 0
    p.x_range.range_padding = 0.1


    return p





