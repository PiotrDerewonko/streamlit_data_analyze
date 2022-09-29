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
            print('test')
            tmp_sum = pivot[f'''{row['Nazwa parametru']}'''].max()
            if tmp_sum > max:
                max = tmp_sum
    return max

def change_short_names_ma(data):
    data = data.replace({'sw': 'suma_wplat', 'lw': 'liczba_wplat', 'nc': 'naklad_calkowity',
                         'kc': 'koszt_calkowity', 'roi': 'ROI', 'szlw': 'Stopa zwrotu l.w.'})
    data = data.drop(columns =['index_x', 'Wartosc parametru', 'index_y', 'Parametr oś', 'index', 'Wspolczynnik'])
    return data

def change_short_names_db(data):
    data = data.replace({'sw_db': 'suma_wplat', 'lw_db': 'liczba_wplat', 'nc_db': 'naklad_calkowity',
                         'kc_db': 'koszt_calkowity', 'roi_db': 'ROI', 'szlw_db': 'Stopa zwrotu l.w.',
                         'szp_db': 'Stopa pozyskania'})
    data = data.drop(columns =['index_x', 'Wartosc parametru', 'index_y', 'Parametr oś', 'index', 'Wspolczynnik'])
    return data

def modifcate_data(data, type, multindex):
    if type != 'increase':
        'zmieniam typ kolumny z rokiem na tekst w przeciwnym wypdaku przestaje dzialac'
        data['grupa_akcji_3'] = data['grupa_akcji_3'].astype(str)
        gr3 = data['grupa_akcji_3'].drop_duplicates().to_list()
    else:
        data.sort_values(multindex, inplace=True)
        data['miesiac_dodania'] = data['miesiac_dodania'].astype(int)
        data['miesiac_dodania'] = data['miesiac_dodania'].astype(str)
        for tmp_a in range(1, 10):
           data['miesiac_dodania'].loc[data['miesiac_dodania'] == f"{tmp_a}"] = f"0{tmp_a}"
        data['miesiac_dodania'] = data['miesiac_dodania'].astype(str)
        data['grupa_akcji_1'] = data['grupa_akcji_1'].astype(str)
        data['grupa_akcji_2'] = data['grupa_akcji_2'].astype(str)
        data['rok_dodania'] = data['rok_dodania'].astype(int)
        data['rok_dodania'] = data['rok_dodania'].astype(str)
        data['kod_akcji'] = data['kod_akcji'].astype(str)
        gr3 = data['rok_dodania'].drop_duplicates().to_list()
    if type =='nonaddress':
        data['miesiac'] = data['miesiac'].astype(str)
    if (type =='dist') | (type =='dist2'):
        gr3 = data['date_part'].drop_duplicates().to_list()
    gr3.sort()


    'pobieram zakres lat'
    from_ = gr3[0]
    to_ = gr3[-1]

    return data, gr3, from_, to_

def create_pivot_table(data, multindex, type):
    if type == 'increase':
        pivot_table_ma = pd.pivot_table(data, index=multindex, values='ilosc', columns='grupa_akcji_1', aggfunc='sum')
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
        if type == 'nonaddress':
            pivot_table_ma['Stopa pozyskania'] = (pivot_table_ma['pozyskano']/pivot_table_ma['naklad_calkowity'])*100
        elif type == 'address':
            pivot_table_ma.drop(columns='pozyskano', inplace=True)
        pivot_table_ma.replace([np.inf, -np.inf], np.nan, inplace=True)
        pivot_table_ma.fillna(0, inplace=True)

    return pivot_table_ma

def label_of_axis(data):
    label_axis_prime = ''
    label_axis_second = ''
    for i, row2 in data.iterrows():
        if row2['oś'] == 'Oś główna':
            if len(label_axis_prime) == 0:
                label_axis_prime = row2[0]
            else:
                label_axis_prime = label_axis_prime + '/' + str(row2['Nazwa parametru'])
        else:
            if len(label_axis_second) == 0:
                label_axis_second = row2[0]
            else:
                label_axis_second = label_axis_second + '/' + str(row2['Nazwa parametru'])
    return label_axis_prime, label_axis_second
