import pandas as pd
def pivot_table_w_subtotals(df, values, indices, columns, aggfunc, fill_value):
    '''
    Adds tabulated subtotals to pandas pivot tables with multiple hierarchical indices.

    Args:
    - df - dataframe used in pivot table
    - values - values used to aggregrate
    - indices - ordered list of indices to aggregrate by
    - columns - columns to aggregrate by
    - aggfunc - function used to aggregrate (np.max, np.mean, np.sum, etc)
    - fill_value - value used to in place of empty cells

    Returns:
    -flat table with data aggregrated and tabulated

    '''
    listOfTable = []
    listofFirstTable = []
    for indexNumber in range(len(indices)):
        n = indexNumber + 1

        table = pd.pivot_table(df, values=values, index=indices[:n],
                               columns=columns,
                               aggfunc=aggfunc,
                               fill_value=fill_value).reset_index()
        if n == 1:
            listofFirstTable.append(table)
        if n == len(indices):
            test = indices[n - 1]
            test2 = indices[:n - 1]
            concatLastTable = table.copy()
            concatLastTable['new_index'] = ''
            for i in range(len(indices)):
                concatLastTable['new_index'] = concatLastTable['new_index'] + concatLastTable[indices[i]]
            concatLastTable.set_index(keys='new_index', inplace=True)
            concatLastTable.drop(columns=indices[:n+1], axis=1, inplace=True)
        for column in indices[n:]:
            table[column] = ''
        listOfTable.append(table)
    concatTable = pd.concat(listOfTable).sort_index()
    concatTable = concatTable.set_index(keys=indices)

    return concatTable.sort_index(axis=0, ascending=True), concatLastTable