import pandas as pd


def make_pivot_percent_of_people(data) -> pd.DataFrame:
    data_tmp1 = data.loc[data['aktualny_numer_roku'] == '1']
    pivot_tmp1 = pd.pivot_table(data_tmp1, index=['rok_dodania'], aggfunc='count', values='id_korespondenta')
    max_year_number = data['aktualny_rok'].max()
    data_tmp2 = data.loc[(data['aktualny_rok'] == max_year_number) & (data['udzial'] == 'brał_udział')]
    pivot_tmp2 = pd.pivot_table(data_tmp2, index=['rok_dodania'], aggfunc='count', values='id_korespondenta')
    final_pivot = pd.merge(left=pivot_tmp1, right=pivot_tmp2, left_index=True, right_index=True)
    columns_name = final_pivot.columns.to_list()
    final_pivot['procent_pozostałych'] = 0
    final_pivot['procent_pozostałych'] = final_pivot[columns_name[1]] / final_pivot[columns_name[0]]
    final_pivot.drop(columns=columns_name, inplace=True)

    return final_pivot