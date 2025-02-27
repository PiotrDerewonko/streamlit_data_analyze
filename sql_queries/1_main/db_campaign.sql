select fdagt.text                as grupa_akcji_3,
       fdagt2.text               as grupa_akcji_2,
       fcs.name                  as kod_akcji,
       sum(fpp.amount)           as suma_wplat,
       count(fpp.amount)         as liczba_wplat,
       substring(fcs.name, 7, 2) as miesiac
from fsaps_order_order_answer fooa
         left outer join fsaps_campaign_subaction fcs
                         on fooa.subaction_id = fcs.id
         left outer join fsaps_campaign_action fca
                         on fcs.action_id = fca.id
         left outer join fsaps_campaign_main_action fcma
                         on fca.action_main_id = fcma.id
         left outer join fsaps_campaign_campaign fcc
                         on fcma.campaign_id = fcc.id
         left outer join fsaps_dictionary_action_group_three fdagt
                         on fcc.action_group_three_id = fdagt.id
         left outer join fsaps_dictionary_action_group_two fdagt2
                         on fcma.action_group_two_id = fdagt2.id
         left outer join fsaps_payment_payment fpp
                         on fooa.payment_id = fpp.id
where fcma.action_group_two_id in
      (1, 2, 5, 91, 93, 95, 96, 101, 102, 103, 104, 105, 117, 118, 119, 120, 121, 122, 123, 124, 125, 86, 126, 127, 128)
group by grupa_akcji_3, grupa_akcji_2, kod_akcji, miesiac
order by grupa_akcji_3 desc