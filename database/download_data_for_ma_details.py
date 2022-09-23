import pandas as pd

def data_for_sum_of_amount_in_days(mailing, years, days_from, days_to, type, data):
    data_to_show = data.loc[(data['dzien_po_mailingu'] >= days_from) & (data['dzien_po_mailingu'] <= days_to)]
    data_to_show = data_to_show[data_to_show['grupa_akcji_2'].isin(mailing)]
    data_to_show = data_to_show[data_to_show['grupa_akcji_3'].isin(years)]
    if type =='sum':
        values = 'suma_wplat'
    elif type == 'count':
        values = 'liczba_wplat'
    pivot_table = pd.pivot_table(data_to_show, index='dzien_po_mailingu', values=values,
                                 columns=['grupa_akcji_3','grupa_akcji_2'], aggfunc='sum')
    pivot_table.fillna(0, inplace=True)
    pivot_table = pivot_table.cumsum()
    return pivot_table
