import pandas as pd

from database.read_file_sql import read_file_sql


def download_data_ma_main(con, refresh, engine) -> pd.DataFrame:
    """Metoda generuje dane potrzebne do raportu z mailingów adresowych w zakładce main."""
    if refresh == 'True':

        #pobieram wpłaty z mailingów adresowych
        sql_ma_amount = read_file_sql('sql_queries/main/ma_campaign.sql')
        data_ma_amount = pd.read_sql(sql_ma_amount, con=con)

        #pobieram koszt
        sql_ma_cost = read_file_sql('sql_queries/main/cost_campaign.sql')
        data_ma_cost = pd.read_sql(sql_ma_cost, con=con)

        # łączę ramki danych
        data_to_insert = data_ma_amount.merge(data_ma_cost, how='left', on='kod_akcji')

        # zapisuje dane w bazie danych
        data_to_insert.to_sql('dash_ma_data', engine, if_exists='replace', schema='raporty', index=False)
        print('dodano do bazy danych dane dla dashboard adresowy')

        data_to_return = data_to_insert

    else:
        sql = f'''select * from raporty.dash_ma_data'''
        data_to_return = pd.read_sql_query(sql, con)
        data_to_return['grupa_akcji_3'] = data_to_return['grupa_akcji_3'].astype(int)

    return data_to_return
