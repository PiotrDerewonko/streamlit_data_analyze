import pandas as pd
import plotly.express as px

# Przykładowe dane (zakładam, że masz takie dane w swoim DataFrame)
data = {
    'Value': [10, 20, 15, 25, 30, 35],
    'Year': [2021, 2021, 2021, 2022, 2022, 2022],
    'Month': [1, 2, 3, 4, 5, 6],
    'Day': [1, 1, 1, 1, 1, 1]
}

# Tworzenie DataFrame'a z indeksem wielopoziomowym
df = pd.DataFrame(data)
df.set_index(['Year', 'Month', 'Day'], inplace=True)

# Resetowanie indeksu MultiIndex'a do kolumny (tworzymy nowe kolumny 'Year', 'Month' i 'Day')
df_reset = df.reset_index()

# Łączenie kolumn 'Year', 'Month' i 'Day' w jedno pole 'Date' jako nowy indeks
df_reset['Date'] = pd.to_datetime(df_reset[['Year', 'Month', 'Day']])
df_reset.set_index('Date', inplace=True)

# Tworzenie wykresu liniowego
fig = px.line(df_reset, x=df_reset.index, y='Value', markers=True, title='Wykres z indeksem z trzech pól')
fig.show()