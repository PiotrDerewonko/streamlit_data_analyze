select date_part('year', data_pozyskania)                     as rok_dodania,
       grupa_akcji_1,
       grupa_akcji_2,
       grupa_akcji_3,
       kod_akcji,
       case
           when date_part('month', data_pozyskania) < 10 then '0' || date_part('month', data_pozyskania)::text
           else date_part('month', data_pozyskania)::text end as miesiac_dodania,
       mailingi,
       wpłata,
       count(fvzpd.correspondent_id)                          as ilosc
from fsaps_v_zrodlo_pozyskania_darczyncy fvzpd
         left outer join (select distinct correspondent_id, 'dalej w mailingach'::text as mailingi
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
                                                                                                          where text = '{default_year}')))))) mailing
                         on fvzpd.correspondent_id = mailing.correspondent_id
         left outer join (select distinct correspondent_id, 'wpłata' as wpłata
                          from fsaps_payment_payment
                          where date between ('{default_year}'::text || '-01-01')::date and ('{default_year}'::text || '-12-31')::date) pay
                         on fvzpd.correspondent_id = pay.correspondent_id
group by rok_dodania, grupa_akcji_1, grupa_akcji_2, grupa_akcji_3, kod_akcji, miesiac_dodania, mailingi, wpłata