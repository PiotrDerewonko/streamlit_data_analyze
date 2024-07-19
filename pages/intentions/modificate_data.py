import pandas as pd


def modificate_data(data_intention, data_about_people) -> pd.DataFrame:
    data_to_return = pd.merge(data_intention, data_about_people, left_on='correspondent_id',
                              right_on='id_korespondenta',
                              how='left')
    # data_to_return['stary_nowy'] = ''
    # data_to_return['stary_nowy'].loc[data_to_return['data_dodania'] <= data_to_return['data_mailingu']] = 'stary'
    # data_to_return['stary_nowy'].loc[data_to_return['data_dodania'] == ''] = 'nowy'
    return data_to_return


def options_to_choose():
    # options = ['grupa_akcji_1_mailingu', 'grupa_akcji_2_mailingu', 'grupa_akcji_3_mailingu', 'typ_intencji',
    #            'stary_nowy', 'grupa_akcji_1_dodania', 'grupa_akcji_2_dodania', 'grupa_akcji_3_dodania'
    #            ]
    options = ['grupa_akcji_1', 'grupa_akcji_2', 'grupa_akcji_3', 'typ_intencji',
               'stary_nowy', 'grupa_akcji_1_dodania', 'grupa_akcji_2_dodania', 'grupa_akcji_3_dodania', 'patron',
               'rok_dodania'
               ]
    return options


def create_df_with_options(data) -> pd.DataFrame:
    columns_names = data.columns
    df_to_return = pd.DataFrame()
    for i in columns_names:
        temp_df = pd.DataFrame(data={'Nazwa parametru': [i],
                                     'oś': ['Oś główna'],
                                     'Opcje': ['Wykres Słupkowy', ]
                                     }, index=[0])
        df_to_return = pd.concat([df_to_return, temp_df], ignore_index=True)
    return df_to_return


def change_int_to_str_columns(data, choose_columns) -> pd.DataFrame:
    for i in choose_columns:
        if (data[i].dtype == float) | (data[i].dtype == int):
            data[i] = data[i].fillna(0)
            data[i] = data[i].astype('int')
            data[i] = data[i].astype('str')
    return data
