import pandas as pd

def change_name(data):
    data.replace('MAILING Q1', 'Q1.1', inplace=True)
    data.replace('MAILING Q2', 'Q2', inplace=True)
    data.replace('MAILING Q3', 'Q3.1', inplace=True)
    data.replace('MAILING Q4', 'Q4', inplace=True)
    data.replace('KARDYNALSKA SIERPIEŃ', 'Q3.0 KARD', inplace=True)
    data.replace('KARDYNALSKA LUTY', 'Q1.0 KARD', inplace=True)
    data.replace('MAILING Q3 KUSTOSZ LIPIEC', 'Q3 KUST', inplace=True)
    data.replace('KARDYNALSKA LUTY PRIM', 'Q1.0 KARD', inplace=True)
    data.replace('KARDYNALSKA LUTY BIS', 'Q1.0 KARD', inplace=True)

    return data