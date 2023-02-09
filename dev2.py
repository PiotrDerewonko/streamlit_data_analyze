import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show

# utwórz DataFrame z multiindexem
index = pd.MultiIndex.from_tuples([('A', 'foo'), ('A', 'bar'), ('B', 'baz')], names=['one', 'two'])
df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]}, index=index)

# wybierz kolumny i przekształć DataFrame na jednopoziomowy
df_new = df.reset_index().set_index('one')

# utwórz ColumnDataSource z nowego DataFrame
source = ColumnDataSource(df_new)

# utwórz wykres słupkowy
p = figure(x_range=df_new.index.unique().tolist())
p.vbar(x='one', top='y', width=0.9, source=source)


show(p)
print('ok')