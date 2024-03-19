from typing import Tuple, List

import pandas as pd


def generete_pivot_tables(subaction_list, data_second, is_grouped) -> Tuple[pd.DataFrame, List]:
    pivot_to_weeks_final = pd.DataFrame()
    if not is_grouped:
        index_values = ['kod_akcji', 'numer_tygodnia']
        for akcja in subaction_list:
            data_tmp = data_second.loc[data_second['kod_akcji'] == akcja]
            pivot_to_weeks = pd.pivot_table(data_tmp, index=index_values, values=
            ['suma_wplat', 'pozyskano', 'koszt_wysylki_giftu', 'koszt_insertu'], aggfunc='sum')
            pivot_to_weeks = pivot_to_weeks.cumsum()
            pivot_to_weeks_final = pd.concat([pivot_to_weeks_final, pivot_to_weeks])
    elif is_grouped:
        #todo do zastanowienia czy nie dodac tu kampani aby rozrzucniac te akcje
        index_values = ['grupa_akcji_2', 'numer_tygodnia']
        # zmienne tymczasowe, jedna do finalej tabeli przestanwej druga do odfiltorwania grup akcji 2
        data_gr2 = pd.DataFrame()
        for akcja in subaction_list:
            data_tmp = data_second['grupa_akcji_2'].loc[data_second['kod_akcji'] == akcja]
            data_gr2 = pd.concat([data_gr2, data_tmp])
        data_gr2.drop_duplicates(inplace=True)
        list_gr2 = list(data_gr2[0].drop_duplicates())
        filtered_data = data_second[
            (data_second['grupa_akcji_2'].isin(list_gr2)) & (data_second['kod_akcji'].isin(subaction_list))]

        for grupa in list_gr2:
            data_tmp = filtered_data.loc[filtered_data['grupa_akcji_2'] == grupa]
            pivot_to_weeks = pd.pivot_table(data_tmp, index=index_values, values=
            ['suma_wplat', 'pozyskano', 'koszt_wysylki_giftu', 'koszt_insertu'], aggfunc='sum')
            pivot_to_weeks = pivot_to_weeks.cumsum()
            pivot_to_weeks_final = pd.concat([pivot_to_weeks_final, pivot_to_weeks])

    else:
        index_values = ['kod_akcji', 'numer_tygodnia']

    return pivot_to_weeks_final, index_values
