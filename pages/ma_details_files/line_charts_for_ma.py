import itertools

from bokeh.palettes import Dark2_5 as palette
from bokeh.plotting import figure


def line_chart_for_m(pivot):
    p = figure(height=700, width=1500,
               toolbar_location='right')
    colors_fin = []
    colors = itertools.cycle(palette)
    for m, color in zip(range(len(pivot.columns)), colors):
        colors_fin.append(color)
    j = 0
    for i in pivot.columns:
        p.line(pivot.index.values, pivot[i], line_width=3, legend=f'{i}', color=colors_fin[j]
               )
        j += 1
    p.legend.location = 'top_left'
    p.yaxis.formatter.use_scientific = False
    return p