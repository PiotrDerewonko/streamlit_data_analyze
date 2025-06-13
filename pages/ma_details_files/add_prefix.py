import os
from datetime import datetime

import pandas as pd

from functions_pandas.short_mailings_names import change_name_shot_to_long


def add_prefix(con, refresh_data, engine):
    if refresh_data=='True':
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_file/people_camp.csv'))
        data = pd.read_csv(csv_path, index_col='Unnamed: 0')
        #tmp = pd.read_excel('./pages/ma_details_files/tmp_file/zastepcze.xlsx', sheet_name='Arkusz1')
        #data = pd.merge(data, tmp, on='kod_akcji_wysylki', how='left')

        #data.to_csv('./pages/ma_details_files/tmp_file/people_camp.csv')
        #print('zapisano')
        data = change_name_shot_to_long(data)
        #todo sql do wstawienia w pliki
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
left outer join (select * from fsaps_campaign_main_action where newly_acquired=False) fcma on fcc.id = fcma.campaign_id and
                                                   ta.kod_akcji like '%'||fcma.prefix||'%'
left outer join fsaps_campaign_action fca on fcma.id = fca.action_main_id and 
                                                   ta.kod_akcji like '%'||fca.prefix||'%'
where id_grupy_akcji_1=23 and  ta.id_grupy_akcji_2 in (9,10,11,12,24,67,100)

