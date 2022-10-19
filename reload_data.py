from database.data_about_people import download_data_about_people
from database.source_db import deaful_set

sorce_main = 'lwowska'
refresh_data = 'True'
mail, con, engine = deaful_set(sorce_main)
print('rozpoczynam przeladowanie danych')
#download_dash_address_data(con, refresh_data, engine, 'address')
#download_dash_address_data(con, refresh_data, engine, 'non address')
#download_increase_data(con, refresh_data, engine)
#distance_between_first_and_second_pay(con, engine, refresh_data)
#down_data_sum_and_count(con, refresh_data, engine)
download_data_about_people(con, refresh_data, engine)
print('zakonczono przeladowanie danych')