def data_to_100_percent(data_all):
    data = data_all.copy()
    data.fillna(0, inplace=True)
    data['sum'] = 0

    for i in data.columns:
        if i != 'sum':
            data['sum'] = data['sum'] + data[i]
    tmp_df = data.copy()
    for j in data.columns:
        if j != 'sum':
            tmp_df[j] = tmp_df['sum']
    tmp2 = data.div(tmp_df)
    tmp2.drop(columns=['sum'], inplace=True)
    return tmp2