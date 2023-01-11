from datetime import datetime

import pandas as pd

from functions_pandas.short_mailings_names import change_name_shot_to_long


def add_prefix(con, refresh_data, engine):
    if refresh_data=='True':
        data = pd.read_csv('./pages/ma_details_files/tmp_file/people_camp.csv', index_col='Unnamed: 0')
        data = change_name_shot_to_long(data)
        sql = '''
select kod_akcji,grupa_akcji_2, grupa_akcji_3::int, fcma.name as akcja_glowna_mailingu, fca.name as akcja_mailingu 
from t_akcje ta
    left outer join t_grupy_akcji_2 gr2
    on gr2.id_grupy_akcji_2=ta.id_grupy_akcji_2
    left outer join t_grupy_akcji_3 gr3
    on gr3.id_grupy_akcji_3=ta.id_grupy_akcji_3
left outer join fsaps_campaign_campaign fcc
on fcc.action_group_one_id=ta.id_grupy_akcji_1 and fcc.action_group_two_id = ta.id_grupy_akcji_2 and
   fcc.action_group_three_id = ta.id_grupy_akcji_3
left outer join fsaps_campaign_main_action fcma on fcc.id = fcma.campaign_id and
                                                   ta.kod_akcji like '%'||fcma.prefix||'%'
left outer join fsaps_campaign_action fca on fcma.id = fca.action_main_id and
                                                   ta.kod_akcji like '%'||fca.prefix||'%'
where id_grupy_akcji_1=23 and  ta.id_grupy_akcji_2 in (9,10,11,12,24,67,100)

'''
        tmp = pd.read_sql_query(sql, con)
        data = pd.merge(data, tmp, how='left', left_on=['kod_akcji_wysylki', 'grupa_akcji_2_wysylki', 'grupa_akcji_3_wysylki'],
                        right_on=['kod_akcji', 'grupa_akcji_2', 'grupa_akcji_3'])

        #dodaje naglowki kolumn na podsatwie slownika z rodzajammi wspolczynnikow
        sql = f'''select text from fsaps_dictionary_shipping_factor_condition order by text'''
        tmp = pd.read_sql_query(sql, con)
        for it in tmp.iterrows():
            text = it[1][0]
            data[text] = ''

        #dodaje dane do dodanych kolumn
        sql = '''select text from fsaps_dictionary_action_group_two where is_for_billing = True'''
        group_two = pd.read_sql_query(sql, con)
        rok = datetime.now().year
        for year in range(2022, rok+1):
            for gr2, row_1 in group_two.iterrows():
                sql = f'''select prefix_correct as prefiks_wspolczynnika, fcma.name as akcja_glowna,
                text as rodzaj_wspolczynnika from fsaps_campaign_shipping_indicator fcsi 
                left outer join fsaps_dictionary_shipping_factor_condition fdsfc 
                on fcsi.shiping_type = fdsfc.id
                left outer join fsaps_campaign_main_action fcma 
                on fcsi.main_action_address_id = fcma.id
                where main_action_address_id in (
                select id from fsaps_campaign_main_action where campaign_id in (
                select id from fsaps_campaign_campaign where action_group_two_id in (
                select id from fsaps_dictionary_action_group_two where text = '{row_1.iloc[0]}')
                and action_group_three_id in (select id from fsaps_dictionary_action_group_three where text='{year}')))'''
                data_tmp = pd.read_sql_query(sql, con)
                for j, row in data_tmp.iterrows():
                    if row['rodzaj_wspolczynnika'] is not None:
                        a = row_1.iloc[0]
                        b = row['prefiks_wspolczynnika']
                        c = row['akcja_glowna']

                        data[row['rodzaj_wspolczynnika']].loc[(data['akcja_glowna_mailingu'] == c) &
                                                          (data['grupa_akcji_2_wysylki'] == a) &
                                                          (data['grupa_akcji_3_wysylki'] == year) &
                                                          (data['kod_akcji_wysylki'].str.contains(row['prefiks_wspolczynnika']))
                                                              ] = \
                        row['rodzaj_wspolczynnika']
                        print('dodano')



        data.to_csv('./pages/ma_details_files/tmp_file/people_camp.csv')


