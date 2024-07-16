import pandas as pd

def pivot_table(df):
    pivot_table = pd.pivot_table(df, values='total', index=['year', 'month', 'day'], columns=['type'])