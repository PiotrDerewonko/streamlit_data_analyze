select distinct fooa.correspondent_id,
                ordered_at                          as data_wpłaty,
                date_part('month', fooa.ordered_at) as miesiac_wpłaty,
                date_part('year', fooa.ordered_at)  as rok_wpłaty,
                fpp.amount                          as kwota,
                case
                    when fdit.text is null then 'Brak'
                    else fdit.text
                    end                             as patron,
                fdago.text                          as grupa_akcji_1_mailingu,
                case
                    when fdagt.text is null then fdagt2.text
                    else fdagt.text
                    end                                grupa_akcji_2_mailingu,
                fdagt3.text                         as grupa_akcji_3_mailingu,
                fcs.name                            as kod_akcji,
                fdit.text                           as typ_intencji

from fsaps_order_order_answer fooa
         left outer join fsaps_order_order foo
                         on fooa.order_id = foo.id
         left outer join fsaps_order_order_subaction foos
                         on fooa.order_id = foos.order_id and fooa.subaction_id = foos.subaction_id
         left outer join fsaps_intention_intention fii
                         on foos.intention_id = fii.id
         left outer join fsaps_dictionary_intention_type fdit
                         on fii.intention_type_id = fdit.id
         left outer join fsaps_payment_payment fpp
                         on fooa.payment_id = fpp.id
         left outer join fsaps_campaign_subaction fcs
                         on fooa.subaction_id = fcs.id
         left outer join fsaps_campaign_action fca
                         on fcs.action_id = fca.id
         left outer join (select * from fsaps_campaign_main_action where newly_acquired = False) fcma
                         on fca.action_main_id = fcma.id
         left outer join fsaps_campaign_campaign fcc
                         on fcma.campaign_id = fcc.id
         left outer join fsaps_dictionary_action_group_one fdago
                         on fcc.action_group_one_id = fdago.id
         left outer join fsaps_dictionary_action_group_two fdagt
                         on fcc.action_group_two_id = fdagt.id
         left outer join fsaps_dictionary_action_group_two fdagt2
                         on fcma.action_group_two_id = fdagt2.id
         left outer join fsaps_dictionary_action_group_three fdagt3
                         on fcc.action_group_three_id = fdagt3.id
where fdago.id = 36
order by typ_intencji

