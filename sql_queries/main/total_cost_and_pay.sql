select subaction as kod_akcji, sum(laczna_suma_wplat) as laczna_suma_wplat,
       sum(laczny_koszt_utrzymania) as laczny_koszt_utrzymania from (select foo2.id as id_korespondenta, sourse_id, fcs.name as subaction, date::date, fdago.text as grupa_akcji_1_new,
       case when fdagt.text is not null then fdagt.text else fdagt2.text end as grupa_akcji_2_new,
t.text as grupa_akcji_3_new
from (select id, sourse_id, case when order_sub_id is not null then order_sub_id
    when int_sub_id is not null then int_sub_id
    when  apli_sub_id is not null then apli_sub_id
    when pol_sub_id is not null then pol_sub_id
    when enstr_sub_id is not null then enstr_sub_id
else 0 end as subaction, date from (
select fcc.id ,fccs.id as sourse_id, fooa.subaction_id as order_sub_id, fiia.subaction_id as int_sub_id,
       faa.subaction_id as apli_sub_id, fppa.subaction_id as pol_sub_id,
       fea.subaction_id as enstr_sub_id, fccs.date
from fsaps_correspondent_correspondent fcc
left outer join fsaps_correspondent_correspondent_source fccs on fcc.source_id = fccs.id
left outer join fsaps_order_order_answer fooa on fccs.order_answer_id = fooa.id
left outer join fsaps_intention_intention_answer fiia on fccs.intention_answer_id = fiia.id
left outer join fsaps_application_application faa on fccs.application_id = faa.id
left outer join fsaps_poll_poll_answer fppa on fccs.poll_answer_id = fppa.id
left outer join fsaps_entrustment_acts fea on fccs.entrustment_act_id = fea.id)foo)foo2
left outer join fsaps_campaign_subaction fcs on fcs.id = foo2.subaction
left outer join fsaps_campaign_action fca on fcs.action_id = fca.id
left outer join fsaps_campaign_main_action fcma on fca.action_main_id = fcma.id
left outer join fsaps_campaign_campaign f on fcma.campaign_id = f.id
left outer join fsaps_dictionary_action_group_one fdago on f.action_group_one_id = fdago.id
left outer join fsaps_dictionary_action_group_two fdagt on f.action_group_two_id = fdagt.id
left outer join fsaps_dictionary_action_group_two fdagt2 on fcma.action_group_two_id = fdagt2.id
left outer join fsaps_dictionary_action_group_three t on f.action_group_three_id = t.id
           ) foo3
left outer join (select correspondent_id, sum(amount) as laczna_suma_wplat from fsaps_payment_payment
    group by correspondent_id) pay
on foo3.id_korespondenta = pay.correspondent_id
left outer join (select fcp.correspondent_id, round(sum((fcc.real_cost::float8/1000) * fcc.number)::numeric,
     3)  as laczny_koszt_utrzymania
from (select subaction_id, correspondent_id
     from fsaps_campaign_person ) fcp
left outer join fsaps_campaign_cost fcc on fcp.subaction_id = fcc.subaction_id
left outer join fsaps_campaign_subaction fcs on fcp.subaction_id = fcs.id
    group by fcp.correspondent_id) cost
on foo3.id_korespondenta = cost.correspondent_id
group by kod_akcji
