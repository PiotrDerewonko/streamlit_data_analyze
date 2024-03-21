import pandas as pd


def data_to_100_percent(data_all) -> pd.DataFrame:
    """Zadaniem funkcji jest zwrocenie początkowego dataframu ale zamiast wartości bezwględnych, są wartości
    procentowe. Wyliczanie procentow odbywa się dla każdego wiersza osobno."""
    data = data_all.copy()
    data.fillna(0, inplace=True)
    data['sum'] = 0

    # petla ma na celu zsumowanie wartosci kadego wiersza
    for i in data.columns:
        if i != 'sum':
            data['sum'] = data['sum'] + data[i]

    tmp_df = data.copy()

    # na uwtorzonej kopii df dodaje we wszystkie komorki oprocz kolumnu sum, sume danego wiersza
    for j in data.columns:
        if j != 'sum':
            tmp_df[j] = tmp_df['sum']

    # dziale poczatkowe tabele przez skopiowana tabele zawierajaca sumy wierszy w kazdej komorce
    tmp2 = data.div(tmp_df)
    tmp2.drop(columns=['sum'], inplace=True)
    return tmp2
