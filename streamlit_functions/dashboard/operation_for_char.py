import numpy as np
import pandas as pd


def create_df(data):
    if len(data) > 1:
        tmp = pd.DataFrame(data.items(), columns=['Wspolczynnik', 'Opcje'])
        # todo dorobic tutaj aby sam tworzyl ta liste parametrow na podswteier dlugosci
        position_of_parameter = []
        numbers_of_obcjects = len(data)/3
        j = 0
        for i in range(0, int(numbers_of_obcjects)):
            position_of_parameter.append(j)
            j += 3
        position_of_axis = [x+1 for x in position_of_parameter]
        position_of_char = [x+2 for x in position_of_parameter]
        parameters = tmp.iloc[position_of_parameter].reset_index()
        parameters = parameters.rename(columns={'Wspolczynnik': 'Nazwa parametru', 'Opcje': 'Wartosc parametru'})
        axis = tmp.iloc[position_of_axis].reset_index()
        axis = axis.rename(columns={'Wspolczynnik': 'Parametr oś', 'Opcje': 'oś'})
        char = tmp.iloc[position_of_char].reset_index()
        tmp_all = pd.merge(parameters, axis, left_index=True, right_index=True)
        tmp_all = pd.merge(tmp_all, char, left_index=True, right_index=True)
        return tmp_all.loc[tmp_all['Wartosc parametru'] == True]

def check_max_value(pivot, data, axis):
    max = 0
    tmp = data.loc[data['oś'] == axis]
    if len(tmp) >= 1:
        for i, row in tmp.iterrows():
            tmp_sum = pivot[row['Nazwa parametru']].max()
            if tmp_sum > max:
                max = tmp_sum
        tmp_2 = tmp.loc[tmp['Opcje'] == 'Wykres Słupkowy Skumulowany']
        if len(tmp_2) >= 1:
            max_for_stock = 0
            pivot_tmp = pivot[tmp_2['Nazwa parametru']]
            i_int = 0
            for j, row2 in pivot_tmp.iterrows():
                tmp_sum_2 = pivot_tmp.iloc[i_int].sum()
                i_int += 1
                if tmp_sum_2 > max_for_stock:
                    max_for_stock = tmp_sum_2
            if max_for_stock > max:
                max = max_for_stock
    return max

def change_short_names_ma(data):
    data = data.replace({'sw': 'suma_wplat', 'lw': 'liczba_wplat', 'nc': 'naklad_calkowity',
                         'kc': 'koszt_calkowity', 'roi': 'ROI', 'szlw': 'Stopa zwrotu l.w.',
                        })
    data = data.drop(columns =['index_x', 'Wartosc parametru', 'index_y', 'Parametr oś', 'index', 'Wspolczynnik'])
    return data

def change_short_names_db(data):
    data = data.replace({'sw_db': 'suma_wplat', 'lw_db': 'liczba_wplat', 'nc_db': 'naklad_calkowity',
                         'kc_db': 'koszt_insertowania', 'roi_db': 'ROI', 'szlw_db': 'Stopa zwrotu l.w.',
                         'szp_db': 'Stopa pozyskania',  'swt_db': 'laczna_suma_wplat_nowych',
                         'kct_db': 'laczny_koszt_utrzymania', 'poz_db': 'pozyskano', 'kcin_db': 'koszt_insertu_dla_nowych',
                         'un_db': 'udzial_nowych', 'swn_db': 'suma_wplat_nowi', 'udzial_aktywnych_nowych_db': '%pozyskanych_w_ost_mailingu'})
    data = data.drop(columns =['index_x', 'Wartosc parametru', 'index_y', 'Parametr oś', 'index', 'Wspolczynnik'])
    return data

def modifcate_data(data, type, multindex, title):
    for i in multindex:
        data[f'{i}'] = data[f'{i}'].astype(str)

    if 'grupa_akcji_3' in multindex:
        years = data['grupa_akcji_3'].drop_duplicates().to_list()
        years.sort()
        'pobieram zakres lat'
        from_ = years[0]
        to_ = years[-1]
    elif 'grupa_akcji_3_wysylki' in multindex:
        years = data['grupa_akcji_3_wysylki'].drop_duplicates().to_list()
        years.sort()
        'pobieram zakres lat'
        from_ = years[0]
        to_ = years[-1]
    else:
        from_ = '0'
        to_ = '0'
        years = []
    if 'grupa_akcji_2' in multindex:
        list_mailings = data['grupa_akcji_2'].drop_duplicates().to_list()
        list_mailings.sort()
    elif 'grupa_akcji_2_wysylki' in multindex:
        list_mailings = data['grupa_akcji_2_wysylki'].drop_duplicates().to_list()
        list_mailings.sort()
    else:
        list_mailings = []
    title_fin = title
    if len(list_mailings) >= 1:
        title_fin = title_fin + f" dla mailingów {list_mailings}"
    if len(years) >= 1:
        title_fin = title_fin + f" za lata {years}"
    return data,  title_fin

