import pandas as pd

from functions_pandas.short_mailings_names import change_name_shot_to_long


def add_prefiex(con, refresh_data, engine):
    if refresh_data=='True':
        data = pd.read_csv('./pages/ma_details_files/tmp_file/people_camp.csv', index_col='Unnamed: 0')
        data = change_name_shot_to_long(data)
        sql = '''
select kod_akcji,grupa_akcji_2, grupa_akcji_3::int, fcma.prefix as akcja_glowna_mailingu, fca.name as akcja_mailingu from t_akcje ta
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
AND FCMA.newly_acquired=FALSE'''
        tmp = pd.read_sql_query(sql, con)
        data = pd.merge(data, tmp, how='left', left_on=['kod_akcji_wysylki', 'grupa_akcji_2_wysylki', 'grupa_akcji_3_wysylki'],
                        right_on=['kod_akcji', 'grupa_akcji_2', 'grupa_akcji_3'])
        sql = '''select distinct grupa_akcji_2, grupa_akcji_3, fcma.prefix as akcja_glowna_mailingu,
       fcsi.prefix_correct, fcsi.prefix_incorrect
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
left outer join fsaps_campaign_shipping_indicator fcsi on fcma.id = fcsi.main_action_address_id
where id_grupy_akcji_1=23 and  ta.id_grupy_akcji_2 in (9,10,11,12,24,67,100)
AND FCMA.newly_acquired=FALSE
order by grupa_akcji_2, grupa_akcji_3 '''
        list_of_ind = pd.read_sql(sql, con)
        list_of_ind.drop(list_of_ind.loc[list_of_ind['prefix_correct']=='ZW'].index, inplace=True)
        list_of_ind.drop(list_of_ind.loc[list_of_ind['prefix_correct']=='BW'].index, inplace=True)
        sql = '''select max(ilosc) as maks from (select main_action_address_id, count(id) as ilosc 
        from fsaps_campaign_shipping_indicator group by main_action_address_id)a'''
        number = pd.read_sql_query(sql, con)
        number_fin = number['maks'].iloc[0]
        for i in range(0, number_fin+1):
            data[f'wspolczynnik_{i+1}'] = ''
        sql = '''select grupa_akcji_3 from t_grupy_akcji_3 where grupa_akcji_3 not like 'NIE%' order by grupa_akcji_3'''
        lata = pd.read_sql_query(sql, con)
        sql = '''select grupa_akcji_2 from t_grupy_akcji_2 where id_grupy_akcji_2 in (9,10,11,12,24,67,100)'''
        mailingi = pd.read_sql_query(sql, con)
        for j, row in lata.iterrows():
            for z, row2 in mailingi.iterrows():
                y = 0
                #todo usunac prefiz zw i bw i daoc go na sztywno
                sql = f"""select distinct grupa_akcji_2, grupa_akcji_3, fcma.prefix as akcja_glowna_mailingu,
       fcsi.prefix_correct, fcsi.prefix_incorrect
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
left outer join fsaps_campaign_shipping_indicator fcsi on fcma.id = fcsi.main_action_address_id
where grupa_akcji_2='{row2.iloc[0]}' and  grupa_akcji_3='{row.iloc[0]}'
AND FCMA.newly_acquired=FALSE
order by grupa_akcji_2, grupa_akcji_3  """
                test = pd.read_sql_query(sql, con)
                if len(test)>0:
                    for x, row3 in test.iterrows():
                        number = x + 1
                        test2=row3['grupa_akcji_2']
                        test3=row3['prefix_correct']
                        test4=row3['grupa_akcji_3']
                        #todo dodac warunek nie spelnienia
                        #todo dorobic do bazy rodzaj warunku
                        print(test2)
                        print(test3)
                        print(test4)
                        if row3['prefix_correct'] != None:
                            data[f'wspolczynnik_{number}'].loc[(data['grupa_akcji_2_wysylki'] == row3['grupa_akcji_2']) &
                                                           (data['grupa_akcji_3_wysylki'] == int(row3['grupa_akcji_3'])) &
                                                        (data['akcja_glowna_mailingu'] == row3['akcja_glowna_mailingu']) &
(data['kod_akcji'].str.contains(test3, na=False))] = row3['prefix_correct']
        data.to_csv('./pages/ma_details_files/tmp_file/people_camp.csv')


