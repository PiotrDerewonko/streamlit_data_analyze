select correspondent_id         as id_korespondenta,
       fcs.name                 as kod_akcji,
       fdago.text               as grupa_akcji_1_wysylki,
       fdagt.text                  asgrupa_akcji_2_wysylki,
       fdagt2.text              as grupa_akcji_3_wysylki,
       cost.koszt,
       1                        as naklad,
       takpog.nazwa_szczegolowa as powod_otrzymania_giftu,
       row_number() over (partition by fcp.correspondent_id, fdagt.text,fdagt.text order by
           fcp.correspondent_id, fdagt.text, fdagt.text)
from fsaps_campaign_person fcp
         left outer join fsaps_campaign_subaction fcs
                         on fcp.subaction_id = fcs.id
         left outer join fsaps_campaign_action fca
                         on fcs.action_id = fca.id
         left outer join fsaps_campaign_main_action fcma
                         on fca.action_main_id = fcma.id
         left outer join fsaps_campaign_campaign fcc
                         on fcma.campaign_id = fcc.id
         left outer join fsaps_dictionary_action_group_one fdago
                         on fcc.action_group_one_id = fdago.id
         left outer join fsaps_dictionary_action_group_two fdagt
                         on fcc.action_group_two_id = fdagt.id
         left outer join fsaps_dictionary_action_group_three fdagt2
                         on fcc.action_group_three_id = fdagt2.id
         left outer join (select subaction_id, sum((real_cost::float8 / 1000) * number) as koszt
                          from fsaps_campaign_cost
                          group by subaction_id) cost
                         on fcp.subaction_id = cost.subaction_id
         left outer join t_akcje_korespondenci_powod_otrzymania_giftu takpog
                         on fcp.correspondent_id = takpog.id_korespondenta and
                            fcc.action_group_one_id = takpog.id_grupy_akcji_1 and
                            fcc.action_group_two_id = takpog.id_grupy_akcji_2 and
                            fcc.action_group_three_id = takpog.id_grupy_akcji_3

order by id_korespondenta


