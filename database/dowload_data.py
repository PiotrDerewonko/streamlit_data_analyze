import pandas as pd

from database.change_types_of_columns import change_types_of_columns


def download_dash_address_data(con, refresh, engine, type):
    if type == 'address':
        id_group_two = '(9,10,11,12,24,67,100)'
        extra = ''
        extra_group = ''
        extra_union = ''
    else:
        id_group_two = '(1, 2, 5, 91, 93, 95, 96, 101, 102, 103, 104, 105, 117, 118, 119, 120, 121, 122, 123, 124, 125,86, 126, 127, 128)'
        extra = ', substring(ta.kod_akcji, 7,2) as miesiac'
        extra_group = ',miesiac'
        extra_union = f'''union
        select grupa_akcji_3,grupa_akcji_2,kod_akcji, 0, 0, 0, 0, substring(kod_akcji, 7,2) as miesiac,
        count(id_korespondenta) as pozyskano 
        from v_akcja_dodania_korespondenta2
        where id_akcji in (select id_akcji from t_akcje where id_grupy_akcji_2 in {id_group_two})
                group by grupa_akcji_3, grupa_akcji_2,kod_akcji, miesiac'''
    # todo sql do przerobki
    if refresh == 'True':
        sql = f'''select grupa_akcji_3, grupa_akcji_2,kod_akcji, sum(kwota) as suma_wplat, count(tr.id_transakcji)
                 as liczba_wplat {extra} from public.t_aktywnosci_korespondentow tak
                left outer join public.t_transakcje tr
                on tr.id_transakcji = tak.id_transakcji
                left outer join t_akcje ta
                on ta.id_akcji=tak.id_akcji
                left outer join public.t_grupy_akcji_2 t on ta.id_grupy_akcji_2 = t.id_grupy_akcji_2
                left outer join public.t_grupy_akcji_3 a on ta.id_grupy_akcji_3 = a.id_grupy_akcji_3

                where tak.id_akcji in ( select id_akcji from t_akcje where  id_grupy_akcji_2 in {id_group_two} and t_akcje.id_grupy_akcji_3 !=7)
                group by --rok_i_mailing, 
                grupa_akcji_3,grupa_akcji_2, kod_akcji{extra_group}'''
        to_insert = pd.read_sql_query(sql, con)

        sql2 = f'''select distinct kod_akcji, sum(koszt_calkowity) as koszt_calkowity, sum(naklad_calkowity) as naklad_calkowity
         from v_akcje_naklad_koszt_calkowity vankc
            left outer join t_akcje ta on vankc.id_akcji = ta.id_akcji
            left outer join t_grupy_akcji_2 t on ta.id_grupy_akcji_2 = t.id_grupy_akcji_2
            left outer join t_grupy_akcji_3 a on ta.id_grupy_akcji_3 = a.id_grupy_akcji_3
            where vankc.id_akcji in (select id_akcji from t_akcje where id_grupy_akcji_2 in {id_group_two} and t_akcje.id_grupy_akcji_3 !=7)
            group by kod_akcji

                '''
        to_insert_2 = pd.read_sql_query(sql2, con)
        to_insert = pd.merge(to_insert, to_insert_2, how='left', on='kod_akcji')

        if type == 'address':
            to_insert['pozyskano'] = 0
            to_insert = change_types_of_columns(to_insert)
            to_insert.to_sql('dash_ma_data', engine, if_exists='replace', schema='raporty', index=False)
            print('dodano do bazy danych dane dla dashboard adresowy')

        else:
            extra_data = pd.read_sql_query(f'''select distinct k.kod_akcji, laczna_suma_wplat, laczny_koszt_utrzymania from v_akcja_dodania_korespondenta2 k
left outer join (select kod_akcji,  sum(kwota) as laczna_suma_wplat from t_transakcje tr
    left outer join v_akcja_dodania_korespondenta vadk on tr.id_korespondenta = vadk.id_korespondenta
    group by kod_akcji) tr
on tr.kod_akcji = k.kod_akcji
left outer join (select dod.kod_akcji,  sum(koszt) laczny_koszt_utrzymania
from v_koszt_korespondenta_w_akcjach_z_szczegolowa vkkwazs
    left outer join v_akcja_dodania_korespondenta2 dod on dod.id_korespondenta = vkkwazs.id_korespondenta
    group by dod.kod_akcji)koszt
on koszt.kod_akcji = k.kod_akcji''', con)
            to_insert = pd.merge(to_insert, extra_data, how='left', on='kod_akcji')
            new_people_sql = ''' select kod_akcji ,count(id_korespondenta) as pozyskano
                    from v_akcja_dodania_korespondenta2
                    group by kod_akcji'''
            new_people = pd.read_sql_query(new_people_sql, con)
            to_insert = pd.merge(to_insert, new_people, how='left', on='kod_akcji')
            pay_new_people = f'''select ta.kod_akcji, sum(kwota) as suma_wplat_nowi, count(tr.id_transakcji)
                 as liczba_wplat_nowi from public.t_aktywnosci_korespondentow tak
                left outer join public.t_transakcje tr
                on tr.id_transakcji = tak.id_transakcji
                left outer join t_akcje ta
                on ta.id_akcji=tak.id_akcji
                left outer join public.t_grupy_akcji_2 t on ta.id_grupy_akcji_2 = t.id_grupy_akcji_2
                left outer join public.t_grupy_akcji_3 a on ta.id_grupy_akcji_3 = a.id_grupy_akcji_3
left outer join v_akcja_dodania_korespondenta2 v on tak.id_korespondenta = v.id_korespondenta

                where tak.id_akcji in ( select id_akcji from t_akcje where  id_grupy_akcji_2 in {id_group_two} and t_akcje.id_grupy_akcji_3 !=7)
and ta.kod_akcji =v.kod_akcji
group by  ta.kod_akcji'''
            pay_new_people = pd.read_sql_query(pay_new_people, con)
            to_insert = pd.merge(to_insert, pay_new_people, how='left', on='kod_akcji')
            gift = pd.read_sql_query('''select kod_akcji, fmm.name as OBIECYWANY_GIFT, typ.rodzaj AS RODZAJ_GIFTU from t_akcje
    left outer join fsaps_campaign_subaction fcs
on fcs.name = t_akcje.kod_akcji
left outer join fsaps_campaign_action fca on fcs.action_id = fca.id
left outer join fsaps_campaign_main_action fcma on fca.action_main_id = fcma.id
left outer join fsaps_campaign_campaign fcc on fcma.campaign_id = fcc.id
left outer join fsaps_order_order foo on fcc.id = foo.campaign_id
left outer join fsaps_material_material fmm on foo.material_id = fmm.id
left outer join (select material_id, value AS rodzaj from fsaps_material_parameter where utility_parameter_name_id=1) typ
on typ.material_id=fmm.id
where id_grupy_akcji_1=22
ORDER BY ID_AKCJI DESC
''', con)
            to_insert = pd.merge(to_insert, gift, how='left', on='kod_akcji')

            # dodaje ile osob jest dalej aktywnych pozsyaknych dalej z tych subakcji
            sql = '''select fdagt.text as grupa_akcji_2, f.text as grupa_akcji_3 from fsaps_campaign_campaign
            left outer join fsaps_dictionary_action_group_two fdagt on fsaps_campaign_campaign.action_group_two_id = fdagt.id
            left outer join fsaps_dictionary_action_group_three f on fsaps_campaign_campaign.action_group_three_id = f.id
            where date_from is not null
            and fsaps_campaign_campaign.action_group_two_id is not null and fsaps_campaign_campaign.action_group_three_id is not null
            and fsaps_campaign_campaign.action_group_one_id = 23 and fsaps_campaign_campaign.action_group_two_id in (9,10,11,12)
            order by date_from desc limit 1'''
            data = pd.read_sql_query(sql, con)
            default_camp = data['grupa_akcji_2'].iloc[0]
            default_year = str(data['grupa_akcji_3'].iloc[0])
            sql = f'''select kod_akcji, count(id_korespondenta) as obecnie_aktywnych from v_akcja_dodania_korespondenta2
where id_korespondenta in (select id_korespondenta
                           from t_akcje_korespondenci where id_akcji in (
                               select id_akcji from t_akcje where id_grupy_akcji_2 in (
                                   select id_grupy_akcji_2 from t_grupy_akcji_2 where grupa_akcji_2 = '{default_camp}'
                                   ) AND  id_grupy_akcji_3 in (
                                   select id_grupy_akcji_3 from t_grupy_akcji_3 where grupa_akcji_3 = '{default_year}'
                                   )
    )
)
group by kod_akcji'''
            data = pd.read_sql_query(sql, con)
            to_insert = pd.merge(to_insert, data, how='left', on='kod_akcji')
            to_insert = change_types_of_columns(to_insert)
            to_insert.to_sql('dash_db_data', engine, if_exists='replace', schema='raporty', index=False)
            print('dodano do bazy danych dane dla dashboard bezadresowy')
    if type == 'address':
        sql = f'''select * from raporty.dash_ma_data'''
    else:
        sql = f'''select * from raporty.dash_db_data'''
    to_return = pd.read_sql_query(sql, con)
    to_return['grupa_akcji_3'] = to_return['grupa_akcji_3'].astype(int)

    return to_return


