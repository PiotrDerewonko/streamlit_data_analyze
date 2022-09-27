#from main import con, refresh_data
from database.down_data_cr_distansce import down_data_about_cor, down_data_about_pay

def distance_between_first_and_second_pay(con, engine, refresh_data):
    data_corr = down_data_about_cor(con, engine, refresh_data)
    data_pay = down_data_about_pay(con, engine, refresh_data)
    print('test')