import pandas as pd


def filter_data(data, gr1, gr2, gr3) -> pd.DataFrame:
    """funkcja filtruje przekazane dane o wybrane przez użytkwonika parametry"""
    if len(gr1) > 0:
        data = data.loc[data['grupa_akcji_1_mailingu'].isin(gr1)]
    if len(gr2) > 0:
        data = data.loc[data['grupa_akcji_2_mailingu'].isin(gr2)]
    if len(gr3) > 0:
        data['grupa_akcji_3_mailingu'] = data['grupa_akcji_3_mailingu'].astype(int)
        data['grupa_akcji_3_mailingu'] = data['grupa_akcji_3_mailingu'].astype(str)
        data = data[data['grupa_akcji_3_mailingu'].isin(gr3)]
        data['grupa_akcji_3_mailingu'] = data['grupa_akcji_3_mailingu'].astype(int)
    return data
