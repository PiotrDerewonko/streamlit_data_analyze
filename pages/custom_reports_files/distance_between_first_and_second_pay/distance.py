#from main import con, refresh_data
from database.down_data_cr_distansce import down_data_about_cor, down_data_about_pay

def distance_between_first_and_second_pay(con, engine, refresh_data):
    data_corr = down_data_about_cor(con, engine, refresh_data)
    data_pay = down_data_about_pay(con, engine, refresh_data)
    data_corr_pay = data_corr.merge(data_pay, on='id_korespondenta')

    #sprawdzenie kiedy dokonal pierwszej wplaty i czy byla ona w momencie pozyskania
    data_corr_pay['distance_add_to_fp'] = (data_corr_pay['first_pay'] - data_corr_pay['data_dodania']).dt.days
    data_corr_pay['distance_add_to_fp'].loc[data_corr_pay['distance_add_to_fp'] < 0] = 0
    data_corr_pay['distance_add_to_fp'].fillna(99999, inplace=True)
    data_corr_pay['status_first_pay'] = ''
    data_corr_pay['status_first_pay'].loc[data_corr_pay['distance_add_to_fp'] == 0] = 'Wplata w momencie pozyskania'
    data_corr_pay['status_first_pay'].loc[data_corr_pay['distance_add_to_fp'] > 0] = 'Wplata w późniejszym terminie'
    data_corr_pay['status_first_pay'].loc[data_corr_pay['distance_add_to_fp'] == 99999] = 'Brak wpłaty'

    #sprawdzenie czy byla druga wplata i kiedy ona byla dokonana
    data_corr_pay['distance_fp_to_sp'] = (data_corr_pay['second_pay'] - data_corr_pay['first_pay']).dt.days
    data_corr_pay['distance_fp_to_sp'].fillna(99999, inplace=True)
    data_corr_pay['status_second_pay'] = ''
    compartment = [(0, 180, '1) do pół roku'), (180, 365, '2) od pół roku do roku'),
                   (365, 730, '3) miedzy 1 a drugim rokiem'),
                   (730, 99998, '4) powyżej dwóch lat')]
    for i in compartment:
        data_corr_pay['status_second_pay'].loc[(data_corr_pay['distance_fp_to_sp'] >= i[0]) &
                                           (data_corr_pay['distance_fp_to_sp'] <= i[1])] = f'{i[2]}'
    data_corr_pay['status_second_pay'].loc[data_corr_pay['status_second_pay'] == ''] = 'Brak wpłaty'
    return data_corr_pay