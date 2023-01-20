from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.ma_details_files.add_prefix import add_prefix
from pages.ma_details_files.data_about_people_and_campaign_pay import download_data_about_people_camp, distinct_options, \
    download_data_about_people_camp_pay

sorce_main = dotenv_values('.env')
sorce_main = list(sorce_main.values())[0]
refresh_data = 'True'
mail, con, engine = deaful_set(sorce_main)
print('rozpoczynam przeladowanie danych')
#download_dash_address_data(con, refresh_data, engine, 'address')
#download_dash_address_data(con, refresh_data, engine, 'non address')
#down_data_cost_and_circulation(con, refresh_data, engine)
#download_increase_data(con, refresh_data, engine)
#distance_between_first_and_second_pay(con, engine, refresh_data)
#down_data_sum_and_count(con, refresh_data, engine)
#download_data_about_people(con, refresh_data, 0, [])
download_data_about_people_camp_pay(con, refresh_data, engine)
download_data_about_people_camp(con, refresh_data, engine)
add_prefix(con, refresh_data, engine)
distinct_options(refresh_data)

print('zakonczono przeladowanie danych')