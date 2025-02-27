select fcs.name as kod_ackji, sum(fpp.amount) as suma_wplat_nowi, count(fpp.id) as liczba_wplat_nowi
from fsaps_order_order_answer fooa
         left outer join fsaps_campaign_subaction fcs
                         on fooa.subaction_id = fcs.id
         left outer join fsaps_payment_payment fpp
                         on fooa.payment_id = fpp.id
         left outer join fsaps_v_zrodlo_pozyskania_darczyncy fvzpd
                         on fooa.correspondent_id = fvzpd.correspondent_id
where fvzpd.kod_akcji = fcs.name
and fvzpd.grupa_akcji_1 in ('DRUKI BEZADRESOWE', 'EVENT')
group by kod_ackji