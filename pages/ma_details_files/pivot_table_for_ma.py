import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.ma_details_files.data_about_people_and_campaign_pay import download_data_about_people, \
    download_data_about_people_camp_pay, download_data_about_people_camp


def create_pivot_table(con, refresh_data, engine, camp, year, columns_options, corr_method):
    sorce_main = dotenv_values('.env')
    sorce_main = list(sorce_main.values())[0]
    refresh_data = 'False'
    year_int = []
    for i in year:
        year_int.append(int(i))
    mail, con, engine = deaful_set(sorce_main)
    data_about_people = download_data_about_people(con, refresh_data, engine)
    data_about_pay = download_data_about_people_camp_pay(con, refresh_data, engine)
    data_about_camp = download_data_about_people_camp(con, refresh_data, engine)
    if len(camp)>=1:
        data_about_camp = data_about_camp[data_about_camp['grupa_akcji_2_wysylki'].isin(camp)]
    if len(year_int)>=1:
        data_about_camp = data_about_camp[data_about_camp['grupa_akcji_3_wysylki'].isin(year_int)]
    data_all = pd.merge(data_about_camp, data_about_pay, left_on=['id_korespondenta', 'kod_akcji_wysylki'],
                        right_on=['id_korespondenta', 'kod_akcji_wplaty'], how='left')
    data_all = pd.merge(data_all, data_about_people, on='id_korespondenta', how='left')
    data_all['grupa_akcji_3_wysylki'] = data_all['grupa_akcji_3_wysylki'].astype(str)
    data_all['naklad'] = 1
    data_all['suma_wplat_stand'] = data_all['suma_wplat'].loc[(data_all['suma_wplat']>=10) & (data_all['suma_wplat']<=10000)]
    #pivot_to_return = pivot_table_w_subtotals(data_all,['suma_wplat', 'liczba_wplat', 'koszt'],columns_options, aggfunc='sum',columns= [],
    #                                          fill_value=0)
    pivot_to_return = data_all.pivot_table(values=['suma_wplat', 'liczba_wplat', 'koszt', 'naklad', 'suma_wplat_stand'], aggfunc='sum',
                                           index=columns_options)
    def my25(g):
        return g.quantile(0.25)
    def my75(g):
        return g.quantile(0.75)


    pivot_to_return_2 = data_all.pivot_table(values=['suma_wplat_stand'], aggfunc=[ my25,np.median, my75, np.std],
                                           index=columns_options)

    pivot_to_return = pivot_to_return.merge(pivot_to_return_2, how='left', left_index=True, right_index=True)
    a = pivot_to_return.columns
    pivot_to_return.rename(columns={a[5]: '1 percentyl'}, inplace=True)
    pivot_to_return.rename(columns={a[6]: 'mediana'}, inplace=True)
    pivot_to_return.rename(columns={a[7]: '3 percentyl'}, inplace=True)
    pivot_to_return.rename(columns={a[8]: 'Odchylenie'}, inplace=True)
    pivot_to_return['średnia'] = pivot_to_return['suma_wplat']/pivot_to_return['liczba_wplat']
    pivot_to_return['ROI'] = pivot_to_return['suma_wplat']/pivot_to_return['koszt']
    pivot_to_return['SZLW'] = (pivot_to_return['liczba_wplat']/pivot_to_return['naklad'])*100
    plt.figure(figsize=(16, 9))
    columns_options.append('suma_wplat')
    columns_options.append('liczba_wplat')
    data_all = data_all[columns_options].replace('nie posiada.+?', 0, regex=True)
    data_all= data_all[columns_options].replace('posiada.+?', 1, regex=True)
    korelacja = data_all[columns_options].corr(corr_method)
    kor = sns.heatmap(korelacja)
    plt.title(f'Dane dla mailingu {camp} za lata {year_int} przy pomocy metody {corr_method}')
    #pivot_to_return['średnia'] = pivot_to_return['suma_wplat']/pivot_to_return['liczba_wplat']
    cell_hover = {  # for row hover use <tr> instead of <td>
        'selector': 'td:hover',
        'props': [('background-color', '#ffffb3')]
    }
    def highlight_everyother(s):
        return ['background-color: yellow' if x % 2 == 1 else ''
                for x in range(len(s))]

    pivot_to_return['suma_wplat'].loc[pivot_to_return.index.isin(pivot_to_return.index)] = \
        pivot_to_return['suma_wplat'].apply(lambda x: "{:.0f} zł".format(x))
    pivot_to_return['koszt'].loc[pivot_to_return.index.isin(pivot_to_return.index)] = \
        pivot_to_return['koszt'].apply(lambda x: "{:.0f} zł".format(x))
    pivot_to_return['liczba_wplat'].loc[pivot_to_return.index.isin(pivot_to_return.index)] = \
        pivot_to_return['liczba_wplat'].apply(lambda x: "{:.0f}".format(x))
    pivot_to_return['średnia'].loc[pivot_to_return.index.isin(pivot_to_return.index)] = \
        pivot_to_return['średnia'].apply(lambda x: "{:.0f} zł".format(x))
    pivot_to_return['ROI'].loc[pivot_to_return.index.isin(pivot_to_return.index)] = \
        pivot_to_return['ROI'].apply(lambda x: "{:.2f} zł".format(x))
    pivot_to_return['SZLW'].loc[pivot_to_return.index.isin(pivot_to_return.index)] = pivot_to_return['SZLW'].\
        apply(lambda x: "{:.0f} %".format(x))

    t = pivot_to_return.style.apply(highlight_everyother)
    t.set_table_styles([{"selector": "", "props": [("border", "1px solid grey")]}])
    t.set_table_styles([{"selector": "", "props": [("border", "1px solid grey")]},
                        {"selector": "tbody td", "props": [("border", "1px solid grey")]},
                        {"selector": "th", "props": [("border", "1px solid grey")]}
                        ])
    #test = pd.concat([
    #    d.append(d.sum().rename((k, 'Total')))
    #    for k, d in pivot_to_return.groupby(level=len(columns_options)-2)
    #]).append(pivot_to_return.sum().rename(('Grand', 'Total')))
    return t, plt



