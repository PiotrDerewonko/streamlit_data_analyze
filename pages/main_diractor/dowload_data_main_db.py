
from pages.main_diractor.download_data_main import DownloadDataMain

def generate_data_main_db(con, engine, test_mode=False):
    db_data = DownloadDataMain(con, engine, 'dash_db_data', test_mode=test_mode)
    data_db_amount = db_data.get_data_from_sql('sql_queries/1_main/db_campaign.sql')
    data_db_cost = db_data.get_data_from_sql('sql_queries/1_main/cost_campaign.sql')
    list_to_merge_db = [data_db_cost]
    data_db_total_cost = db_data.get_data_from_sql('sql_queries/1_main/total_cost_and_pay.sql')
    list_to_merge_db.append(data_db_total_cost)
    data_db_new_people = db_data.get_data_from_sql('sql_queries/1_main/total_new.sql')
    list_to_merge_db.append(data_db_new_people)
    data_db_new_people_pay = db_data.get_data_from_sql('sql_queries/1_main/pay_from_new.sql')
    list_to_merge_db.append(data_db_new_people_pay)
    data_db_promise_gift = db_data.get_data_from_sql('sql_queries/1_main/promise_gifts.sql')
    list_to_merge_db.append(data_db_promise_gift)
    last_mailng = db_data.get_data_from_sql_with_out_limit('sql_queries/1_main/last_mailing.sql')
    dict_to_replace = {'{default_camp}': last_mailng['grupa_akcji_2'].iloc[0],
                       '{default_year}': last_mailng['grupa_akcji_3'].iloc[0]}
    data_db_is_still_active = db_data.get_data_from_sql_with_replace('sql_queries/1_main/is_still_active.sql',
                                                                     dict_to_replace)
    list_to_merge_db.append(data_db_is_still_active)
    data_all_db = db_data.merge_data(data_db_amount, list_to_merge_db, 'kod_akcji')
    db_data.insert_data(data_all_db)

def download_data_main_db(con, engine, test_mode=False):
    db_data = DownloadDataMain(con, engine, 'dash_db_data')
    data_to_return = db_data.download_data()
    return data_to_return