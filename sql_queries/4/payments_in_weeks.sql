select grupa_akcji_3,
       grupa_akcji_2,
       kod_akcji,
       suma_wplat,
       pozyskano,
       row_number() over (partition by kod_akcji order by kod_akcji,rok, num_tygodnia) as numer_tygodnia
from (select fdagt3.text                 as grupa_akcji_3,
             case
                 when fcc.action_group_two_id is null
                     then fdagt2.text
                 else fdagt.text
                 end                     as grupa_akcji_2,
             fcs.name                    as kod_akcji,
             sum(fpp.amount)             as suma_wplat,
             date_part('week', fpp.date) as num_tygodnia,
             date_part('year', fpp.date) as rok,
             sum(pozyskani)              as pozyskano
      from fsaps_order_order_answer fooa
               left outer join fsaps_payment_payment fpp
                               on fooa.payment_id = fpp.id
               left outer join fsaps_campaign_subaction fcs
                               on fooa.subaction_id = fcs.id
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
               left outer join fsaps_dictionary_action_group_two fdagt2
                               on fcma.action_group_two_id = fdagt2.id
               left outer join fsaps_dictionary_action_group_three fdagt3
                               on fcc.action_group_three_id = fdagt3.id
               left outer join (select 1 as pozyskani, subaction, correspondent_id
                                from fsaps_v_zrodlo_pozyskania_darczyncy) poz
                               on fooa.subaction_id = poz.subaction and
                                  fooa.correspondent_id = poz.correspondent_id
      where fcc.action_group_one_id = 22
        and fcc.action_group_three_id >= 8
      group by grupa_akcji_3, grupa_akcji_2, kod_akcji, num_tygodnia, rok) foo
