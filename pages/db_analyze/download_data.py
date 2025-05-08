import pandas as pd
import os
from dateutil.relativedelta import relativedelta
from pages.main_diractor.download_data_main import DownloadDataMain


class DataForLivePeopleFromDB(DownloadDataMain):
    """Klasa generuje dane potrzebne do wykresu z cyklem życia darczyńcy z druków bezadresowych."""


def generate_data_for_live_people(_con, engine, test_mode=False) -> None:
    """Funkcja tworzy obiekt klasy, generującej dane do wykresu z cyklem życia darczyńcy."""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_file/db.csv'))
    live_people_from_db = DataForLivePeopleFromDB(_con, engine, csv_path, test_mode)
    subaction_list = live_people_from_db.get_data_from_sql('sql_queries/4/subackion_list.sql')
    cost_of_living = live_people_from_db.get_data_from_sql('sql_queries/4/total_cost_of_living.sql')

    final_df = pd.DataFrame(
        data={'id_korespondenta': 1, 'data_dodania': '2008-01-01', 'suma_wplat': 0, 'koszt_utrzymania': 0}, index=[0])
    # iteruje pętlą po każdej sub akcji z listy
    for i, row in subaction_list.iterrows():
        temporary_data_for_sub_action = live_people_from_db.get_data_from_sql_with_replace(
            'sql_queries/4/people_from_subaction.sql',
            {'#A#': f"""{row['id_akcji']}"""})
        temporary_data_for_sub_action['data_tmp'] = temporary_data_for_sub_action['data_dodania']
        fin_for_subaction = temporary_data_for_sub_action.copy()

        # tworze dla każdego korespondenta z danej subakcji, 24 miesiące, które będę analizował
        for j in range(1, 24):
            temporary_data_for_sub_action['data_tmp'] = temporary_data_for_sub_action['data_tmp'] + relativedelta(
                months=1)
            temporary_data_for_sub_action['miesiac_obecnosci_w_bazie'] = j + 1
            fin_for_subaction = pd.concat([fin_for_subaction, temporary_data_for_sub_action], ignore_index=True)

            # wyciagam unikalna liste data dodania i zamieniam na pierwszy u osoatni dzien miesiaca w celu dalszych petli
            date = fin_for_subaction['data_tmp'].drop_duplicates().to_frame()
            date['last_day'] = date['data_tmp'] + relativedelta(day=31)
            date['first_day'] = date['data_tmp'] - relativedelta(day=1)
            date.drop(columns=['data_tmp'], inplace=True)
            date.drop_duplicates(subset=['first_day'], inplace=True)
            fin_for_subaction['data_tmp'] = fin_for_subaction['data_tmp'] - relativedelta(day=1)
            fin_for_subaction['year'] = fin_for_subaction['data_tmp'].astype(str).str[:4].astype(int)
            fin_for_subaction['month'] = fin_for_subaction['data_tmp'].astype(str).str[5:7].astype(int)

            # pobieram unikalan liste uzytkownikow
            list_of_id = temporary_data_for_sub_action.drop_duplicates(subset=['id_korespondenta'])
            list_of_id2 = tuple(list_of_id['id_korespondenta'])
            if len(list_of_id2) <= 1:
                continue

            # pobieram uniklan liste dat dodania (wszytskie jako 1 dzien miesiaca)
            uniq_data_of_add = temporary_data_for_sub_action['data_dodania'].drop_duplicates().to_frame()
            uniq_data_of_add['first_day'] = temporary_data_for_sub_action['data_dodania'] - relativedelta(day=1)
            uniq_data_of_add.drop(columns=['data_dodania'], inplace=True)
            uniq_data_of_add = uniq_data_of_add.drop_duplicates()
            uniq_data_of_add['last_day'] = uniq_data_of_add['first_day'] + relativedelta(day=31)
            uniq_data_of_add.sort_values(by='first_day', inplace=True)

            # petla dodajaca sume wplat w tabeli z datami
            print(f'''rozpoczynam dodawanie wplat {row['kod_akcji']}''')
            for j3, row3 in date.iterrows():
                rok = int(str(row3['first_day'])[:4])
                miesiac = int(str(row3['first_day'])[5:7])
                data_tmp_pay = live_people_from_db.get_data_from_sql_with_replace('sql_queries/4/payment_in_months.sql',
                                                                                  {
                                                                                      '#DATE_FROM#': f"""'{row3['first_day'].isoformat()}'""",
                                                                                      "#DATE_TO#": f"""'{row3[
                                                                                          'last_day'].isoformat()}'""",
                                                                                      "#LIST_COR_ID#": str(list_of_id2),
                                                                                      "#MIESIAC#": str(miesiac),
                                                                                      "#ROK#": str(rok)})
                if len(data_tmp_pay) >= 1:
                    data_tmp_pay.set_index(['id_korespondenta', 'year', 'month'], inplace=True)
                    fin_for_subaction.set_index(['id_korespondenta', 'year', 'month'], inplace=True)
                    fin_for_subaction.update(data_tmp_pay)
                    fin_for_subaction.reset_index(inplace=True)
                print(f'''dodano wplaty lp {j3} dla {row['kod_akcji']} za rok {rok} za miesiac {miesiac} ''')
            print(f'''zakonczono dodawanie wplat {row['kod_akcji']}''')

            # petla dodajaca koszt utrzymania w tabeli z datami
            print(f'''rozpoczynam dodawanie kosztow {row['kod_akcji']}''')
            for j5, row5 in date.iterrows():
                rok = int(str(row5['first_day'])[:4])
                miesiac = int(str(row5['first_day'])[5:7])
                tmp_cost = cost_of_living.loc[(cost_of_living['data'] >= row5['first_day']) &
                                               (cost_of_living['data'] <= row5['last_day']) &
                                               (cost_of_living['id_korespondenta'].isin(list_of_id2))]
                if len(tmp_cost) >= 1:
                    tmp_cost['month'] = miesiac
                    tmp_cost['year'] = rok
                    tmp_pivot = pd.pivot_table(tmp_cost, index=['id_korespondenta', 'year', 'month'],
                                               values='koszt_utrzymania', aggfunc='sum')
                    fin_for_subaction.set_index(['id_korespondenta', 'year', 'month'], inplace=True)
                    fin_for_subaction.update(tmp_pivot)
                    fin_for_subaction.reset_index(inplace=True)
                print(f'''dodano koszty lp {j5} dla {row['kod_akcji']} za rok {rok} za miesiac {miesiac} ''')

            print(f'''zakonczono dodawanie kosztow {row['kod_akcji']}''')
            # dodanie kosztów pozyskania
            cost_of_add = live_people_from_db.get_data_from_sql_with_replace('sql_queries/4/new_cost_of_insert.sql',
                                                                             {'#id#': str(row['id_akcji'])})

            # lacze utworzona tabela dla danej sub akcji w jedną wielką tabelę ze wszystkimi subakcjiami
            final_df = pd.concat([final_df, fin_for_subaction, cost_of_add])
            final_df.fillna(0, inplace=True)
        if test_mode:
            break

    # dodac grupy akcji 1,2,3
    tags = live_people_from_db.get_data_from_sql_with_out_limit('sql_queries/4/tags.sql')
    final_df['id_akcji'] = final_df['id_akcji'].astype(int)
    final_df = pd.merge(final_df, tags, on='id_akcji', how='left')

    #zapisuje plik
    live_people_from_db.insert_data(final_df)


