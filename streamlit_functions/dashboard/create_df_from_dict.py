import pandas as pd
def create_df(data):
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
    return tmp_all