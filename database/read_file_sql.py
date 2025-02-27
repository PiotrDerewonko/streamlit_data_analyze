import os

def read_file_sql(filename) -> str:
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     f'../{filename}'))
    with open(sql_file_path, 'r') as sql_file:
        zapytanie = sql_file.read()
    return zapytanie