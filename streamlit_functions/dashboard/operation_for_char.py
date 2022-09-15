import pandas as pd
def create_df(data):
    if len(data) > 1:
        tmp = pd.DataFrame(data.items(), columns=['Wspolczynnik', 'Opcje'])
        position_of_parameter = [0, 3, 6, 9, 12, 15]
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

def check_max_value(pivot, data):
    print('test')

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
        data['rok_dodania'] = data['rok_dodania'].astype(int)
        data['rok_dodania'] = data['rok_dodania'].astype(str)
        gr3 = data['rok_dodania'].drop_duplicates().to_list()
    gr3.sort()

    'pobieram zakres lat'
    from_ = gr3[0]
    to_ = gr3[-1]

    return data, gr3, from_, to_