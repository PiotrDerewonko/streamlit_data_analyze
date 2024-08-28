from dotenv import dotenv_values

from database.dowload_data import download_dash_address_data, download_increase_data
from database.source_db import deaful_set
from pages.about_db.data import download_data
from pages.charakterystyka_bazy.download_data import download_data_about_age
from pages.custom_reports_files.distance_between_first_and_second_pay.distance import \
    distance_between_first_and_second_pay
from pages.cycle_of_life.download_data import download_data_cycle_of_life
from pages.db_analyze.get_data_to_db_analyze import live_people_from_db, weeks_of_db
from pages.intentions.download_data_intention import download_data_intention_count, download_data_intention_money
from pages.ma_details_files.add_prefix import add_prefix
from pages.ma_details_files.addpromisegift import promise_gift
from pages.ma_details_files.charts_in_days.download_data_for_days_charts import download_data_for_days_charts
from pages.ma_details_files.cost_structure import get_costs
from pages.ma_details_files.data_about_people_and_campaign_pay import download_data_about_people_camp, distinct_options, \
    download_data_about_people_camp_pay, download_data_about_people, data_pay_all
from pages.ma_details_files.download_data_fo_char_line import down_data_sum_and_count, down_data_cost_and_circulation
from pages.ma_details_files.max_day import check_max_day

sorce_main = dotenv_values('.env')
sorce_main = list(sorce_main.values())[0]
refresh_data = 'True'
mail, con, engine = deaful_set(sorce_main)
print('rozpoczynam przeladowanie danych')

download_dash_address_data(con, refresh_data, engine, 'address')
download_dash_address_data(con, refresh_data, engine, 'non address')
down_data_cost_and_circulation(con, refresh_data, engine)
down_data_sum_and_count(con, refresh_data, engine)
download_data_for_days_charts(con, engine, refresh_data, 'dash_char_ma_data_by_id',
                              '10_chart_in_days/count_and_sum_amount_for_char_days')
download_data_for_days_charts(con, engine, refresh_data,
                              'dash_char_ma_data_cost_cir_by_id',
                              '10_chart_in_days/cost_and_cirtulation_for_char_days')
download_increase_data(con, refresh_data, engine)
distance_between_first_and_second_pay(con, engine, refresh_data)
download_data_about_people_camp(con, refresh_data, engine)
download_data_about_people(con, refresh_data, 0, [])
download_data_about_people_camp_pay(con, refresh_data, engine)
data_pay_all(con, refresh_data)
check_max_day(refresh_data)
add_prefix(con, refresh_data, engine)
promise_gift()
distinct_options(refresh_data)
live_people_from_db(con, refresh_data)
weeks_of_db(con, refresh_data, engine)
get_costs(con, refresh_data, engine)
download_data(con, refresh_data)
download_data_cycle_of_life(con, refresh_data)
download_data_about_age(con, refresh_data, engine)
download_data_intention_money(con, refresh_data)
download_data_intention_count(con, refresh_data)

print('zakonczono przeladowanie danych')
