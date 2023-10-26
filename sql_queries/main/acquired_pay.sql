select vzpd.kod_akcji, sum(fpp.amount) as suma_wplat_nowi, count(fpp.amount) as liczba_wplat_nowi
from fsaps_order_order_answer fooa
left outer join fsaps_campaign_subaction fcs on fooa.subaction_id = fcs.id
left outer join fsaps_v_zrodlo_pozyskania_darczyncy vzpd on fooa.correspondent_id = vzpd.correspondent_id
left outer join fsaps_payment_payment fpp on fooa.payment_id = fpp.id
left outer join fsaps_campaign_action fca on fcs.action_id = fca.id
left outer join fsaps_campaign_main_action fcma on fca.action_main_id = fcma.id
left outer join fsaps_campaign_campaign fcc on fcma.campaign_id = fcc.id
where fcc.action_group_one_id=22 and vzpd.kod_akcji = fcs.name
group by vzpd.kod_akcji

