from charts.basic_chart_bokeh_create_char import ChartBokehCreateChart


class BasicChartBokehCreateChartOverwrite(ChartBokehCreateChart):

    def create_line_chart(self, parametr_name, axis, colour, *args, **kwargs):
        legend = kwargs.get('legend', parametr_name)
        self.figure.line(self.pivot_table.index.values, self.pivot_table[parametr_name], line_width=5,
                         y_range_name=axis,
                         legend=legend, color=colour)

    def create_chart(self):
        """Nadpisuje domyslna metode w celu iinnego prezentowania danych na wykresie liniowym"""
        for i, row in self.df_with_options.iterrows():
            self.create_line_chart(row['Nazwa parametru'], row['oś'], colour=self.colors_fin[self.colour_number],
                                   legend=f"""{row['Nazwa parametru']} - naklad {row['Nakład']})""")
            self.create_position_chart(row['Nazwa parametru'], row['oś'],
                                           colour=self.colors_fin[self.colour_number])
            self.colour_number += 1

        self.figure.legend.location = 'top_left'

        return self.figure




