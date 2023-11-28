select id as id_korespondenta, grupa_akcji_1, grupa_akcji_2, grupa_akcji_3, data_pozyskania as data_dodania,
       last_mailing, date_part('year', data_pozyskania)
from fsaps_correspondent_correspondent fcc
left outer join fsaps_v_zrodlo_pozyskania_darczyncy fvzpd
on fcc.id = fvzpd.correspondent_id
left outer join (
        select distinct correspondent_id , True as last_mailing from fsaps_campaign_person
                                where subaction_id in
                                      (select id from fsaps_campaign_subaction where action_id in(
                                          select id from fsaps_campaign_action where action_main_id in (
                                              select id from fsaps_campaign_main_action where campaign_id in (
                                                  select id from fsaps_campaign_campaign where id in (
                                                      select id from fsaps_campaign_campaign
                                                                where action_group_two_id in (9,10,11,12)
                                                                order by date_from desc
                                                                limit 1
                                                      )
                                              ))
                                          )  ))mailing
        on mailing.correspondent_id = fcc.id