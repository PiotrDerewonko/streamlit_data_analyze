from bokeh.plotting import ColumnDataSource

from streamlit_functions.dashboard.operation_for_char import check_max_value


class SetOptions:
    def __init__(self, main_class, pivot_table, df_with_options):
        self.main_class = main_class
        self.pivot_table = pivot_table
        self.df_with_options = df_with_options
        self.max_value_for_y_prime = None
        self.max_value_for_y_second = None
        self.index_for_char = None
        self.source = None
        self.is_second_x_axis = False

    def check_max_value_for_prime_y_axis(self):
        max_value_for_y_prime = check_max_value(self.pivot_table, self.df_with_options, 'Oś główna')
        return max_value_for_y_prime

    def check_max_value_for_second_y_axis(self):
        max_value_for_y_second = check_max_value(self.pivot_table, self.df_with_options, 'Oś pomocnicza')
        return max_value_for_y_second

    def set_options(self):
        if self.main_class.dict_of_orientations is not None:
            self.main_class.major_x_label_oriantation = self.main_class.dict_of_orientations['major']
            self.main_class.group_x_label_oriantation = self.main_class.dict_of_orientations['group']
            self.main_class.sub_group_x_label_oriantation = self.main_class.dict_of_orientations['sub_group']
        if len(self.main_class.df_with_options.loc[self.main_class.df_with_options['oś'] == 'Oś pomocnicza']) > 0:
            self.is_second_x_axis = True
            self.max_value_for_y_second = self.check_max_value_for_second_y_axis()
        else:
            self.is_second_x_axis = False
            self.max_value_for_y_second = None
        self.max_value_for_y_prime = self.check_max_value_for_prime_y_axis()
        self.main_class.pivot_table = self.main_class.pivot_table.fillna(value=0)
        index_for_char = self.main_class.data.groupby(self.main_class.multindex, dropna=True)
        source = ColumnDataSource(self.main_class.pivot_table)
        str_mutlindex = ''
        j = 0
        for i in self.main_class.multindex:
            if j == 0:
                str_mutlindex = i
                j += 1
            else:
                str_mutlindex = str_mutlindex + "_" + i
        return (index_for_char, source, str_mutlindex, self.max_value_for_y_prime, self.max_value_for_y_second,
                self.is_second_x_axis)
