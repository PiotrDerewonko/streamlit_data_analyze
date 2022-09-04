import pandas as pd

def change_name(data):
    data.replace('MAILING Q1', 'Q1', inplace=True)
    data.replace('MAILING Q2', 'Q2', inplace=True)
    data.replace('MAILING Q3', 'Q3', inplace=True)
    data.replace('MAILING Q4', 'Q4', inplace=True)
    data.replace('KARDYNALSKA SIERPIEŃ', 'Q3 KARD', inplace=True)
    data.replace('KARDYNALSKA LUTY', 'Q1 KARD', inplace=True)
    data.replace('MAILING Q3 KUSTOSZ LIPIEC', 'Q3 KUST', inplace=True)
    return data