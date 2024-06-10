import pandas as pd


def filter_data(data, gr1, gr2, gr3) -> pd.DataFrame:
    """funkcja filtruje przekazane dane o wybrane przez użytkwonika parametry"""
    if len(gr1) > 0:
        data = data.loc[data['grupa_akcji_1'].isin(gr1)]
    if len(gr2) > 0:
        data = data.loc[data['grupa_akcji_2'].isin(gr2)]
    if len(gr3) > 0:
        data['grupa_akcji_3'] = data['grupa_akcji_3'].astype(str)
        data = data.loc[data['grupa_akcji_3'].isin(gr3)]
        data['grupa_akcji_3'] = data['grupa_akcji_3'].astype(int)
    return data
