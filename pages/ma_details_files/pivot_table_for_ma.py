import pandas as pd

from database.source_db import deaful_set
from functions_pandas.pivot_table import pivot_table_w_subtotals
from pages.ma_details_files.data_about_people_and_campaign_pay import download_data_about_people, \
    download_data_about_people_camp_pay, download_data_about_people_camp


def create_pivot_table(con, refresh_data, engine, camp, year, columns_options):
    sorce_main = 'lwowska'
    refresh_data = 'False'
    year_int = []
    for i in year:
        year_int.append(int(i))
    mail, con, engine = deaful_set(sorce_main)
    data_about_people = download_data_about_people(con, refresh_data, engine)
    data_about_pay = download_data_about_people_camp_pay(con, refresh_data, engine)
    data_about_camp = download_data_about_people_camp(con, refresh_data, engine)
    data_about_camp = data_about_camp[data_about_camp['grupa_akcji_2_wysylki'].isin(camp)]
    data_about_camp = data_about_camp[data_about_camp['grupa_akcji_3_wysylki'].isin(year_int)]
    data_all = pd.merge(data_about_camp, data_about_pay, left_on=['id_korespondenta', 'kod_akcji_wysylki'],
                        right_on=['id_korespondenta', 'kod_akcji_wplaty'], how='left')
    data_all = pd.merge(data_all, data_about_people, on='id_korespondenta', how='left')
    pivot_to_return = pivot_table_w_subtotals(data_all,['suma_wplat', 'liczba_wplat', 'koszt'],columns_options, aggfunc='sum',columns= [],
                                              fill_value=0)
    pivot_to_return['średnia'] = pivot_to_return['suma_wplat']/pivot_to_return['liczba_wplat']
    pivot_to_return['ROI'] = pivot_to_return['suma_wplat']/pivot_to_return['koszt']
    #pivot_to_return['średnia'] = pivot_to_return['suma_wplat']/pivot_to_return['liczba_wplat']
    return pivot_to_return



