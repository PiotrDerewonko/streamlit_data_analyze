select fcc.id                                   as id_korespondenta,
       subaction,
       case
           when rodzaj_materialu_pozyskania is null then
               'brak'
           else rodzaj_materialu_pozyskania end as rodzaj_materialu_pozyskania,
       case
           when material_pozyskania is null
               then 'brak'
           else material_pozyskania end         as material_pozyskania,
       nazwa_kampanii_pozyskania
from fsaps_correspondent_correspondent fcc
         left outer join (select *
                          from (select foo2.id                                                               as id_korespondenta,
                                       sourse_id,
                                       subaction,
                                       date::date,
                                       fdago.text                                                            as grupa_akcji_1_new,
                                       case when fdagt.text is not null then fdagt.text else fdagt2.text end as grupa_akcji_2_new,
                                       t.text                                                                as grupa_akcji_3_new,
                                       f.id                                                                  as campaign_id,
                                       f.topic                                                               as nazwa_kampanii_pozyskania
                                from (select id,
                                             sourse_id,
                                             case
                                                 when order_sub_id is not null then order_sub_id
                                                 when int_sub_id is not null then int_sub_id
                                                 when apli_sub_id is not null then apli_sub_id
                                                 when pol_sub_id is not null then pol_sub_id
                                                 when enstr_sub_id is not null then enstr_sub_id
                                                 else 0 end as subaction,
                                             date
                                      from (select fcc.id,
                                                   fccs.id           as sourse_id,
                                                   fooa.subaction_id as order_sub_id,
                                                   fiia.subaction_id as int_sub_id,
                                                   faa.subaction_id  as apli_sub_id,
                                                   fppa.subaction_id as pol_sub_id,
                                                   fea.subaction_id  as enstr_sub_id,
                                                   fccs.date
                                            from fsaps_correspondent_correspondent fcc
                                                     left outer join fsaps_correspondent_correspondent_source fccs on fcc.source_id = fccs.id
                                                     left outer join fsaps_order_order_answer fooa on fccs.order_answer_id = fooa.id
                                                     left outer join fsaps_intention_intention_answer fiia
                                                                     on fccs.intention_answer_id = fiia.id
                                                     left outer join fsaps_application_application faa on fccs.application_id = faa.id
                                                     left outer join fsaps_poll_poll_answer fppa on fccs.poll_answer_id = fppa.id
                                                     left outer join fsaps_entrustment_acts fea on fccs.entrustment_act_id = fea.id) foo) foo2
                                         left outer join fsaps_campaign_subaction fcs on fcs.id = foo2.subaction
                                         left outer join fsaps_campaign_action fca on fcs.action_id = fca.id
                                         left outer join fsaps_campaign_main_action fcma on fca.action_main_id = fcma.id
                                         left outer join fsaps_campaign_campaign f on fcma.campaign_id = f.id
                                         left outer join fsaps_dictionary_action_group_one fdago
                                                         on f.action_group_one_id = fdago.id
                                         left outer join fsaps_dictionary_action_group_two fdagt
                                                         on f.action_group_two_id = fdagt.id
                                         left outer join fsaps_dictionary_action_group_two fdagt2
                                                         on fcma.action_group_two_id = fdagt2.id
                                         left outer join fsaps_dictionary_action_group_three t on f.action_group_three_id = t.id) foo3) sub
                         on sub.id_korespondenta = fcc.id
         left outer join (select distinct campaign_id,
                                          fmp.value as rodzaj_materialu_pozyskania,
                                          fmm.name  as material_pozyskania
                          from fsaps_order_order foo
                                   left outer join fsaps_material_material fmm on foo.material_id = fmm.id
                                   left outer join fsaps_material_parameter fmp on fmm.id = fmp.material_id
                          where utility_parameter_name_id = 1) mat
                         on mat.campaign_id = sub.campaign_id