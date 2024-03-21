import pandas as pd


def add_extra_filter(df, list_to_loc) -> pd.DataFrame:
    """funkcja ktrórej zadaniem jest dodatkowe odfiltorwanie danych. Do tego celu wykorzystuje listę pobraną
    z popovera"""
    if len(list_to_loc) >= 1:
        # Tworzenie warunkowej maski logicznej
        condition = None
        for i, val in enumerate(list_to_loc):
            warunek_logiczny = eval(val)
            if condition is None:
                condition = warunek_logiczny
            else:
                condition &= warunek_logiczny

            # Zastosowanie warunku do filtrowania DataFrame
        data_to_return = df.loc[condition]
    else:
        data_to_return = df

    return data_to_return


def change_type_of_columns(df, list_of_index) -> pd.DataFrame:
    """funkcja sprawdza czy dana kolumna ktora ma byc w index pivot table, jest typu str, a jesli nie to
    zamienia ja na taki wlasnie typ. Zamiana na str jest konieczna, poniewaz wymaga tego bibiloteka bokeh"""
    for i in list_of_index:
        if df[i].dtype != 'object':
            if df[i].dtype == 'float64':
                df[i].fillna(-999.0, inplace=True)
                df[i] = df[i].astype(int)
                df[i] = df[i].astype(str)
                df[i] = df[i].replace('-999', 'brak danych')
            else:
                df[i] = df[i].astype(str)


    return df
