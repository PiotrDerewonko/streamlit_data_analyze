
import bokeh
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import Plot, VBar, LinearAxis
import matplotlib.pyplot as plt

def pivot_for_dash(data):
    data['grupa_akcji_3'] = data['grupa_akcji_3'].astype(str)
    gr2 = data['grupa_akcji_2'].drop_duplicates().to_list()
    gr3 = data['grupa_akcji_3'].drop_duplicates().to_list()
    gr2 = ['KARDYNALSKA LUTY', 'MAILING Q3 KUSTOSZ LIPIEC', 'MAILING Q4', 'MAILING Q2', 'KARDYNALSKA SIERPIEŃ', 'MAILING Q1', 'MAILING Q3']
    data2 = data[['grupa_akcji_3',  'suma_wplat']]
    group = data.groupby(['grupa_akcji_3','grupa_akcji_2'])
    source = ColumnDataSource(data=group)

    p = figure(x_range=group,
               height=250, title="Wyniki mailingow za lata",
               toolbar_location=None)
    #p.vbar_stack(gr3, x='grupa_akcji_2', width=0.9,  source=source,
    #             legend_label=gr3)
    p.vbar(x='grupa_akcji_3_grupa_akcji_2', top='suma_wplat_mean', source=source, width=0.8)
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.y_range.start = 0
    p.x_range.range_padding = 0.1


    return p





