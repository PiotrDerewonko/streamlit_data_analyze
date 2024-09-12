import itertools

from bokeh.palettes import Category20_20 as palette
from bokeh.palettes import Category20_20 as palette_for_prim
from bokeh.transform import dodge


class ChartBokehCreateChart:
    def __init__(self, df_with_options, figure, str_multindex, source, pivot_table):
        self.df_with_options = df_with_options
        self.figure = figure
        self.str_multindex = str_multindex
        self.source = source
        self.pivot_table = pivot_table
        self.colors_fin = []
        self.colour_number = 0
        self.width_value_for_bar = 0
        self.list_of_position_bar_chars = [0.0]
        self.count_of_y_prime = 0
        self.len_stock = None

    def create_bar_chart(self, position, parametr_name, axis, width, colour):
        self.figure.vbar(x=dodge(self.str_multindex, position,
                                 range=self.figure.x_range), top=parametr_name, source=self.source,
                         width=width, legend_label=parametr_name, y_range_name=axis, color=colour)

    def create_line_chart(self, parametr_name, axis, colour):
        self.figure.line(self.pivot_table.index.values, self.pivot_table[parametr_name], line_width=5,
                         y_range_name=axis,
                         legend=f'{parametr_name}', color=colour)

    def create_position_chart(self, parametr_name, axis, colour):
        self.figure.circle(self.pivot_table.index.values, self.pivot_table[parametr_name],
                           y_range_name=axis, size=12, color=colour)

    def create_stacke_bar_chart(self, str_mutlindex, position, source, value, colors_fin_stock, stock_second_axis,
                                stock_default, test, y_range_name):
        self.figure.vbar_stack(test, x=dodge(str_mutlindex, position,
                                             range=self.figure.x_range), source=source, width=value,
                               legend_label=stock_second_axis['Nazwa parametru'].to_list(), y_range_name=y_range_name,
                               color=colors_fin_stock[len(stock_default):len(stock_default) + len(stock_second_axis)])

    def count_weidht_and_position(self, len_vbar, len_vbar_count):
        # zmienna pomocnicza do wyliczenia ile ma byc pozycji na liscie
        tmp = 0

        # wyliczam jaka szerokosc ma miesc wykres slukowy oraz na jkich pozycjach maja byc poszczegolne slupki
        if len_vbar >= 1:
            if len_vbar == 1:
                self.width_value_for_bar = 0.8
            else:
                self.width_value_for_bar = round(0.9 / len_vbar_count, 2)
            count = 1
            while tmp <= 1:
                self.list_of_position_bar_chars.append(count * self.width_value_for_bar)
                self.list_of_position_bar_chars.append(count * self.width_value_for_bar * -1)
                tmp += self.width_value_for_bar
                count += 1

    def prepare_data(self):
        """Przygotowuje niezbene dane do tworzenia wykresu """
        self.df_with_options = self.df_with_options.replace({'Oś główna': 'default', 'Oś pomocnicza': 'secon_axis'})

        # sprawdzam ile jest wykresow słupkowych i ślukowych skumulowanych
        len_vbar_ = len((self.df_with_options.loc[self.df_with_options['Opcje'] == 'Wykres Słupkowy']))
        self.len_stock = len((self.df_with_options.loc[self.df_with_options['Opcje'] == 'Wykres Słupkowy Skumulowany']))
        tmp_vbar_stock_len = 0
        if len(self.df_with_options.loc[(self.df_with_options['Opcje'] == 'Wykres Słupkowy Skumulowany') &
                                        (self.df_with_options['oś'] == 'default')]):
            tmp_vbar_stock_len += 1
        if len(self.df_with_options.loc[(self.df_with_options['Opcje'] == 'Wykres Słupkowy Skumulowany') &
                                        (self.df_with_options['oś'] == 'secon_axis')]):
            tmp_vbar_stock_len += 1

        len_vbar = len_vbar_ + self.len_stock
        len_vbar_count = len_vbar_ + tmp_vbar_stock_len

        self.count_weidht_and_position(len_vbar, len_vbar_count)

        # tworze palete kolorow dla wykresow zwyklych
        colors = itertools.cycle(palette)
        for m, color in zip(range(len(self.df_with_options)), colors):
            self.colors_fin.append(color)
        self.df_with_options.sort_values(['Opcje'], inplace=True)

    def create_chart(self):
        """Metoda dodajace do przekazanej figury obiekty"""

        # wydzielam tylko te wiersze ktore maja wykres slupkowy skumulowany
        if self.len_stock >= 1:
            self.df_with_options.reset_index(inplace=True)
            stock = self.df_with_options.loc[self.df_with_options['Opcje'] == 'Wykres Słupkowy Skumulowany']
            stock_default = stock.loc[stock['oś'] == 'default']
            stock_second_axis = stock.loc[stock['oś'] == 'secon_axis']

            # okreslam dodatkowa palete kolorow dla wykresow slupkowych kumulacyjnych
            colors_fin_stock = []
            colors_stock = itertools.cycle(palette_for_prim)
            for m2, color2 in zip(range(len(stock_default) + len(stock_second_axis)), colors_stock):
                colors_fin_stock.append(color2)
            if len(stock_default) >= 1:
                position = self.list_of_position_bar_chars[self.count_of_y_prime]
                self.count_of_y_prime += 1
                pt_columns = self.pivot_table.columns
                pt_columns = pt_columns.to_list()
                # test = self.pivot_table[stock_default['Nazwa parametru'].to_list()].columns
                self.create_stacke_bar_chart(self.str_multindex, position, self.source, self.width_value_for_bar,
                                             colors_fin_stock, stock_second_axis, stock_default, pt_columns, 'default')
                self.colour_number += 1
            if len(stock_second_axis) >= 1:
                position = self.list_of_position_bar_chars[self.count_of_y_prime]
                self.count_of_y_prime += 1
                test = self.pivot_table[stock_second_axis['Nazwa parametru'].to_list()].columns
                self.create_stacke_bar_chart(self.str_multindex, position, self.source, self.width_value_for_bar,
                                             colors_fin_stock, stock_second_axis, stock_default, test, 'secon_axis')
                self.colour_number += 1

        for i, row in self.df_with_options.iterrows():

            if row['Opcje'] == 'Wykres Słupkowy':
                position = self.list_of_position_bar_chars[self.count_of_y_prime]
                self.count_of_y_prime += 1
                self.create_bar_chart(position, row['Nazwa parametru'], row['oś'], width=self.width_value_for_bar,
                                      colour=self.colors_fin[self.colour_number])
            elif row['Opcje'] == 'Wykres liniowy':
                self.create_line_chart(row['Nazwa parametru'], row['oś'], colour=self.colors_fin[self.colour_number])
                self.create_position_chart(row['Nazwa parametru'], row['oś'],
                                           colour=self.colors_fin[self.colour_number])

            self.colour_number += 1

        self.figure.legend.location = 'top_left'

        return self.figure