def download_increase_data(con, refresh, engine):
    if refresh == 'True':
        # todo sql do przerobki
        sql = '''select id_grupy_akcji_2, ta.id_grupy_akcji_3, data, gr3.grupa_akcji_3 from t_akcje_korespondenci tak
         left outer join t_akcje ta 
         on ta.id_akcji = tak.id_akcji
         left outer join t_grupy_akcji_3 gr3
         on gr3.id_grupy_akcji_3 = ta.id_grupy_akcji_3
         where id_grupy_akcji_2 in (9,10,11,12)
         order by data desc limit 1'''
        data = pd.read_sql_query(sql, con)
        id_gr2 = data['id_grupy_akcji_2'].iloc[0]
        id_gr3 = data['id_grupy_akcji_3'].iloc[0]
        rok = data['grupa_akcji_3'].iloc[0]
        sql = f'''select date_part('year', adod.data) as rok_dodania, grupa_akcji_1, grupa_akcji_2, kod_akcji,
        case when date_part('month', adod.data)<10 then '0'||date_part('month', adod.data)::text
        else date_part('month', adod.data)::text end as miesiac_dodania, mailingi, wpłata, count(adod.id_korespondenta) as ilosc
        from v_akcja_dodania_korespondenta2 adod
        left outer join (select id_korespondenta, 'dalej w mailingach'::text as mailingi from t_akcje_korespondenci where id_akcji in (
        select id_akcji from t_akcje where id_grupy_akcji_2 = {id_gr2} and id_grupy_akcji_3 = {id_gr3})) mailing
        on mailing.id_korespondenta = adod.id_korespondenta
        left outer join (select distinct id_korespondenta, 'wpłata' as wpłata from t_transakcje where data_wplywu_srodkow
        between ({rok}::text||'-01-01')::date and ({rok}::text||'-12-31')::date) wp
        on wp.id_korespondenta = adod.id_korespondenta
        group by rok_dodania, grupa_akcji_1, grupa_akcji_2,kod_akcji, miesiac_dodania, mailingi, wpłata'''
        to_insert = pd.read_sql_query(sql, con)
        to_insert['mailingi'].fillna('nie bierze udziału', inplace=True)
        to_insert['wpłata'].fillna('nie wpłacił', inplace=True)
        to_insert = change_types_of_columns(to_insert)
        to_insert.to_sql('dash_increase_data', engine, if_exists='replace', schema='raporty', index=False)
        print('dodano do bazy danych dane dla dashboard przyrost')
    to_return = pd.read_sql_query('select * from raporty.dash_increase_data', con)
    return to_return
