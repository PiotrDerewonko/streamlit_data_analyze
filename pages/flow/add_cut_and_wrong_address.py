import pandas as pd

from pages.flow.wrong_address import wrong_address


def add_others_address(df, year, df_people):
    """Funkcja dodaje wszystkich korespondentow ktorzy byli w bazie danych w przekazanym roku lub wcześniej. Następnie
    usuwa duplikaty na bazie roku i id_korespondenta zachowując pierwotne wartości, a usuwając dodane. W efekcie
    uzyskujemy listę wszystkich korespondentów na dany rok"""
    people_by_year = df_people.loc[df_people.data_dodania <= (str(year) + '12-31')]
    people_by_year['grupa_akcji_3_wysylki'] = year
    people_by_year['TYP DARCZYŃCY'] = 'odcięci'
    df = pd.concat([df, people_by_year])
    df = df.drop_duplicates(subset=['id_korespondenta', 'grupa_akcji_3_wysylki'], keep='first')
    return df


def add_cut_and_wrong_address(df, max_year, df_people):
    for i in range(2008, max_year + 1):
        df = add_wrong_address(df, i, df_people)
        df = add_others_address(df, i, df_people)
        df = update_new_people(df, i, df_people)
    return df


def add_wrong_address(df, year, df_people):
    """Metoda pobiera dane o błędnych adresach, odfiltrowuje tylko te adresy, które zostały zablokowane w przekazanym
    roku lub wcześniej. Następnie dodaje te dane do pliku głównego,i usuwa duplikaty. Jeśli w danym roku
    korespondent otrzymał choć jeden mailing, ale przeszedł, też zwrot to w finalnym pliku będzie info tylko o typie
    z mailingu. Jeśli w danym roku korespondent nie dostał żadnego mailingu, a co za tym idzie, nie ma przypisanego typu,
    zostanie mu dopisany typ zwrot."""
    data_wrong_address = wrong_address(False, None)
    data_wrong_address = data_wrong_address.loc[data_wrong_address['blocked_at'] <= f'{year}-12-31']
    data_wrong_address = data_wrong_address.rename(columns={'correspondent_id': 'id_korespondenta'})
    data_wrong_address = data_wrong_address[['id_korespondenta']].drop_duplicates()  # Zostaw DataFrame
    people_by_year = df_people.loc[df_people.id_korespondenta.isin(data_wrong_address['id_korespondenta'])]
    people_by_year['grupa_akcji_3_wysylki'] = year
    people_by_year['TYP DARCZYŃCY'] = 'zwrot'
    df = pd.concat([df, people_by_year])
    df = df.drop_duplicates(subset=['id_korespondenta', 'grupa_akcji_3_wysylki'], keep='first')
    return df


def update_new_people(df, year, df_people):
    """Metoda odfiltrowuje ludzie, którzy w roku swojego wejścia mają status odcięci, i sprawdza czy, w kolejnym roku
    mają status < 3 lata. Jeśli tak, podmienia im typ w roku wejścia."""
    data_new_cut = df.loc[(df['TYP DARCZYŃCY'] == 'odcięci') & (df['grupa_akcji_3_wysylki'] == year) &
                          (df['rok_dodania'] == year)]
    data_new_next_year = df.loc[
        (df['grupa_akcji_3_wysylki'] == (year + 1)) & (df['TYP DARCZYŃCY'] == '<3 lata w bazie')]
    data_to_update = data_new_cut.loc[data_new_cut.id_korespondenta.isin(data_new_next_year.id_korespondenta)]
    data_to_update = data_to_update.loc[data_to_update['TYP DARCZYŃCY'] == '<3 lata w bazie']
    df.loc[df.id_korespondenta.isin(data_to_update.id_korespondenta)] = '<3 lata w bazie'
    return df
