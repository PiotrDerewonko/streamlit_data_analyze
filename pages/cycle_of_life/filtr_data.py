import pandas as pd

def filtr_data_by_year_of_add(data, values) -> pd.DataFrame:
    if len(values)>=1:
        data_fin = pd.DataFrame()
        for i in values:
            tmp = data.loc[data['rok_dodania'] == i]
            data_fin = pd.concat([data_fin, tmp])
    else:
        data_fin = data

    return data_fin