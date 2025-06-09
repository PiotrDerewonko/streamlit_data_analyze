
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