'''
        tmp = pd.read_sql_query(sql, con)
        data = pd.merge(data, tmp, how='left', left_on=['kod_akcji_wysylki', 'grupa_akcji_2_wysylki', 'grupa_akcji_3_wysylki'],
                        right_on=['kod_akcji', 'grupa_akcji_2', 'grupa_akcji_3'])

        #dodaje naglowki kolumn na podsatwie slownika z rodzajammi wspolczynnikow
        sql = f'''select text, text_negative from fsaps_dictionary_shipping_factor_condition order by text'''
        tmp = pd.read_sql_query(sql, con)
        for it in tmp.iterrows():
            text = it[1][0]
            text_default = it[1][1]
            data[text] = text_default

        #dodaje dane do dodanych kolumn
        sql = '''select text from fsaps_dictionary_action_group_two where is_for_billing = True'''
        group_two = pd.read_sql_query(sql, con)
        rok = datetime.now().year
        for year in range(2020, rok+1):
            for gr2, row_1 in group_two.iterrows():
                sql = f'''select prefix_correct as prefiks_wspolczynnika, fcma.name as akcja_glowna,
                text as rodzaj_wspolczynnika from fsaps_campaign_shipping_indicator fcsi 
                left outer join fsaps_dictionary_shipping_factor_condition fdsfc 
                on fcsi.shipping_factor_condition_id = fdsfc.id
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

        #dodaje dodatkowa kolumne zwiazana z kartami darczyncow
        data['KARTY'] = 'BRAK WPŁATY'
        lista_warunkow = {'UPGRADE KARTY': ['UPGR', 'WYMIANA'],
                          'WYDANIE NOWEJ KARTY': ['WYDANIE', 'A_NIEBIESKA'],
                          'PRZEDŁUŻENIE KARTY': ['PRZED'],
                          'BRAK KOMUNIKATU': ['WAŻNA', 'WAZNA']
                          }
        for key, value in lista_warunkow.items():
            for i in value:
                data['KARTY'].loc[(data['grupa_akcji_2_wysylki'].str.contains('KARDYNALS')) &
                                                      (data['kod_akcji_wysylki'].str.contains(i))] = key

        #dodaje dodatkowa kolumne zwiazana z kolorem karty darczyncow
        data['KOLOR KARTY'] = 'BEZ KARTY'
        lista_warunkow = {'ZŁOTA': ['ZŁOT'],
                          'SREBRNA': ['SREBR'],
                          'NIEBIESKA': ['NIEBIE'],
                          'WAŻNA KARTA': ['WAŻNA', 'WAZNA']
                          }
        for key, value in lista_warunkow.items():
            for i in value:
                data['KOLOR KARTY'].loc[(data['grupa_akcji_2_wysylki'].str.contains('KARDYNALS')) &
                                                      (data['kod_akcji_wysylki'].str.contains(i))] = key

        #dodaje dodatkowa kolumne zwiazana z potwierdzeniem wplaty
        data['WPŁATA'] = 'BEZ POTWIERDZENIA'
        lista_warunkow = {'Z POTWIERDZENIEM': ['_ZW']}
        for key, value in lista_warunkow.items():
            for i in value:
                data['WPŁATA'].loc[(data['kod_akcji_wysylki'].str.contains(i))] = key

        sql = '''select id_korespondenta, grupa_akcji_2 AS grupa_akcji_2_wysylki, grupa_akcji_3::int AS grupa_akcji_3_wysylki
        , case when
jaka_karta_wtedy = 0  then 'NIEBIESKA'
when jaka_karta_wtedy = 1 then 'SREBRNA'
when jaka_karta_wtedy = 2 then 'ZŁOTA'
else 'BRAK DANYCH'
end as KARTA_NA_MAILING
from
                                                           (
                                                               select distinct ak.id_korespondenta,
                                                                               t.grupa_akcji_2,
                                                                               tga3.grupa_akcji_3,

                                                                               case
                                                                                   when ak.data >=
                                                                                        wydanie_niebieskiej and
                                                                                        (ak.data < wydanie_srebrnej or wydanie_srebrnej is null)
                                                                                        and (ak.data < wydanie_zlotej or wydanie_zlotej is null)
                                                                                       then karta.niebieska
                                                                                   when ak.data >= wydanie_srebrnej and
                                                                                        (ak.data < wydanie_zlotej or wydanie_zlotej is null)
                                                                                       then karta.srebrna
                                                                                   when ak.data >= wydanie_zlotej
                                                                                       then karta.zlota
                                                                                   else null end as jaka_karta_wtedy

                                                               from t_akcje_korespondenci ak

                                                                        left join
                                                                    (
                                                                        select k.id_korespondenta,
                                                                               case
                                                                                   when (niebieska.wydanie_niebieskiej >= srebrna.wydanie_srebrnej) or
                                                                                        (niebieska.wydanie_niebieskiej >= zlota.wydanie_zlotej)
                                                                                       then null
                                                                                   else niebieska.wydanie_niebieskiej end as wydanie_niebieskiej,
                                                                               niebieska.niebieska,
                                                                               case
                                                                                   when srebrna.wydanie_srebrnej >= zlota.wydanie_zlotej
                                                                                       then null
                                                                                   else srebrna.wydanie_srebrnej end      as wydanie_srebrnej,
                                                                               srebrna.srebrna,

                                                                               zlota.wydanie_zlotej,
                                                                               zlota.zlota

                                                                        from (select distinct id_korespondenta from t_karty_darczyncow) k
                                                                                 left join
                                                                             (select id_korespondenta,
                                                                                     id_rodzaju_karty        as niebieska,
                                                                                     min(data_wydania_karty) as wydanie_niebieskiej
                                                                              from t_karty_darczyncow
                                                                              where id_rodzaju_karty = 0
                                                                              group by id_korespondenta, id_rodzaju_karty) niebieska
                                                                             on niebieska.id_korespondenta = k.id_korespondenta
                                                                                 left join
                                                                             (select id_korespondenta,
                                                                                     id_rodzaju_karty        as srebrna,
                                                                                     min(data_wydania_karty) as wydanie_srebrnej
                                                                              from t_karty_darczyncow
                                                                              where id_rodzaju_karty = 1
                                                                              group by id_korespondenta, id_rodzaju_karty) srebrna
                                                                             on srebrna.id_korespondenta = k.id_korespondenta
                                                                                 left join
                                                                             (select id_korespondenta,
                                                                                     id_rodzaju_karty        as zlota,
                                                                                     min(data_wydania_karty) as wydanie_zlotej
                                                                              from t_karty_darczyncow
                                                                              where id_rodzaju_karty = 2
                                                                              group by id_korespondenta, id_rodzaju_karty) zlota
                                                                             on zlota.id_korespondenta = k.id_korespondenta
                                                                    ) karta
                                                                    on karta.id_korespondenta = ak.id_korespondenta

                                                                        left join t_akcje a on a.id_akcji = ak.id_akcji
                                                                        left join t_grupy_akcji_2 t on a.id_grupy_akcji_2 = t.id_grupy_akcji_2
                                                                        left join t_grupy_akcji_3 tga3 on a.id_grupy_akcji_3 = tga3.id_grupy_akcji_3
                                                           ) foo
'''
        data_sql = pd.read_sql_query(sql, con)
        data = pd.merge(data, data_sql, how='left',
                        on=['id_korespondenta', 'grupa_akcji_2_wysylki', 'grupa_akcji_3_wysylki'])
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp_file/people_camp.csv'))
        data.to_csv(csv_path)


