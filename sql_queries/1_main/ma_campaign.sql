select fdagt.text as grupa_akcji_3, fdagt2.text as grupa_akcji_2, fcs.name as kod_akcji,
sum(fpp.amount) as suma_wplat, count(fpp.amount) as liczba_wplat
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
on fcc.action_group_two_id = fdagt2.id
left outer join fsaps_payment_payment fpp
on fooa.payment_id = fpp.id
where fcc.action_group_two_id in (9,10,11,12,24,67,100) and fcc.action_group_one_id = 23
group by grupa_akcji_3, grupa_akcji_2, kod_akcji
order by kod_akcji