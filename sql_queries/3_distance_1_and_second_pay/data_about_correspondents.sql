select fvzpd.correspondent_id             as id_korespondenta,
       grupa_akcji_1,
       grupa_akcji_2,
       grupa_akcji_3,
       data_pozyskania                    as data_dodania,
       last_mailing.last_mailing,
       date_part('year', data_pozyskania) as rok_dodania,
       case
           when fccs.type = 'plural' then 'mnogie'
           when fccs.id in (6, 4, 10, 9, 16, 1) then 'mężczyźni'
           when fccs.id in (5, 2) then 'kobiety'
           when fccs.id in (11) then 'mnogie'
           else 'mnogie'
           end                            as plec,

       case
           when substring(kod_pocztowy, 1, 1)::int = 0 then 'warszawski'
           when substring(kod_pocztowy, 1, 1)::int = 1 then 'olsztyński'
           when substring(kod_pocztowy, 1, 1)::int = 2 then 'lubelski'
           when substring(kod_pocztowy, 1, 1)::int = 3 then 'krakowski'
           when substring(kod_pocztowy, 1, 1)::int = 4 then 'katowicki'
           when substring(kod_pocztowy, 1, 1)::int = 5 then 'wrocłąwski'
           when substring(kod_pocztowy, 1, 1)::int = 6 then 'poznański'
           when substring(kod_pocztowy, 1, 1)::int = 7 then 'szczeciński'
           when substring(kod_pocztowy, 1, 1)::int = 8 then 'gdański'
           when substring(kod_pocztowy, 1, 1)::int = 9 then 'łódzki'
           else 'puste'
           end                            as okreg_pocztowy,
       case
           when adr.id_korespondenta is not null then
               'poprawny_adres'
           else 'niepoprawny' end         as good_address


from fsaps_v_zrodlo_pozyskania_darczyncy fvzpd
         left outer join (select distinct correspondent_id, True as last_mailing
                          from fsaps_campaign_person
                          where subaction_id in (select id
                                                 from fsaps_campaign_subaction
                                                 where action_id in (select id
                                                                     from fsaps_campaign_action
                                                                     where action_main_id in (select id
                                                                                              from fsaps_campaign_main_action
                                                                                              where campaign_id in
                                                                                                    (select id
                                                                                                     from fsaps_campaign_campaign
                                                                                                     where
                                                                                                         action_group_two_id in
                                                                                                         (select id
                                                                                                          from fsaps_dictionary_action_group_two
                                                                                                          where text = '{default_camp}')
                                                                                                       and
                                                                                                         action_group_three_id in
                                                                                                         (select id
                                                                                                          from fsaps_dictionary_action_group_three
                                                                                                          where text = '{default_year}')))))) last_mailing
                         on fvzpd.correspondent_id = last_mailing.correspondent_id
         left outer join raporty.fsaps_v_adresy_do_mailingow adr
                         on fvzpd.correspondent_id = adr.id_korespondenta
         left outer join fsaps_correspondent_correspondent_salutation fccs
                         on adr.tytul = fccs.text



