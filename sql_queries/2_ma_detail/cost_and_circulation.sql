select grupa_akcji_3, grupa_akcji_2, sum(koszt) as koszt, sum(naklad) as naklad, 1 as dzien_po_mailingu from (
select  fdagt2.text as grupa_akcji_3, fdagt.text as grupa_akcji_2, round(sum((fcc.real_cost::float8/1000) * fcc.number)::numeric,
     3) * ilosc as koszt, ilosc as naklad
from (select subaction_id, count(correspondent_id) as ilosc
     from fsaps_campaign_person group by subaction_id) fcp
left outer join fsaps_campaign_cost fcc on fcp.subaction_id = fcc.subaction_id
left outer join fsaps_campaign_subaction fcs on fcp.subaction_id = fcs.id
    left outer join fsaps_campaign_action fca
    on fcs.action_id = fca.id
    left outer join fsaps_campaign_main_action fcma
    on fca.action_main_id = fcma.id
    left outer join fsaps_campaign_campaign fcc2
    on fcma.campaign_id = fcc2.id
    left outer join fsaps_dictionary_action_group_two fdagt
on fcc2.action_group_two_id = fdagt.id
left outer join fsaps_dictionary_action_group_three fdagt2
on fcc2.action_group_three_id = fdagt2.id
group by  grupa_akcji_3, grupa_akcji_2, ilosc)foo
group by grupa_akcji_3, grupa_akcji_2
