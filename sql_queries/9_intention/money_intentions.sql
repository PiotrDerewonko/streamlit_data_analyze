select distinct fooa.correspondent_id,
                ordered_at                          as data,
                date_part('month', fooa.ordered_at) as miesiac_zamowienia,
                date_part('year', fooa.ordered_at)  as rok_zamowienia,
                ''                                  as patron,
                fdago.text                          as grupa_akcji_1,
                case
                    when fdagt.text is null then fdagt2.text
                    else fdagt.text
                    end                                grupa_akcji_2,
                fdagt3.text                         as grupa_akcji_3,
                fcs.name                            as kod_akcji,
                fpp.amount                          as kwota
from fsaps_order_order_answer fooa
         left outer join fsaps_order_order foo
                         on fooa.order_id = foo.id
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

