select id as id_akcji, name as kod_akcji
from fsaps_campaign_subaction
where action_id in (select id
                    from fsaps_campaign_action
                    where action_main_id in (select id
                                             from fsaps_campaign_main_action
                                             where campaign_id in (select id
                                                                   from fsaps_campaign_campaign
                                                                   where action_group_three_id >= 8)
                                             and action_group_two_id in #A#))