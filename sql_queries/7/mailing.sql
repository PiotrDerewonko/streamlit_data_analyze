select distinct correspondent_id as id_korespondenta
from fsaps_campaign_person
where subaction_id in (select id
                       from fsaps_campaign_subaction
                       where action_id in (select id
                                           from fsaps_campaign_action
                                           where action_main_id in (select id
                                                                    from fsaps_campaign_main_action
                                                                    where campaign_id in (#KAMPANIA#))))