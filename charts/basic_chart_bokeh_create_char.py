from bokeh.transform import dodge


class ChartBokehCreateChart:
    def __init__(self, df_with_options, figure, str_multindex, source, pivot_table):
        self.df_with_options = df_with_options
        self.figure = figure
        self.str_multindex = str_multindex
        self.source = source
        self.pivot_table = pivot_table

    def create_chart(self):
        """Metoda dodajace do przekazanej figury obiekty"""

        df_with_options = self.df_with_options.replace({'Oś główna': 'default', 'Oś pomocnicza': 'secon_axis'})

        # sprawdzam ile jest wykresow słupkowych i ślukowych skumulowanych
        len_vbar_ = len((df_with_options.loc[df_with_options['Opcje'] == 'Wykres Słupkowy']))
        len_stock = len((df_with_options.loc[df_with_options['Opcje'] == 'Wykres Słupkowy Skumulowany']))
        tmp_vbar_stock_len = 0
        if len(df_with_options.loc[(df_with_options['Opcje'] == 'Wykres Słupkowy Skumulowany') &
                                   (df_with_options['oś'] == 'default')]):
            tmp_vbar_stock_len += 1
        if len(df_with_options.loc[(df_with_options['Opcje'] == 'Wykres Słupkowy Skumulowany') &
                                   (df_with_options['oś'] == 'secon_axis')]):
            tmp_vbar_stock_len += 1

        len_vbar = len_vbar_ + len_stock
        len_vbar_count = len_vbar_ + tmp_vbar_stock_len

        for i, row in df_with_options.iterrows():

            if row['Opcje'] == 'Wykres Słupkowy':
                position = 0
                # count_of_y_prime += 1
                self.figure.vbar(x=dodge(self.str_multindex, position,
                                         range=self.figure.x_range), top=row['Nazwa parametru'], source=self.source,
                                 width=0.8, legend_label=row['Nazwa parametru'], y_range_name=row['oś'], color='blue')
        return self.figure
