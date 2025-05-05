select distinct fcs.id     as id_akcji,
                fcs.name   as kod_akcji,
                fdago.text as grupa_akcji_1,
                fdagt.text as grupa_akcji_2,
                fdagt2.text as grupa_akcji_3
from fsaps_campaign_subaction fcs
         left outer join fsaps_campaign_action fca
                         on fcs.action_id = fca.id
         left outer join fsaps_campaign_main_action fcma
                         on fca.action_main_id = fcma.id
         left outer join fsaps_campaign_campaign fcc
                         on fcma.campaign_id = fcc.id
         left outer join fsaps_dictionary_action_group_one fdago
                         on fcc.action_group_one_id = fdago.id
         left outer join fsaps_dictionary_action_group_two fdagt
                         on fcma.action_group_two_id = fdagt.id
         left outer join fsaps_dictionary_action_group_three fdagt2
                         on fcc.action_group_three_id = fdagt2.id