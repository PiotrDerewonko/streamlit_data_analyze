from typing import Optional

import pandas as pd
import streamlit as st
from bokeh.models import Legend, Range1d, LinearAxis
from bokeh.plotting import figure

from charts.basic_chart_bokeh_create_char import ChartBokehCreateChart
from charts.basic_chart_bokeh_set_options import SetOptions


class CreateCharts:
    is_second_x_axis = False
    major_x_label_oriantation = "vertical"
    group_x_label_oriantation = "horizontal"
    sub_group_x_label_oriantation = "horizontal"

    def __init__(self, data: pd.DataFrame, multindex: list, title: str, xlabel: str, ylabel: str,
                 pivot_table: pd.DataFrame, df_with_options: pd.DataFrame, dict_of_orientations: Optional[dict] = None,
                 y_label_second: Optional[str] = None):
        self.data = data
        self.multindex = multindex
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.pivot_table = pivot_table
        self.df_with_options = df_with_options
        self.dict_of_orientations = dict_of_orientations
        self.y_label_second = y_label_second

    def create_chart(self):
        """Metoda tworzaca wykresy, w pierwszej kolejnosci tworze obiekt, ktory bedzie ustawial podsatwowe opcje
         wykresu"""
        char_options = SetOptions(self, self.pivot_table, self.df_with_options)
        (index_for_char, source, str_mutlindex, max_value_for_y_prime, max_value_for_y_second,
         is_second_x_axis) = char_options.set_options()
        figure = self.create_figure(index_for_char)
        figure_after_custom = self.custom_figure(figure, max_value_for_y_prime, max_value_for_y_second,
                                                 is_second_x_axis)
        final_char_obj = ChartBokehCreateChart(self.df_with_options, figure_after_custom, str_mutlindex, source,
                                           self.pivot_table)
        final_char_obj = final_char_obj.create_chart()
        st.bokeh_chart(final_char_obj)


    def create_figure(self, index_for_char):
        """Metoda tworzaca figure do ktorej nastepnie dodawane sa wykresy"""
        p = figure(x_range=index_for_char,
                   height=800,
                   title=f"{self.title}",
                   toolbar_location='right',
                   x_axis_label=self.xlabel,
                   y_axis_label=self.ylabel,
                   sizing_mode='stretch_both')
        return p

    def custom_figure(self, p, max_value_for_y_prime, max_value_for_y_second, is_second_x_axis):
        """Metoda w której konfigurujemy wyglad figury takie jak, wielkosc czcionki, orientacja itd"""
        p.title.text_font_size = '12pt'
        p.add_layout(Legend(background_fill_alpha=0.3))

        # ustawienie orintacji etykiet na osi x
        if self.dict_of_orientations is not None:
            p.xaxis.major_label_orientation = self.major_x_label_oriantation
            p.xaxis.group_label_orientation = self.group_x_label_oriantation
            p.xaxis.subgroup_label_orientation = self.sub_group_x_label_oriantation
        else:
            p.xaxis.major_label_orientation = CreateCharts.major_x_label_oriantation
            p.xaxis.group_label_orientation = CreateCharts.group_x_label_oriantation
            p.xaxis.subgroup_label_orientation = CreateCharts.sub_group_x_label_oriantation

        # ustawienie wielkosci czionek
        p.xaxis.major_label_text_font_size = "13pt"
        p.xaxis.axis_label_text_font_size = "13pt"
        p.yaxis.major_label_text_font_size = "13pt"
        p.xaxis.subgroup_text_font_size = "13pt"
        p.xaxis.group_text_font_size = "14pt"
        p.title.text_font_size = '18pt'

        # ustawienie zakresów osi i ewentualne tworzenie dodatkowe osi
        p.y_range = Range1d(0, max_value_for_y_prime * 1.1)
        if is_second_x_axis:
            p.extra_y_ranges = {'secon_axis': Range1d(0, max_value_for_y_second * 1.1)}
            p.add_layout(LinearAxis(y_range_name="secon_axis", axis_label=self.y_label_second), 'right')
            p.yaxis.axis_label_text_font_size = "15pt"

        # wylaczam tryb naukowy, dzieki czemu pokazuja sie pelni liczby a nie ich potegi
        p.yaxis.formatter.use_scientific = False

        return p
