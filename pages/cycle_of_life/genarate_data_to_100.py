import pandas as pd


def generate_data_to_100(pivot) -> pd.DataFrame:
    list_of_columns = pivot.columns
    pivot_cum = pivot.copy()
    pivot_cum.fillna(0, inplace=True)
    pivot_cum['sum'] = 0
    for j in list_of_columns:
        pivot_cum['sum'] = pivot_cum['sum'] + pivot_cum[j]
    for k in list_of_columns:
        pivot_cum[f'{k}_udzial'] = pivot_cum[k] / pivot_cum['sum']
        pivot_cum.drop(columns=[k], inplace=True)
        pivot_cum.rename(columns={f'{k}_udzial': k}, inplace=True)
    pivot_cum.drop(columns=['sum'], inplace=True)
    return pivot_cum