def download_data_for_live_people(_con, engine, test_mode=False) -> pd.DataFrame:
    """Funkcja tworzy obiekt klasy, pobierający dane do wykresu z cyklem życia darczyńcy."""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_file/db.csv'))
    live_people_from_db = DataForLivePeopleFromDB(_con, engine, csv_path, test_mode)
    data_to_analyze = live_people_from_db.download_data()
    return data_to_analyze

class DataForDbInWeeks(DownloadDataMain):
    """Klasa generuje dane potrzebne do wykresu z tygodniami wpłat z druków bezadresowych."""


def generate_data_for_db_weeks(_con, engine, test_mode=False) -> None:
    """Funkcja tworzy obiekt klasy, generuje dane do wykresu z wpłatami w tygodniach dla db."""
    table_name = 'weeks_of_db'
    weeks_for_db = DataForDbInWeeks(_con, engine, table_name, test_mode)
    data_part_1 = weeks_for_db.get_data_from_sql('sql_queries/4/payments_in_weeks.sql')
    data_part_2 = weeks_for_db.get_data_from_sql('sql_queries/4/cost_of_insert.sql')
    data_part_3 = weeks_for_db.get_data_from_sql('sql_queries/4/cost_of_realization.sql')
    final_data = pd.concat([data_part_1, data_part_2, data_part_3])
    weeks_for_db.insert_data(final_data)

def download_data_for_db_weeks(_con, engine, test_mode=False) -> pd.DataFrame:
    """Funkcja tworzy obiekt klasy, pobierający dane do wykresu z wpłatami w tygodniach dla db."""
    table_name = 'weeks_of_db'
    weeks_for_db = DataForDbInWeeks(_con, engine, table_name, test_mode)
    data = weeks_for_db.download_data()
    return data