select correspondent_id   as id_korespondenta
     , grupa_akcji_2      AS grupa_akcji_2_wysylki
     , grupa_akcji_3::int AS grupa_akcji_3_wysylki
     , case
           when
               jaka_karta_wtedy = 1 then 'NIEBIESKA'
           when jaka_karta_wtedy = 2 then 'SREBRNA'
           when jaka_karta_wtedy = 3 then 'ZŁOTA'
           else 'BRAK DANYCH'
    end                   as KARTA_NA_MAILING
from (select distinct fcp.correspondent_id,
                      fdagt.text        as grupa_akcji_2,
                      fdagt2.text       as grupa_akcji_3,
                      case
                          when fcc.date_from >=
                               wydanie_niebieskiej and
                               (fcc.date_from < wydanie_srebrnej or wydanie_srebrnej is null)
                              and (fcc.date_from < wydanie_zlotej or wydanie_zlotej is null)
                              then collor_cards_filtered.niebieska
                          when fcc.date_from >= wydanie_srebrnej and
                               (fcc.date_from < wydanie_zlotej or wydanie_zlotej is null)
                              then collor_cards_filtered.srebrna
                          when fcc.date_from >= wydanie_zlotej
                              then collor_cards_filtered.zlota
                          else null end as jaka_karta_wtedy
      from fsaps_campaign_person fcp
               left outer join fsaps_campaign_action fca
                               on fcp.action_id = fca.id
               left outer join fsaps_campaign_main_action fcma
                               on fca.action_main_id = fcma.id
               left outer join fsaps_campaign_campaign fcc
                               on fcma.campaign_id = fcc.id
               left outer join fsaps_dictionary_action_group_two fdagt on fcc.action_group_two_id = fdagt.id
               left outer join fsaps_dictionary_action_group_three fdagt2 on fcc.action_group_three_id = fdagt2.id
               left outer join (select correspondent_id,
                                       case
                                           when (wydanie_niebieskiej >= wydanie_srebrnej) or
                                                (wydanie_niebieskiej >= wydanie_zlotej)
                                               then null
                                           else wydanie_niebieskiej end as wydanie_niebieskiej,
                                       niebieska,
                                       case
                                           when wydanie_srebrnej >= wydanie_zlotej
                                               then null
                                           else wydanie_srebrnej end    as wydanie_srebrnej,
                                       srebrna,

                                       wydanie_zlotej,
                                       zlota
                                from (select distinct k.correspondent_id,
                                                      niebieska.wydanie_niebieskiej,
                                                      niebieska,
                                                      srebrna.wydanie_srebrnej,
                                                      srebrna,
                                                      zlota.wydanie_zlotej,
                                                      zlota

                                      from fsaps_donor_cards k
                                               left join
                                           (select correspondent_id,
                                                   card_type_id      as niebieska,
                                                   min(release_date) as wydanie_niebieskiej
                                            from fsaps_donor_cards
                                            where card_type_id = 1
                                            group by correspondent_id, card_type_id) niebieska
                                           on niebieska.correspondent_id = k.correspondent_id
                                               left join
                                           (select correspondent_id,
                                                   card_type_id      as srebrna,
                                                   min(release_date) as wydanie_srebrnej
                                            from fsaps_donor_cards
                                            where card_type_id = 2
                                            group by correspondent_id, card_type_id) srebrna
                                           on srebrna.correspondent_id = k.correspondent_id
                                               left join
                                           (select correspondent_id,
                                                   card_type_id      as zlota,
                                                   min(release_date) as wydanie_zlotej
                                            from fsaps_donor_cards
                                            where card_type_id = 3
                                            group by correspondent_id, card_type_id) zlota
                                           on zlota.correspondent_id = k.correspondent_id
                                      order by correspondent_id) color_date_all
                                order by correspondent_id) collor_cards_filtered
                               on fcp.correspondent_id = collor_cards_filtered.correspondent_id) foo
