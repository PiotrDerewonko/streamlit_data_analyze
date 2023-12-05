from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.cycle_of_life.download_data import download_data_cycle_of_life

sorce_main = dotenv_values('.env')
sorce_main = list(sorce_main.values())[0]
refresh_data = 'True'
mail, con, engine = deaful_set(sorce_main)
print('rozpoczynam przeladowanie danych')

# download_dash_address_data(con, refresh_data, engine, 'address')
# download_dash_address_data(con, refresh_data, engine, 'non address')
# down_data_cost_and_circulation(con, refresh_data, engine)
# download_increase_data(con, refresh_data, engine)
# distance_between_first_and_second_pay(con, engine, refresh_data)
# down_data_sum_and_count(con, refresh_data, engine)
# download_data_about_people_camp(con, refresh_data, engine)
# download_data_about_people(con, refresh_data, 0, [])
# download_data_about_people_camp_pay(con, refresh_data, engine)
# data_pay_all(con, refresh_data)
# check_max_day(refresh_data)
# add_prefix(con, refresh_data, engine)
# promise_gift()
# distinct_options(refresh_data)
# live_people_from_db(con, refresh_data)
# weeks_of_db(con, refresh_data, engine)
# get_costs(con, refresh_data, engine)
# download_data(con, refresh_data)
download_data_cycle_of_life(con, refresh_data)





print('zakonczono przeladowanie danych')