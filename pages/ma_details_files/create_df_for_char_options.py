import pandas as pd


def create_df_for_char_options_structure(data) -> pd.DataFrame:
    columns_name = data.columns
    index_column_name = []
    j = 0
    for i in columns_name:
        index_column_name.append(j)
        j += 1
    d = {'Nazwa parametru': columns_name}
    new_option_char = pd.DataFrame(data=d, index=index_column_name)
    new_option_char['oś'] = 'Oś główna'
    new_option_char['Opcje'] = 'Wykres Słupkowy Skumulowany'
    return new_option_char
