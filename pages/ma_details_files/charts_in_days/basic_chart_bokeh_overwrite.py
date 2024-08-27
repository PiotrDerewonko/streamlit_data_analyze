from bokeh.plotting import figure

from charts.basic_chart_bokeh import CreateCharts


class BasicChartBokehOverwrite(CreateCharts):
    index_for_char = None

    def create_figure(self, index_for_char):
        """Metoda tworzaca figure do ktorej nastepnie dodawane sa wykresy"""

        p = figure(
            height=800,
            title=f"{self.title}",
            toolbar_location='right',
            x_axis_label=self.xlabel,
            y_axis_label=self.ylabel,
            sizing_mode='stretch_both'
        )
        return p
