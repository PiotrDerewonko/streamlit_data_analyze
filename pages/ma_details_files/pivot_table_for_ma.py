import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from dotenv import dotenv_values

from database.source_db import deaful_set
from functions_pandas.data_to_100_percent import data_to_100_percent
from functions_pandas.plot_cam_adr_dash import pivot_and_chart_for_dash
from pages.ma_details_files.data_about_people_and_campaign_pay import download_data_about_people, \
    download_data_about_people_camp_pay, download_data_about_people_camp, data_pay_all
from pages.ma_details_files.pivot_table.pivot_table_for_ma_details import create_pivot_table_for_ma_details, \
    style_pivot_table_for_ma


def create_pivot_table(camp, year, type_of_campaign, columns_options, corr_method, options_char, filtr, tit,
                       sub_tit, dict_of_oriantation, is_post):
    sorce_main = dotenv_values('.env')
    sorce_main = list(sorce_main.values())[0]
    refresh_data = 'False'
    year_int = []
    for i in year:
        year_int.append(int(i))
    mail, con, engine = deaful_set(sorce_main)
    data_about_people = download_data_about_people(con, refresh_data, 0, [])
    data_about_pay_orig = download_data_about_people_camp_pay(con, refresh_data, engine)
    data_about_camp = download_data_about_people_camp(con, refresh_data, engine)
    days = pd.read_excel('./pages/ma_details_files/tmp_file/days.xlsx', sheet_name='Sheet1')

    if len(camp) >= 1:
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
            if j == 'KARDYNALSKA LUTY':
                camp2[z] = 'Q1.0 KARD'
            if j == 'KARDYNALSKA SIERPIEŃ':
                camp2[z] = 'Q3.0 KARD'
            z += 1

        data_about_camp = data_about_camp[data_about_camp['grupa_akcji_2_wysylki'].isin(camp)]
        days = days[days['grupa_akcji_2_wplaty'].isin(camp)]
    if len(year_int) >= 1:
        data_about_camp = data_about_camp[data_about_camp['grupa_akcji_3_wysylki'].isin(year_int)]
        days = days[days['grupa_akcji_3_wplaty'].isin(year_int)]
        year_int.sort()

    if len(type_of_campaign) >= 1:
        data_about_camp = data_about_camp[data_about_camp['grupa_akcji_1_wysylki'].isin(type_of_campaign)]
        days = days[days['grupa_akcji_3_wplaty'].isin(year_int)]

    for i in filtr[3:]:
        if i[1] != ' ':
            minimum_value = days['dzien_po_mailingu'].min()
            data_about_pay_orig = data_about_pay_orig.loc[data_about_pay_orig['dzien_po_mailingu'] <= minimum_value]
    data_about_pay = pd.pivot_table(data=data_about_pay_orig,
                                    index=['id_korespondenta', 'grupa_akcji_2_wplaty', 'grupa_akcji_3_wplaty'],
                                    values=['suma_wplat', 'liczba_wplat'], aggfunc='sum')

    # data_about_camp= data_about_camp['kod_akcji_wysylki'].replace('_', ' ', regex=True)

    data_uniq = data_about_camp.loc[data_about_camp['row_number'] == 1]
    data_not_uniq = data_about_camp.loc[data_about_camp['row_number'] != 1]
    data_all = pd.merge(data_uniq, data_about_pay,
                        left_on=['id_korespondenta', 'grupa_akcji_2_wysylki', 'grupa_akcji_3_wysylki'],
                        right_on=['id_korespondenta', 'grupa_akcji_2_wplaty', 'grupa_akcji_3_wplaty'], how='left')
    data_all = pd.concat([data_all, data_not_uniq])

    data_all = pd.merge(data_all, data_about_people, on='id_korespondenta', how='left')
    data_all['kod_akcji_wysylki'] = data_all['kod_akcji_wysylki'].replace('_', ' ', regex=True)
    data_all['kod_akcji_wysylki'] = data_all['kod_akcji_wysylki'].str[12:]
    data_all.drop_duplicates(inplace=True)
    title_with_filtr = 'z filtrami '
    for i in filtr[0:3]:
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
    data_all['suma_wplat_stand'] = data_all['suma_wplat'].loc[
        (data_all['suma_wplat'] >= 10) & (data_all['suma_wplat'] <= 10000)]
    # pivot_to_return = pivot_table_w_subtotals(data_all,['suma_wplat', 'liczba_wplat', 'koszt'],columns_options, aggfunc='sum',columns= [],
    #                                          fill_value=0)

    pivot_to_return = create_pivot_table_for_ma_details(data_all, columns_options)

    # kopjuje tabele przestawna przed formatowaniem
    pivot_to_return_values = pivot_to_return.copy()
    plt.figure(figsize=(16, 9))
    columns_options.append('suma_wplat')
    columns_options.append('liczba_wplat')
    data_all_copy = data_all.copy()

    # tworze wykres korelacji
    for j in columns_options:
        tmp = data_all[j].drop_duplicates().sort_values()
        tmp = tmp.to_frame()
        # tmp.reset_index(inplace=True)
        type_of_tmp = tmp.dtypes
        if type_of_tmp[j] == 'object':
            for k, row in tmp.iterrows():
                data_all[j] = data_all[j].replace(row[j], f'{k}')
            data_all[j] = data_all[j].astype(int)
    data_all = data_all[columns_options].replace('nie posiada.+?', 0, regex=True)
    data_all = data_all[columns_options].replace('posiada.+?', 1, regex=True)
    korelacja = data_all[columns_options].corr(corr_method)
    kor = sns.heatmap(korelacja)
    plt.title(f'Dane dla mailingu {camp} za lata {year_int} przy pomocy metody {corr_method}')

    # stylizuje tabele przestawna
    pivot_to_return_style = style_pivot_table_for_ma(pivot_to_return)

    columns_options.remove('suma_wplat')
    columns_options.remove('liczba_wplat')
    if len(columns_options) > 3:
        columns_options = columns_options[:3]
        pivot_to_return_values = create_pivot_table_for_ma_details(data_all_copy, columns_options)
    if tit != '':
        title_fin = tit
        if sub_tit != '':
            title_fin = f'''{title_fin}
            {sub_tit}'''
    else:
        title_fin = f'''Dane dla mailingu {camp} za lata {year_int}\n{title_with_filtr}'''
    char, a = pivot_and_chart_for_dash(data_all_copy[columns_options], columns_options, 'me_detail', 'Wykres ',
                                       'Wybrane kolumny', {},
                                       pivot_to_return_values, options_char, title_fin, dict_of_oriantation)

    #######################################################################################################

    # tworze wykres struktury wplat
    data_about_pay_all = data_pay_all(con, refresh_data)
    data_about_pay_all['grupa_akcji_3_wplaty'] = data_about_pay_all['grupa_akcji_3_wplaty'].astype(str)

    if len(camp) >= 1:
        data_about_pay_all = data_about_pay_all[data_about_pay_all['grupa_akcji_2_wplaty'].isin(camp)]
    if len(year_int) >= 1:
        data_about_pay_all = data_about_pay_all[data_about_pay_all['grupa_akcji_3_wplaty'].isin(year)]

    for z in filtr[3:]:
        if z[1] != ' ':
            minimum_value = days['dzien_po_mailingu'].min()
            data_about_pay_all = data_about_pay_all.loc[data_about_pay_all['dzien_po_mailingu'] <= minimum_value]
    data_all_copy.drop_duplicates(subset=['id_korespondenta', 'grupa_akcji_2_wysylki', 'grupa_akcji_3_wysylki'],
                                  inplace=True)
    data_to_structure = pd.merge(data_about_pay_all, data_all_copy,
                                 left_on=['id_korespondenta', 'grupa_akcji_2_wplaty', 'grupa_akcji_3_wplaty'],
                                 right_on=['id_korespondenta', 'grupa_akcji_2_wysylki', 'grupa_akcji_3_wysylki'],
                                 how='left')
    data_to_structure.drop(columns=['suma_wplat_y'], inplace=True)
    data_to_structure.rename(columns={'suma_wplat_x': 'suma_wplat'}, inplace=True)
    data_to_structure.drop_duplicates(subset=['id_korespondenta', 'grupa_akcji_2_wplaty', 'grupa_akcji_3_wplaty'],
                                      inplace=True)
    data_to_structure['rok_dodania'] = data_to_structure['rok_dodania'].astype(str)
    if is_post:
        columns_options.append('poczta')
    pivot_for_structure = data_to_structure.pivot_table(values=['suma_wplat'], columns=['przedzialy'],
                                                        aggfunc='count',
                                                        index=columns_options, margins=True, margins_name='Ilość')
    list_of_column_values = pivot_for_structure.columns.values
    pivot_for_structure.columns = ['_'.join(col) for col in list_of_column_values]
    pivot_only_margin = pivot_for_structure.iloc[:-1, -1]
    pivot_for_structure = pivot_for_structure.iloc[:-1, :-1]
    pivot_for_structure_values = pivot_for_structure.copy()
    # tworze tabele przestwna z ukladem do 100 %
    pivot_for_structure = data_to_100_percent(pivot_for_structure)
    pivot_for_structure = pd.merge(left=pivot_for_structure, right=pivot_only_margin, left_index=True, right_index=True)
    columns_name = pivot_for_structure.columns
    index_column_name = []
    j = 0
    for i in columns_name:
        index_column_name.append(j)
        j += 1
    d = {'Nazwa parametru': columns_name}
    new_option_char = pd.DataFrame(data=d, index=index_column_name)
    new_option_char['oś'] = 'Oś główna'
    new_option_char['Opcje'] = 'Wykres Słupkowy Skumulowany'
    new_option_char['oś'].iloc[-1] = 'Oś pomocnicza'
    new_option_char['Opcje'].iloc[-1] = 'Wykres liniowy'
    char_structure, b = pivot_and_chart_for_dash(data_to_structure[columns_options], columns_options, 'me_detail',
                                                 'Wykres ', 'Wybrane kolumny', {},
                                                 pivot_for_structure, new_option_char, title_fin, dict_of_oriantation)

    return pivot_to_return_style, kor, pivot_to_return_values, char, char_structure, pivot_for_structure_values
