from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.ma_details_files.data_about_people_and_campaign_pay import download_data_about_people

sorce_main = dotenv_values('.env')
sorce_main = list(sorce_main.values())[0]
refresh_data = 'True'
mail, con, engine = deaful_set(sorce_main)
from pages.ma_details_files.download_data_fo_char_line import down_data_sum_and_count
down_data_sum_and_count(con, refresh_data, engine)
download_data_about_people(con, refresh_data, 0, [])
