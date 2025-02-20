import pandas as pd


def add_others_address(df, year, df_people):
    """Funkcja dodaje wszystkich korespondentow ktorzy byli w bazie danych w przekazanym roku lub wcześniej. Następnie
    usuwa duplikaty na bazie roku i id_korespondenta zachowując pierwotne wartości, a usuwając dodane. W efekcie
    uzyskujemy listę wszystkich korespondentów na dany rok"""
    people_by_year = df_people.loc[df_people.data_dodania <= (str(year)+'12-31')]
    people_by_year['grupa_akcji_3_wysylki'] = year
    people_by_year['TYP DARCZYŃCY'] = 'odcięci'
    df = pd.concat([df, people_by_year])
    df = df.drop_duplicates(subset=['id_korespondenta', 'grupa_akcji_3_wysylki'], keep='first')
    return df


def add_cut_and_wrong_address(df, max_year, df_people):
    for i in range(2008, max_year + 1):
        df = add_others_address(df, i, df_people)
    return df

def add_wrong_address(df, year, df_people):
    pass

