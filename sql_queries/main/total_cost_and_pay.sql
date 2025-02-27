select distinct fvzpd.kod_akcji, laczna_suma_wplat, laczny_koszt_utrzymania
from fsaps_v_zrodlo_pozyskania_darczyncy fvzpd
         left outer join (select kod_akcji, sum(amount) as laczna_suma_wplat
                          from fsaps_payment_payment fpp
                                   left outer join fsaps_v_zrodlo_pozyskania_darczyncy zrodlo
                                                   on fpp.correspondent_id = zrodlo.correspondent_id
                          group by kod_akcji) pay
                         on fvzpd.kod_akcji = pay.kod_akcji
         left outer join (select zrodlo.kod_akcji, sum(koszt) as laczny_koszt_utrzymania
                          from (select correspondent_id,
                                       FCS.NAME,
                                       fcc.name,
                                       fcs.id,
                                       ((real_cost * number)::double precision / 1000) as koszt
                                from fsaps_campaign_person fcp
                                         left outer join fsaps_campaign_subaction fcs
                                                         on fcp.subaction_id = fcs.id
                                         left outer join fsaps_campaign_cost fcc
                                                         on fcs.id = fcc.subaction_id) cost
                                   left outer join fsaps_v_zrodlo_pozyskania_darczyncy zrodlo
                                                   on cost.correspondent_id = zrodlo.correspondent_id
                          group by zrodlo.kod_akcji) koszt
                         on fvzpd.kod_akcji = koszt.kod_akcji
where fvzpd.grupa_akcji_1 in ('DRUKI BEZADRESOWE', 'EVENT');