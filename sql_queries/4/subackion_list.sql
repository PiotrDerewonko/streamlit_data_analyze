select fcs.name                                                          as kod_akcji,
       split_part(fcs.name, '_', 3)                                      as miesiac,
       fdago.text                                                        as grupa_akcji_1,
       case when fdagt.text is null then fdagt3.text else fdagt.text end as grupa_akcji_2,
       fdagt2.text                                                       as grupa_akcji_3
from fsaps_campaign_subaction fcs
         left outer join fsaps_campaign_action fca
                         on fca.id = fcs.action_id
         left outer join fsaps_campaign_main_action fcma
                         on fcma.id = fca.action_main_id
         left outer join fsaps_campaign_campaign fcc
                         on fcma.campaign_id = fcc.id
         left outer join fsaps_dictionary_action_group_one fdago
                         on fcc.action_group_one_id = fdago.id
         left outer join fsaps_dictionary_action_group_two fdagt
                         on fcc.action_group_two_id = fdagt.id
         left outer join fsaps_dictionary_action_group_three fdagt2
                         on fcc.action_group_three_id = fdagt2.id
         left outer join fsaps_dictionary_action_group_two fdagt3
                         on fcma.action_group_two_id = fdagt3.id
where fcc.action_group_one_id = 22
  and fcc.action_group_three_id >= 8
