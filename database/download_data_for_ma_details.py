import pandas as pd


def data_for_sum_of_amount_in_days(mailing, years, days_from, days_to, type, data, cumulative, new_old, choose):
    if type =='sum' or type =='count':
        if days_from > 1:
            data_to_show_not_show = data.loc[(data['dzien_po_mailingu'] <= days_from)]
            data_to_show = data.loc[(data['dzien_po_mailingu'] >= days_from+1) & (data['dzien_po_mailingu'] <= days_to)]
        else:
            data_to_show = data.loc[(data['dzien_po_mailingu'] >= days_from) & (data['dzien_po_mailingu'] <= days_to)]
    else:
        data_to_show = data
    columns_for_pivot_table = []
    if len(mailing) >= 1:
        data_to_show = data_to_show[data_to_show['grupa_akcji_2'].isin(mailing)]
        if days_from > 1:
            data_to_show_not_show = data_to_show_not_show[data_to_show_not_show['grupa_akcji_2'].isin(mailing)]
        columns_for_pivot_table.append('grupa_akcji_2')
    if len(years) >= 1:
        data_to_show = data_to_show[data_to_show['grupa_akcji_3'].isin(years)]
        if days_from > 1:
            data_to_show_not_show = data_to_show_not_show[data_to_show_not_show['grupa_akcji_3'].isin(years)]
        columns_for_pivot_table.append('grupa_akcji_3')
    if new_old:
        data_to_show = data_to_show[data_to_show['nowy_stary'].isin(choose)]
        if days_from > 1:
            data_to_show_not_show = data_to_show_not_show[data_to_show_not_show['nowy_stary'].isin(choose)]
        columns_for_pivot_table.append('nowy_stary')

    if type =='sum':
        values = 'suma_wplat'
    elif type == 'count':
        values = 'liczba_wplat'
    elif type == 'cost':
        values = 'koszt'
    elif type == 'circ':
        values = 'naklad'
    pivot_table = pd.pivot_table(data_to_show, index='dzien_po_mailingu', values=values,
                                 columns=columns_for_pivot_table, aggfunc='sum')
    if days_from > 1:
        pivot_table_sec = pd.pivot_table(data_to_show_not_show, index='dzien_po_mailingu', values=values,
                                     columns=columns_for_pivot_table, aggfunc='sum')
        pivot_table_sec = pivot_table_sec.cumsum()
        tmp = pivot_table_sec.loc[pivot_table_sec.index == days_from]
        if (type == 'sum') | (type == 'count'):
            pivot_table = pd.concat([tmp, pivot_table])

    pivot_table.fillna(0, inplace=True)
    if cumulative == True:
        pivot_table = pivot_table.cumsum()
    return pivot_table
