select correspondent_id,
       fiia.ordered_at                     as data_zamowienia,
       date_part('month', fiia.ordered_at) as miesiac_zamowienia,
       date_part('year', fiia.ordered_at)  as rok_zamowienia,
       fii.party_date as data_wezwania,
       date_part('month', fii.party_date) as miesiac_wezwania,
       date_part('year', fii.party_date)  as rok_wezwania,
       fdit.text                           as patron,
       fdago.text                          as grupa_akcji_1,
       case
           when fdagt.text is null then fdagt2.text
           else fdagt.text
           end                                grupa_akcji_2,
       fdagt3.text                         as grupa_akcji_3,
       fcma.name,
       fcs.name                            as kod_akcji,
       1                                   as intencja


from fsaps_intention_intention_answer fiia
         left outer join fsaps_intention_intention fii
                         on fiia.intention_id = fii.id
         left outer join fsaps_dictionary_intention_type fdit
                         on fii.intention_type_id = fdit.id
         left outer join fsaps_campaign_subaction fcs
                         on fiia.subaction_id = fcs.id
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
where intention_type_id <= 22
order by correspondent_id, patron