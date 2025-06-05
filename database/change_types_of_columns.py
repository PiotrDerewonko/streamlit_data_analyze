import pandas as pd
def change_types_of_columns(data) -> pd.DataFrame:
    """Funkcja zmienia typy kolumn w celu uniknięcia problemów przy imporcie do bazy danych."""
    for i in data.columns:
        if (data[i].dtype == float) or (data[i].dtype == int):
            data[i] = data[i].fillna(0)
            print(f'zmieniono kolumnę {i}')
        if data[i].dtype == object:
            data[i] = data[i].astype(str)
            print(f'zmieniono kolumnę {i}')
    return data