def create_pivot_table(data, multindex, type, columns_label):
    if type == 'increase':
        for i in range(1, 10):
            data['miesiac_dodania'].loc[data['miesiac_dodania']==f'{i}'] = f'0{i}'
        for j in columns_label:
            data[j] = data[j].astype(str)
        pivot_table_ma = pd.pivot_table(data, columns=columns_label, values='ilosc', index=multindex, aggfunc='sum')
        if len(columns_label)>1:
            def join_levels(levels):
                return '_'.join(levels)
            pivot_table_ma.columns = pivot_table_ma.columns.map(join_levels)
        pivot_table_ma.fillna(0, inplace=True)
    elif type == 'dist':
        pivot_table_ma = pd.pivot_table(data, index=multindex, values='id_korespondenta', columns='status_second_pay',
                                        aggfunc='count')
        pivot_table_ma.fillna(0, inplace=True)
    elif type == 'dist2':
        pivot_table_ma = pd.pivot_table(data, index=multindex, values='id_korespondenta', columns='status_second_pay',
                                        aggfunc='count')
        pivot_table_ma.fillna(0, inplace=True)
        pivot_table_ma['sum'] = 0
        for i in pivot_table_ma.columns:
            if i != 'sum':
                pivot_table_ma['sum'] = pivot_table_ma['sum'] + pivot_table_ma[i]
        tmp_df = pivot_table_ma.copy()
        for j in pivot_table_ma.columns:
            if j != 'sum':
                tmp_df[j] = tmp_df['sum']
        tmp2 = pivot_table_ma.div(tmp_df)
        tmp2.drop(columns=['sum'], inplace=True)
        pivot_table_ma = tmp2

    else:
        pivot_table_ma = pd.pivot_table(data, index=multindex, values=['suma_wplat', 'koszt_calkowity', 'liczba_wplat',
                                                                   'naklad_calkowity', 'pozyskano'], aggfunc='sum')

        pivot_table_ma['ROI'] = pivot_table_ma['suma_wplat']/pivot_table_ma['koszt_calkowity']
        pivot_table_ma['Stopa zwrotu l.w.'] = (pivot_table_ma['liczba_wplat']/pivot_table_ma['naklad_calkowity'])*100
        pivot_table_ma['Koszt na głowę'] = pivot_table_ma['koszt_calkowity']/pivot_table_ma['naklad_calkowity']
        pivot_table_ma['Średnia wpłata'] = pivot_table_ma['suma_wplat']/pivot_table_ma['liczba_wplat']
        if type == 'nonaddress':
            pivot_table_ma['Stopa pozyskania'] = (pivot_table_ma['pozyskano']/pivot_table_ma['naklad_calkowity'])*100
            pivot_table_ma_extra = pd.pivot_table(data, index=multindex,
                                            values=['laczna_suma_wplat', 'laczny_koszt_utrzymania', 'suma_wplat_nowi',
                                                    'liczba_wplat_nowi', 'obecnie_aktywnych'], aggfunc='sum')
            pivot_table_ma = pd.merge(pivot_table_ma, pivot_table_ma_extra, how='left', left_index=True, right_index=True)
            pivot_table_ma['udzial_nowych'] = pivot_table_ma['suma_wplat_nowi'] / pivot_table_ma['suma_wplat']
            pivot_table_ma['pozyskano'] = pivot_table_ma['pozyskano'] + 1
            pivot_table_ma['%pozyskanych_w_ost_mailingu'] = pivot_table_ma['obecnie_aktywnych'] / pivot_table_ma['pozyskano']
            pivot_table_ma['pozyskano'] = pivot_table_ma['pozyskano'] - 1
            pivot_table_ma['koszt_insertu_dla_nowych'] = pivot_table_ma['udzial_nowych'] * pivot_table_ma['koszt_calkowity']
            pivot_table_ma['koszt_insertu_dla_starych'] = pivot_table_ma['koszt_calkowity'] - pivot_table_ma['koszt_insertu_dla_nowych']
            pivot_table_ma.rename(columns={'koszt_calkowity': 'koszt_insertowania', 'laczna_suma_wplat':
                                           'laczna_suma_wplat_nowych'}, inplace=True)
        elif type == 'address':
            pivot_table_ma.drop(columns='pozyskano', inplace=True)
        if type == 'address':
            pivot_table_ma['index_liczba_wplat'] = 0
            pivot_table_ma['index_suma_wplat'] = 0
            for i in range(1, len(pivot_table_ma.index)):
                pivot_table_ma['index_liczba_wplat'].iloc[i] = \
                    (pivot_table_ma['liczba_wplat'].iloc[i] / pivot_table_ma['liczba_wplat'].iloc[i-1]) * 100
                pivot_table_ma['index_suma_wplat'].iloc[i] = \
                    (pivot_table_ma['suma_wplat'].iloc[i] / pivot_table_ma['suma_wplat'].iloc[i-1]) * 100
        pivot_table_ma.replace([np.inf, -np.inf], np.nan, inplace=True)
        pivot_table_ma.fillna(0, inplace=True)

    return pivot_table_ma

def label_of_axis(data):
    label_axis_prime = ''
    label_axis_second = ''
    for i, row2 in data.iterrows():
        if row2['oś'] == 'Oś główna':
            if len(label_axis_prime) == 0:
                label_axis_prime = str(row2[0])
            else:
                label_axis_prime = label_axis_prime + '/' + str(row2['Nazwa parametru'])
        else:
            if len(label_axis_second) == 0:
                label_axis_second = row2[0]
            else:
                label_axis_second = label_axis_second + '/' + str(row2['Nazwa parametru'])
    return label_axis_prime, label_axis_second
