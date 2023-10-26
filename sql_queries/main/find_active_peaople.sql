select kod_akcji, count(correspondent_id) as obecnie_aktywnych from fsaps_v_zrodlo_pozyskania_darczyncy
where correspondent_id in (select correspondent_id from fsaps_campaign_person where subaction_id in (
    select id from fsaps_campaign_subaction where action_id in (
        select id from fsaps_campaign_action where action_main_id in (
            select id from fsaps_campaign_main_action where campaign_id in (
                select id from fsaps_campaign_campaign where action_group_two_id = 11
                and action_group_three_id = 17
                )
            )
        )
    ))
group by kod_akcji