select fpp.correspondent_id as id_korespondenta, fpp.amount as suma_wplat, fdagt.text as grupa_akcji_2_wplaty,
       fdagt2.text as grupa_akcji_3_wplaty
, poczta
from fsaps_payment_payment fpp
left outer join fsaps_order_order_answer fooa
on fooa.payment_id = fpp.id
left outer join fsaps_campaign_subaction fcs
on fooa.subaction_id = fcs.id
left outer join fsaps_campaign_action fca on fcs.action_id = fca.id
left outer join fsaps_campaign_main_action fcma on fca.action_main_id = fcma.id
left outer join fsaps_campaign_campaign fcc on fcma.campaign_id = fcc.id
left outer join fsaps_dictionary_action_group_two fdagt on fcc.action_group_two_id = fdagt.id
left outer join fsaps_dictionary_action_group_three fdagt2 on fcc.action_group_three_id = fdagt2.id
left outer join raporty.t_dni_po_nadaniu_mailingow days
        on days.id_grupy_akcji_3 = fcc.action_group_three_id and days.id_grupy_akcji_2 = fcc.action_group_two_id
and days.data_wplywu_srodkow = fpp.date
left outer join (select payment_id, case when source_line like '%od Bank Pocztowy S.A. w imieniu:%' or
                                              source_line like 'od Bank Pocztowy S.A. w imieniu:%'
                 then 'poczta' else 'pozostali' end as poczta from fsaps_payment_imported_payment) poczta
on fpp.id = poczta.payment_id
where fcc.action_group_two_id in (9,10,11,12,24,67,100)
order by id_korespondenta desc