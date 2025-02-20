import pandas as pd

from database.source_db import mongo_connect

db = mongo_connect()
collectionv2 = db['data_flow']
collectionv2.delete_many({})

collection = db['people']
data_all = pd.read_csv('pages/ma_details_files/tmp_file/people.csv', index_col='Unnamed: 0',
                                   low_memory=False)
collection.insert_many(data_all.to_dict('records'))
