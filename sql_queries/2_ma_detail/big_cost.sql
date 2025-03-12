select fcp.correspondent_id as id_korespondenta,
       fcs.id               as id_akcji,
       fdagt2.text          as grupa_akcji_3,
       fdagt.text           as grupa_akcji_2,
       koszt_drukow,
       koszt_personalizacji,
       koszt_giftow,
       koszt_konfekcjonowania,
       koszt_wysylki_na_polske_bez_warszawy,
       koszt_wysylki_na_warszawe,
       koszt_wysylki_zagranica
from fsaps_campaign_person as fcp
         left outer join fsaps_campaign_subaction fcs
                         on fcp.subaction_id = fcs.id
         left outer join fsaps_campaign_action fca
                         on fcs.action_id = fca.id
         left outer join fsaps_campaign_main_action fcma
                         on fca.action_main_id = fcma.id
         left outer join fsaps_campaign_campaign fcc
                         on fcma.campaign_id = fcc.id
         left outer join fsaps_dictionary_action_group_two fdagt
                         on fcc.action_group_two_id = fdagt.id
         left outer join fsaps_dictionary_action_group_three fdagt2
                         on fcc.action_group_three_id = fdagt2.id
         left outer join (select fcc2.subaction_id,
                                 round(sum((real_cost::float8 / 1000) * fcc2.number)::numeric, 3) as koszt_drukow
                          from fsaps_campaign_cost fcc2
                                   left outer join fsaps_campaign_material fcm
                                                   on fcc2.id = fcm.cost_id
                                   left outer join fsaps_material_material fmm
                                                   on fcm.material_id = fmm.id
                          where fmm.type_id in
                                (4, 1, 2, 6, 9, 14, 15, 16, 20, 22, 23, 24, 25, 26, 13, 11, 10, 3, 28, 29, 21, 23,
                                 33)
                          group by fcc2.subaction_id) druki
                         on fcp.subaction_id = druki.subaction_id
         left outer join (select fcc2.subaction_id,
                                 round(sum((real_cost::float8 / 1000) * fcc2.number)::numeric, 3) as koszt_personalizacji
                          from fsaps_campaign_cost fcc2
                                   left outer join fsaps_campaign_material fcm
                                                   on fcc2.id = fcm.cost_id
                                   left outer join fsaps_material_material fmm
                                                   on fcm.material_id = fmm.id
                          where fmm.type_id in
                                (34)
                          group by fcc2.subaction_id) perso
                         on fcp.subaction_id = perso.subaction_id
         left outer join (select fcc2.subaction_id,
                                 round(sum((real_cost::float8 / 1000) * fcc2.number)::numeric, 3) as koszt_giftow
                          from fsaps_campaign_cost fcc2
                                   left outer join fsaps_campaign_material fcm
                                                   on fcc2.id = fcm.cost_id
                                   left outer join fsaps_material_material fmm
                                                   on fcm.material_id = fmm.id
                          where fmm.type_id in
                                (5, 7, 8, 12, 19, 27, 32, 30, 31)
                          group by fcc2.subaction_id) gifty
                         on fcp.subaction_id = gifty.subaction_id
         left outer join (select subaction_id,
                                 round(((real_cost::float8 / 1000) * number)::numeric, 3) as
                                     koszt_konfekcjonowania
                          from fsaps_campaign_cost
                          where name = 'koszt_konfekcjonowania') konfekcja
                         on fcp.subaction_id = konfekcja.subaction_id
         left outer join (select subaction_id,
                                 round(((real_cost::float8 / 1000) * number)::numeric, 3) as
                                     koszt_wysylki_na_polske_bez_warszawy
                          from fsaps_campaign_cost
                          where name = 'koszt_wysylki_polska') polska_bez_warszawy
                         on fcp.subaction_id = polska_bez_warszawy.subaction_id
         left outer join (select subaction_id,
                                 round(((real_cost::float8 / 1000) * number)::numeric, 3) as
                                     koszt_wysylki_na_warszawe
                          from fsaps_campaign_cost
                          where name = 'koszt_wysylki_na_warszawe') warszawa
                         on fcp.subaction_id = warszawa.subaction_id
         left outer join (select subaction_id,
                                 round(((real_cost::float8 / 1000) * number)::numeric, 3) as
                                     koszt_wysylki_zagranica
                          from fsaps_campaign_cost
                          where name = 'koszt_wysylki_zagranica') zagranica
                         on fcp.subaction_id = zagranica.subaction_id

where fcc.action_group_two_id in (9, 10, 11, 12, 24, 67, 101)
order by id_korespondenta, grupa_akcji_3, grupa_akcji_2
