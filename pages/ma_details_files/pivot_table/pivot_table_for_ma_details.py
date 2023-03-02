import numpy as np
import pandas as pd


def create_pivot_table_for_ma_details(data, columns_options):
    data_all = data.copy()
    for i in columns_options:
        if data_all.dtypes[i] != np.object:
            data_all[i] = data_all[i].astype(str)
    pivot_to_return = data_all.pivot_table(values=['suma_wplat', 'liczba_wplat',
                                                   'koszt', 'naklad', 'suma_wplat_stand'],
                                           aggfunc='sum',
                                           index=columns_options)


    def my25(g):
        return g.quantile(0.25)

    def my75(g):
        return g.quantile(0.75)

    pivot_to_return_2 = data_all.pivot_table(values=['suma_wplat_stand'], aggfunc=[my25, np.median, my75, np.std],
                                             index=columns_options, margins=True)

    pivot_to_return = pivot_to_return.merge(pivot_to_return_2, how='left', left_index=True, right_index=True)
    a = pivot_to_return.columns
    pivot_to_return.rename(columns={a[5]: 'Pierwszy_percentyl'}, inplace=True)
    pivot_to_return.rename(columns={a[6]: 'mediana'}, inplace=True)
    pivot_to_return.rename(columns={a[7]: 'Trzeci_percentyl'}, inplace=True)
    pivot_to_return.rename(columns={a[8]: 'Odchylenie'}, inplace=True)
    pivot_to_return['średnia'] = pivot_to_return['suma_wplat'] / pivot_to_return['liczba_wplat']
    pivot_to_return['średnia_stand'] = pivot_to_return['suma_wplat_stand'] / pivot_to_return['liczba_wplat']
    pivot_to_return['ROI'] = pivot_to_return['suma_wplat'] / pivot_to_return['koszt']
    pivot_to_return['SZLW'] = (pivot_to_return['liczba_wplat'] / pivot_to_return['naklad']) * 100
    pivot_to_return['Koszt_na_głowę'] = pivot_to_return['koszt'] / pivot_to_return['naklad']
    pivot_to_return['SZLW do totalu'] = 0
    pivot_to_return['Nakład total'] = 0
    for j in columns_options:
        tmp_sum = pd.pivot_table(data_all, index=j, values=['naklad'], aggfunc='sum')
        a = 0


    return pivot_to_return

def style_pivot_table_for_ma(pivot_to_return):
    def highlight_everyother(s):
        return ['background-color: yellow' if x % 2 == 1 else ''
                for x in range(len(s))]

    pivot_to_return['suma_wplat'].loc[pivot_to_return.index.isin(pivot_to_return.index)] = \
        pivot_to_return['suma_wplat'].apply(lambda x: "{:.0f} zł".format(x))
    pivot_to_return['koszt'].loc[pivot_to_return.index.isin(pivot_to_return.index)] = \
        pivot_to_return['koszt'].apply(lambda x: "{:.0f} zł".format(x))
    pivot_to_return['liczba_wplat'].loc[pivot_to_return.index.isin(pivot_to_return.index)] = \
        pivot_to_return['liczba_wplat'].apply(lambda x: "{:.0f}".format(x))
    pivot_to_return['średnia'].loc[pivot_to_return.index.isin(pivot_to_return.index)] = \
        pivot_to_return['średnia'].apply(lambda x: "{:.0f} zł".format(x))
    pivot_to_return['ROI'].loc[pivot_to_return.index.isin(pivot_to_return.index)] = \
        pivot_to_return['ROI'].apply(lambda x: "{:.2f} zł".format(x))
    pivot_to_return['SZLW'].loc[pivot_to_return.index.isin(pivot_to_return.index)] = pivot_to_return['SZLW'].\
        apply(lambda x: "{:.0f} %".format(x))

    t = pivot_to_return.style.apply(highlight_everyother)
    t.set_table_styles([{"selector": "", "props": [("border", "1px solid grey")]}])
    t.set_table_styles([{"selector": "", "props": [("border", "1px solid grey")]},
                        {"selector": "tbody td", "props": [("border", "1px solid grey")]},
                        {"selector": "th", "props": [("border", "1px solid grey")]}
                        ])
    return pivot_to_return