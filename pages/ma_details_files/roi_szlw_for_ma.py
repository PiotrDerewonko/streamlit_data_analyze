import pandas as pd

def roi(data1, data2):
    df1_index_len = len(data1)
    data2.reset_index(inplace=True)
    data2_tmp = data2.copy()
    for i in range(2, df1_index_len+3):
        data2_tmp['dzien_po_mailingu'] = i
        data2 = pd.concat([data2, data2_tmp])
    data2.set_index('dzien_po_mailingu', inplace=True)
    data_to_return = data1.div(data2)
    return data_to_return
