from dotenv import dotenv_values

from database.dowload_data import download_dash_address_data, download_increase_data
from database.source_db import deaful_set
from pages.custom_reports_files.distance_between_first_and_second_pay.distance import \
    distance_between_first_and_second_pay
from pages.ma_details_files.add_prefix import add_prefix
from pages.ma_details_files.data_about_people_and_campaign_pay import download_data_about_people_camp, distinct_options, \
    download_data_about_people_camp_pay, download_data_about_people
from pages.ma_details_files.download_data_fo_char_line import down_data_sum_and_count, down_data_cost_and_circulation

sorce_main = dotenv_values('.env')
sorce_main = list(sorce_main.values())[0]
refresh_data = 'True'
mail, con, engine = deaful_set(sorce_main)
print('rozpoczynam przeladowanie danych')
download_dash_address_data(con, refresh_data, engine, 'address')
download_dash_address_data(con, refresh_data, engine, 'non address')
down_data_cost_and_circulation(con, refresh_data, engine)
download_increase_data(con, refresh_data, engine)
distance_between_first_and_second_pay(con, engine, refresh_data)
down_data_sum_and_count(con, refresh_data, engine)
download_data_about_people(con, refresh_data, 0, [])
download_data_about_people_camp_pay(con, refresh_data, engine)
download_data_about_people_camp(con, refresh_data, engine)
add_prefix(con, refresh_data, engine)
distinct_options(refresh_data)

print('zakonczono przeladowanie danych')