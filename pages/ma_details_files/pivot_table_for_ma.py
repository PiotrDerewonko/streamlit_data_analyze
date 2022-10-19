from database.source_db import deaful_set
from pages.ma_details_files.data_about_people_and_campaign_pay import download_data_about_people, \
    download_data_about_people_camp_pay


def create_pivot_table(con, refresh_data, engine):
    sorce_main = 'lwowska'
    refresh_data = 'True'
    mail, con, engine = deaful_set(sorce_main)
    data_about_people = download_data_about_people(con, refresh_data, engine)
    data_about_pay = download_data_about_people_camp_pay(con, refresh_data, engine)

