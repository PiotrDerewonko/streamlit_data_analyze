import itertools

from bokeh.transform import dodge
from colorcet import palette


class ChartBokehCreateChart:
    def __init__(self, df_with_options, figure, str_multindex, source, pivot_table):
        self.df_with_options = df_with_options
        self.figure = figure
        self.str_multindex = str_multindex
        self.source = source
        self.pivot_table = pivot_table
        self.colors_fin = []

    def create_bar_chart(self, position, parametr_name, axis, width):
        self.figure.vbar(x=dodge(self.str_multindex, position,
                                 range=self.figure.x_range), top=parametr_name, source=self.source,
                         width=width, legend_label=parametr_name, y_range_name=axis, color='blue')

    def create_line_chart(self, parametr_name, axis, colour):
        self.figure.line(self.pivot_table.index.values, self.pivot_table[f'''{parametr_name}'''], line_width=5,
                         y_range_name=axis,
                         legend=parametr_name, color=colour)

    def create_position_chart(self, parametr_name, axis, colour):
        self.figure.circle(self.pivot_table.index.values.index.values, self.pivot_table[f'''{parametr_name}'''],
                           y_range_name=axis,
                           legend=parametr_name, color=colour)

    # def create_stacke_bar_chart(self, str_mutlindex, position, source, value):
    #     self.figure.vbar_stack(test, x=dodge(str_mutlindex, position,
    #                                          range=self.figure.x_range), source=source, width=value,
    #                            legend_label=stock_second_axis['Nazwa parametru'].to_list(), y_range_name='default',
    #                            color=colors_fin_stock[len(stock_default):len(stock_default) + len(stock_second_axis)])

    def prepare_data(self):
        """Przygotowuje niezbene dane do tworzenia wykresu """
        self.df_with_options = self.df_with_options.replace({'Oś główna': 'default', 'Oś pomocnicza': 'secon_axis'})

        # sprawdzam ile jest wykresow słupkowych i ślukowych skumulowanych
        len_vbar_ = len((self.df_with_options.loc[self.df_with_options['Opcje'] == 'Wykres Słupkowy']))
        len_stock = len((self.df_with_options.loc[self.df_with_options['Opcje'] == 'Wykres Słupkowy Skumulowany']))
        tmp_vbar_stock_len = 0
        if len(self.df_with_options.loc[(self.df_with_options['Opcje'] == 'Wykres Słupkowy Skumulowany') &
                                   (self.df_with_options['oś'] == 'default')]):
            tmp_vbar_stock_len += 1
        if len(self.df_with_options.loc[(self.df_with_options['Opcje'] == 'Wykres Słupkowy Skumulowany') &
                                   (self.df_with_options['oś'] == 'secon_axis')]):
            tmp_vbar_stock_len += 1
        len_vbar = len_vbar_ + len_stock
        len_vbar_count = len_vbar_ + tmp_vbar_stock_len

        list_tmp = [0]
        tmp = 0

        if len_vbar >= 1:
            if len_vbar == 1:
                value = 0.8
            else:
                value = round(0.9 / len_vbar_count, 2)
            count = 1
            while tmp <= 1:
                list_tmp.append(count * value)
                list_tmp.append(count * value * -1)
                tmp += value
                count += 1

        colors = itertools.cycle(palette)
        for m, color in zip(range(len(self.df_with_options)), colors):
            self.colors_fin.append(color)
        j = 0
        count_of_y_prime = 0
        count_of_y_second = 0
        self.df_with_options.sort_values(['Opcje'], inplace=True)

    def create_chart(self):
        """Metoda dodajace do przekazanej figury obiekty"""

        for i, row in self.df_with_options.iterrows():

            if row['Opcje'] == 'Wykres Słupkowy':
                position = 0
                # count_of_y_prime += 1
                self.create_bar_chart(position, row['Nazwa parametru'], row['oś'], 0.8)
            elif row['Opcje'] == 'Wykres liniowy':
                self.create_line_chart(row['Nazwa parametru'], row['oś'], 'red')
                self.create_position_chart(row['Nazwa parametru'], row['oś'], 'red')

        return self.figure
