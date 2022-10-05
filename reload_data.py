from pages.custom_reports_files.distance_between_first_and_second_pay.distance import distance_between_first_and_second_pay
from database.source_db import deaful_set
from pages.custom_reports_files.distance_between_first_and_second_pay.distance import \
    distance_between_first_and_second_pay
from pages.ma_details_files.download_data_fo_char_line import down_data_sum_and_count, down_data_cost_and_circulation

sorce_main = 'local'
refresh_data = 'True'
mail, con, engine = deaful_set(sorce_main)
print('rozpoczynam migracje')
download_dash_address_data(con, refresh_data, engine, 'address')
download_dash_address_data(con, refresh_data, engine, 'non address')
download_increase_data(con, refresh_data, engine)
distance_between_first_and_second_pay(con, engine, refresh_data)
down_data_sum_and_count(con, refresh_data, engine)
down_data_cost_and_circulation(con, refresh_data, engine)
print('zakonczono migracje')