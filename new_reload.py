from dotenv import dotenv_values

from database.source_db import deaful_set
from pages.main_diractor.dowload_data_main_db import generate_data_main_db
from pages.main_diractor.dowload_data_main_ma import generate_data_main_ma

sorce_main = dotenv_values('.env')
sorce_main = list(sorce_main.values())[0]
refresh_data = True
mail, con, engine = deaful_set(sorce_main)
print('rozpoczynam przeładowanie danych')

# Dane do zakładki 1_main
generate_data_main_ma(con, engine)
generate_data_main_db(con, engine)

a =5
