import pandas as pd

def filtr_mailing(data, filtr):
    data = data[data['grupa_akcji_2'].isin(filtr)]

