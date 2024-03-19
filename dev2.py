from datetime import datetime

import pandas as pd
from pymongo import MongoClient

add = False

# Przykładowy DataFrame
t1 = datetime.now()
df = pd.read_csv('./pages/ma_details_files/tmp_file/people_camp.csv')
t2 = datetime.now()
# Utwórz połączenie z bazą danych MongoDB
client = MongoClient(host='localhost', port=27017)
print(f'odczyt csv {t2 - t1} ')
db = client.moja_baza_danych
collection = db.moja_kolekcja

if add:
    # Konwertuj DataFrame do listy słowników (dokumentów MongoDB)
    documents = df.to_dict(orient='records')

    # Zapisz dokumenty do kolekcji MongoDB
    collection.insert_many(documents)

t3 = datetime.now()
df = pd.DataFrame(list(collection.find()))
t4 = datetime.now()
print(f'odczyt csv {t2 - t1} odczyt mongo {t4 - t3}')
