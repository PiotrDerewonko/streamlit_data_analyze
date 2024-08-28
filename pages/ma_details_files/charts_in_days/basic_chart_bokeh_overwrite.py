from bokeh.plotting import figure

from charts.basic_chart_bokeh import CreateCharts
from pages.ma_details_files.charts_in_days.basic_chart_bokeh_create_char_overwrite import \
    BasicChartBokehCreateChartOverwrite


class BasicChartBokehOverwrite(CreateCharts):
    index_for_char = None

    chart_class = BasicChartBokehCreateChartOverwrite

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

    def create_chart(self, chart_class):
        return super().create_chart(chart_class)
