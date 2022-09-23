import pandas as pd

def data_for_sum_of_amount_in_days(mailing, years, days_from, days_to, con, type):
    sql = '''select grupa_akcji_3, grupa_akcji_2, sum(kwota) as suma_wplat,count(kwota) as liczba_wplat, 
    days.dzien_po_mailingu 
    from public.t_transakcje tr
    left outer join t_aktywnosci_korespondentow tak
    on tak.id_transakcji = tr.id_transakcji
    left outer join t_akcje ta 
    on ta.id_akcji = tak.id_akcji
    left outer join raporty.t_dni_po_nadaniu_mailingow days
    on days.id_grupy_akcji_3 = ta.id_grupy_akcji_3 and days.id_grupy_akcji_2 = ta.id_grupy_akcji_2
    and tr.data_wplywu_srodkow = days.data_wplywu_srodkow
    left outer join t_grupy_akcji_2 gr2 on gr2.id_grupy_akcji_2 = ta.id_grupy_akcji_2
    left outer join t_grupy_akcji_3 gr3 on gr3.id_grupy_akcji_3 = ta.id_grupy_akcji_3
    group by grupa_akcji_3, grupa_akcji_2, dzien_po_mailingu'''
    data = pd.read_sql_query(sql, con)
    data_to_show = data.loc[(data['dzien_po_mailingu'] >= days_from) & (data['dzien_po_mailingu'] <= days_to)]
    data_to_show = data_to_show[data_to_show['grupa_akcji_2'].isin(mailing)]
    data_to_show = data_to_show[data_to_show['grupa_akcji_3'].isin(years)]
    if type =='sum':
        values = 'suma_wplat'
    elif type == 'count':
        values = 'liczba_wplat'
    pivot_table = pd.pivot_table(data_to_show, index='dzien_po_mailingu', values=values, columns=['grupa_akcji_3',
                                                                                                        'grupa_akcji_2'],
                                 aggfunc='sum')
    pivot_table.fillna(0, inplace=True)
    pivot_table = pivot_table.cumsum()
    return pivot_table
