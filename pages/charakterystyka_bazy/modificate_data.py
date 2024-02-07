import pandas as pd

from functions_pandas.plot_cam_adr_dash import pivot_and_chart_for_dash


def to_100_percent(pivot, is_amount) -> pd.DataFrame:
    pivot.fillna(0, inplace=True)
    pivot['sum'] = 0
    if is_amount:
        sum_check = ('sum', '')
    else:
        sum_check = 'sum'
    for i in pivot.columns:
        if i != sum_check:
            pivot['sum'] = pivot['sum'] + pivot[i]
    tmp_df = pivot.copy()
    for j in pivot.columns:
        if j != sum_check:
            tmp_df[j] = tmp_df['sum']
    tmp2 = pivot.div(tmp_df)
    tmp2.drop(columns=['sum'], inplace=True)
    pivot = tmp2

    return pivot

def download_char(pivot, data, multindex, tytul):
    char_options_df_weeks = pd.DataFrame(columns=['Nazwa parametru', 'oś', 'Opcje'])
    for i in range(0, len(pivot.columns)):
        test = pivot.columns[i]
        tmp = pd.DataFrame(data={'Nazwa parametru': pivot.columns[i], 'oś': 'Oś główna', 'Opcje': 'Wykres Słupkowy Skumulowany'}, index=[i])
        char_options_df_weeks = pd.concat([char_options_df_weeks, tmp])
    dict_of_oriantation = {'major': 'vertical', 'group': 'vertical', 'sub_group': 'vertical'}
    char, table = pivot_and_chart_for_dash(data, multindex, 'me_detail', 'test tytulu',
                                          'Rok', {}, pivot, char_options_df_weeks, tytul,
                                               dict_of_oriantation
                                          )
    return char
