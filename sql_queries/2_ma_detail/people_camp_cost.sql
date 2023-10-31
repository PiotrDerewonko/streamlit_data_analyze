select fcp.correspondent_id as id_korespondenta, fcs.name as kod_akcji_wysylki,
       fdagt.text as grupa_akcji_2_wysylki, f.text as grupa_akcji_3_wysylki ,
       new_cost as koszt,
       fooa.realization_reason as powod_otrzymania_giftu, row_number() over (partition by fcp.correspondent_id, fdagt.text, f.text
           order by fcp.correspondent_id, fdagt.text, f.text)

       from fsaps_campaign_person fcp
left outer join fsaps_campaign_subaction fcs on fcp.subaction_id = fcs.id
    left outer join fsaps_campaign_action fca
    on fcs.action_id = fca.id
    left outer join fsaps_campaign_main_action fcma
    on fca.action_main_id = fcma.id
    left outer join fsaps_campaign_campaign fcc
    on fcma.campaign_id = fcc.id
    left outer join fsaps_dictionary_action_group_two fdagt
on fcc.action_group_two_id = fdagt.id
           left outer join (select fcp.correspondent_id,  fcs.name as kod_akcji, round(sum((fcc.real_cost::float8/1000) * fcc.number)::numeric,
     3) * ilosc as new_cost, ilosc as naklad
from (select correspondent_id , subaction_id, count(correspondent_id) as ilosc
     from fsaps_campaign_person group by correspondent_id, subaction_id) fcp
left outer join fsaps_campaign_cost fcc on fcp.subaction_id = fcc.subaction_id
left outer join fsaps_campaign_subaction fcs on fcp.subaction_id = fcs.id
group by fcp.correspondent_id,  fcs.name, naklad) cost
           on fcp.correspondent_id = cost.correspondent_id and fcs.name = cost.kod_akcji
left outer join fsaps_dictionary_action_group_three f on fcc.action_group_three_id = f.id
left outer join fsaps_order_order_answer fooa on fcs.id = fooa.subaction_of_realization_id

where fcc.action_group_two_id in (9,10,11,12,24,67,100)


