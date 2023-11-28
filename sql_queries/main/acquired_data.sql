select date_part('year', adod.data_pozyskania)                     as rok_dodania,
       grupa_akcji_1,
       grupa_akcji_2,
       kod_akcji,
       case
           when date_part('month', adod.data_pozyskania) < 10 then '0' || date_part('month', adod.data_pozyskania)::text
           else date_part('month', adod.data_pozyskania)::text end as miesiac_dodania,
       mailingi,
       wpłata::text,
       count(adod.correspondent_id)                                as ilosc
from fsaps_v_zrodlo_pozyskania_darczyncy adod
         left outer join (select distinct correspondent_id, 'dalej w mailingach'::text as mailingi
                          from fsaps_campaign_person
                          where subaction_id in
                                (select id
                                 from fsaps_campaign_subaction
                                 where action_id in (select id
                                                     from fsaps_campaign_action
                                                     where action_main_id in (select id
                                                                              from fsaps_campaign_main_action
                                                                              where campaign_id in (select id
                                                                                                    from fsaps_campaign_campaign
                                                                                                    where id in
                                                                                                          (select id
                                                                                                           from fsaps_campaign_campaign
                                                                                                           where action_group_two_id in (9, 10, 11, 12)
                                                                                                           order by date_from desc
                                                                                                           limit 1)))))) mailing
                         on mailing.correspondent_id = adod.correspondent_id
         left outer join (select distinct correspondent_id, 'wpłata'::text as wpłata
                          from fsaps_payment_payment
                          where date between
                                    (date_part('year', now())::text || '-01-01')::date and
                                    (date_part('year', now())::text || '-12-31')::date) wpl
                         on wpl.correspondent_id = adod.correspondent_id

group by rok_dodania, grupa_akcji_1, grupa_akcji_2, kod_akcji, miesiac_dodania, mailingi, wpłata