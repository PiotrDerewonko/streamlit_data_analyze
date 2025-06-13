
def delete_tables(conn):

    # Lista nazw tabel do usunięcia (bez schematu)
    tables_to_drop = ["cr_distance_corr", "cr_distance_pay", "dash_char_ma_data", "dash_char_ma_data_cost_cir",
                      "dash_db_data", "dash_increase_data", "dash_ma_data", "streamlit_cost_structure", "weeks_of_db"]

    conn.autocommit = True  # lub użyj commit() na końcu
    cur = conn.cursor()

    # Usuwanie tabel
    for table_name in tables_to_drop:
        print(f"Usuwanie tabeli: {table_name}")
        cur.execute(f'DROP TABLE IF EXISTS raporty."{table_name}" CASCADE;')

    # Zamknięcie połączenia
    cur.close()

def update_tables(conn):

    # Lista nazw tabel do usunięcia (bez schematu)
    tables_to_drop = ["""alter table raporty.dash_char_ma_data
    alter column liczba_wplat type int using liczba_wplat::int""", """alter table raporty.dash_char_ma_data_cost_cir
    alter column naklad type int using naklad::int;""", """
alter table raporty.dash_char_ma_data_cost_cir
    alter column dzien_po_mailingu type int using dzien_po_mailingu::int;"""]

    conn.autocommit = True  # lub użyj commit() na końcu
    cur = conn.cursor()

    # Usuwanie tabel
    for table_name in tables_to_drop:
        print(f"aktualizacja tabeli: {table_name}")
        cur.execute(f'{table_name} ')

    # Zamknięcie połączenia
    cur.close()
