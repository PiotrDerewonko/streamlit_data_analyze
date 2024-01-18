select fdagt2.text as grupa_akcji_3, fdagt.text as grupa_akcji_2, sum(fpp.amount) as suma_wplat,
       count(fpp.correspondent_id) as liczba_wplat,
       case when typ is null then 'nowy' else typ::text end as nowy_stary, days.dzien_po_mailingu::int
from fsaps_payment_payment fpp
left outer join fsaps_order_order_answer fooa
on fooa.payment_id = fpp.id
left outer join fsaps_campaign_subaction fcs on fooa.subaction_id = fcs.id
left outer join fsaps_campaign_action fca on fcs.action_id = fca.id
left outer join fsaps_campaign_main_action fcma on fca.action_main_id = fcma.id
left outer join fsaps_campaign_campaign fcc on fcma.campaign_id = fcc.id
left outer join fsaps_dictionary_action_group_two fdagt on fcc.action_group_two_id = fdagt.id
left outer join fsaps_dictionary_action_group_three fdagt2 on fcc.action_group_three_id = fdagt2.id
left outer join (select distinct correspondent_id, 'stary' as typ
                 from fsaps_campaign_person where subaction_id in
                                                  (select id from fsaps_campaign_subaction where action_id in (
                                                  select id from fsaps_campaign_action where action_main_id in (
                                                  select id from fsaps_campaign_main_action where campaign_id in (
                                                  select id from fsaps_campaign_campaign where action_group_two_id = #A#
                                                                                           and action_group_three_id = #C#))))) old
                        on old.correspondent_id = fpp.correspondent_id
left outer join raporty.t_dni_po_nadaniu_mailingow days
        on days.id_grupy_akcji_3 = fcc.action_group_three_id and days.id_grupy_akcji_2 = fcc.action_group_two_id
and days.data_wplywu_srodkow = fpp.date
where  fcc.action_group_two_id = #A# and fcc.action_group_three_id=#B#
group by grupa_akcji_3, grupa_akcji_2,nowy_stary, days.dzien_po_mailingu
