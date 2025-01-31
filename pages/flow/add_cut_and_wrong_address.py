import pandas as pd

def add_others_address(df, year, df_people):
    """Funkcja dodaje wszystkich korespondentow ktorzy byli w bazie danych w przekazanym roku lub wcześniej. Następnie
    usuwa duplikaty na bazie roku i id_korespondenta zachowując pierwotne wartości, a usuwając dodane. W efekcie
    uzyskujemy listę wszystkich korespondentów na dany rok"""
    people_by_year = df_people.loc[df_people.data_dodania <= (str(year)+'12-31')]
    df = pd.concat([df, people_by_year])


def add_cut_and_wrong_address(df, max_year, df_people):
    for i in range(2008, max_year + 1):
        add_others_address(df, i, df_people)

