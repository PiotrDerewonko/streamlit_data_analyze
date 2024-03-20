import pandas as pd


def add_extra_filter(df, list_to_loc) -> pd.DataFrame:
    """funkcja ktrórej zadaniem jest dodatkowe odfiltorwanie danych. Do tego celu wykorzystuje listę pobraną
    z popovera"""
    if len(list_to_loc) >= 1:
        # Tworzenie warunkowej maski logicznej
        condition = None
        for i, val in enumerate(list_to_loc):
            warunek_logiczny = eval(val)
            if condition is None:
                condition = warunek_logiczny
            else:
                condition &= warunek_logiczny

            # Zastosowanie warunku do filtrowania DataFrame
        data_to_return = df.loc[condition]
    else:
        data_to_return = df

    return data_to_return
