import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from dotenv import dotenv_values

from database.source_db import deaful_set
from functions_pandas.plot_cam_adr_dash import pivot_and_chart_for_dash
from pages.ma_details_files.data_about_people_and_campaign_pay import download_data_about_people, \
    download_data_about_people_camp_pay, download_data_about_people_camp
from pages.ma_details_files.pivot_table.pivot_table_for_ma_details import create_pivot_table_for_ma_details, \
    style_pivot_table_for_ma


def create_pivot_table(con, refresh_data, engine, camp, year, columns_options, corr_method, options_char, filtr):
    sorce_main = dotenv_values('.env')
    sorce_main = list(sorce_main.values())[0]
    refresh_data = 'False'
    year_int = []
    for i in year:
        year_int.append(int(i))
    mail, con, engine = deaful_set(sorce_main)
    data_about_people = download_data_about_people(con, refresh_data, 0, [])
    data_about_pay = download_data_about_people_camp_pay(con, refresh_data, engine)
    data_about_camp = download_data_about_people_camp(con, refresh_data, engine)

    if len(camp)>=1:
        z = 0
        camp2 = camp.copy()
        for j in camp2:
            if j == 'MAILING Q1':
                camp2[z] = 'Q1.1'
            if j == 'MAILING Q2':
                camp2[z] = 'Q2'
            if j == 'MAILING Q3':
                camp2[z] = 'Q3.1'
            if j == 'MAILING Q4':
                camp2[z] = 'Q4'
            z += 1


        data_about_camp = data_about_camp[data_about_camp['grupa_akcji_2_wysylki'].isin(camp2)]
    if len(year_int)>=1:
        data_about_camp = data_about_camp[data_about_camp['grupa_akcji_3_wysylki'].isin(year_int)]
        year_int.sort()
    data_all = pd.merge(data_about_camp, data_about_pay, left_on=['id_korespondenta', 'kod_akcji_wysylki'],
                        right_on=['id_korespondenta', 'kod_akcji_wplaty'], how='left')
    data_all = pd.merge(data_all, data_about_people, on='id_korespondenta', how='left')
    title_with_filtr = 'z filtrami '
    for i in filtr:
        a = i[0]
        b = i[1]
        if i[0] != ' ':
            if len(i[1]) >= 1:
                data_all = data_all.loc[data_all[i[0]].isin(i[1])]
                title_with_filtr = title_with_filtr + f'{i[0]}' + ' ' + f'{i[1]}' + ', '
    if title_with_filtr == 'z filtrami ':
        title_with_filtr = ''

    data_all['grupa_akcji_3_wysylki'] = data_all['grupa_akcji_3_wysylki'].astype(str)
    data_all['naklad'] = 1
    data_all['suma_wplat_stand'] = data_all['suma_wplat'].loc[(data_all['suma_wplat']>=10) & (data_all['suma_wplat']<=10000)]
    #pivot_to_return = pivot_table_w_subtotals(data_all,['suma_wplat', 'liczba_wplat', 'koszt'],columns_options, aggfunc='sum',columns= [],
    #                                          fill_value=0)

    pivot_to_return = create_pivot_table_for_ma_details(data_all, columns_options)

    #kopjuje tabele przestawna przed formatowaniem
    pivot_to_return_values = pivot_to_return.copy()
    plt.figure(figsize=(16, 9))
    columns_options.append('suma_wplat')
    columns_options.append('liczba_wplat')
    data_all_copy = data_all.copy()

    #tworze wykres korelacji
    for j in columns_options:
        tmp = data_all[j].drop_duplicates().sort_values()
        tmp = tmp.to_frame()
        #tmp.reset_index(inplace=True)
        type_of_tmp = tmp.dtypes
        if type_of_tmp[j] == 'object':
            for k, row in tmp.iterrows():
                data_all[j] = data_all[j].replace(row[j], f'{k}')
            data_all[j] = data_all[j].astype(int)
    data_all = data_all[columns_options].replace('nie posiada.+?', 0, regex=True)
    data_all= data_all[columns_options].replace('posiada.+?', 1, regex=True)
    korelacja = data_all[columns_options].corr(corr_method)
    kor = sns.heatmap(korelacja)
    plt.title(f'Dane dla mailingu {camp} za lata {year_int} przy pomocy metody {corr_method}')

    #stylizuje tabele przestawna
    pivot_to_return_style = style_pivot_table_for_ma(pivot_to_return)

    columns_options.remove('suma_wplat')
    columns_options.remove('liczba_wplat')
    if len(columns_options) > 3:
        columns_options = columns_options[:3]
        pivot_to_return_values = create_pivot_table_for_ma_details(data_all_copy, columns_options)
    char, a = pivot_and_chart_for_dash(data_all_copy, columns_options, 'me_detail', 'Wykres ', 'Kolumny', {},
                                       pivot_to_return_values, options_char, f'Dane dla mailingu {camp} za lata {year_int} {title_with_filtr}')
    return pivot_to_return_style, plt,  pivot_to_return_values, char



