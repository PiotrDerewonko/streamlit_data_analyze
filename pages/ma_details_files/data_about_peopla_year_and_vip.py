import os
from datetime import datetime

import pandas as pd


def add_age_and_vip(data, _con) -> pd.DataFrame:
    """dodaje do przekazanych danych infromacja na temat wieku, oraz czy darczynca byl vipem.
    Wazne, wiek jest liczony na rok danej wrzutki, tzn jesli dzis darczynca ma 100 lat to w we wszystkich
    mailingach ubieglorocznych bedzie mial 99 lat, a w mailingach 2 lata temu 98 lat itd.
    Stwierdzenei czy byl vipem czy nie rowniez odbywa sie latami czyli jesli ktos nie w ubieglym roku nie
    spelnial warunkow vip a w tym juz tak, to w obieglym roku bedzie mial staus pzoostali w tym vip"""
    year_now = datetime.now().year
    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     '../.././sql_queries/2_ma_detail/age.sql'))
    with open(sql_file_path, 'r') as sql_file:
        age_sql = sql_file.read()

    sql_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     '../.././sql_queries/2_ma_detail/is_vip_for_year.sql'))
    with open(sql_file_path, 'r') as sql_file:
        vip_sql = sql_file.read()

    # dodaje kolumny odnosnie wieku i statusu vip do uzupelniania w pozniejszych krokach
    data['przedzial_wieku'] = ' '
    data['vip'] = ' '
    data.set_index(['id_korespondenta', 'grupa_akcji_3_wysylki'], inplace=True)

    # petla w celu aktualizacji przekazanych danych o przedial wieku i status vip, dla kazdego roku osobno
    for k in range(2009, year_now + 1):
        age_sql_copy = age_sql.replace('#A#', str(k))
        vip_sql_copy = vip_sql.replace('#A#', str(k))
        vip_sql_copy = vip_sql_copy.replace('#B#', str(k - 1))
        age_data = pd.read_sql_query(age_sql_copy, _con)
        vip_data = pd.read_sql_query(vip_sql_copy, _con)
        age_data.set_index(['id_korespondenta', 'rok'], inplace=True)
        vip_data.set_index(['id_korespondenta', 'rok'], inplace=True)
        data.update(age_data)
        data.update(vip_data)

    #uzupelniam puste wiersze o fraze brak danych
    data.reset_index(inplace=True)
    data['przedzial_wieku'].loc[data['przedzial_wieku'] == ' '] = 'brak danych'
    data['przedzial_wieku'].loc[data['przedzial_wieku'] == ''] = 'brak danych'
    data['przedzial_wieku'].fillna('brak danych', inplace=True)
    data['vip'].loc[data['vip'] == ' '] = 'pozostali'
    data['vip'].loc[data['vip'] == ''] = 'pozostali'
    data['vip'].fillna('pozostali', inplace=True)

    return data
