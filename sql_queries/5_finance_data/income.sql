select suma_wplat,
       rok,
       case
           when miesiac < 10 then '0' || (miesiac)::text
           else miesiac::text
           end as miesiac,
       typ
from (select sum(fpp.amount)          as suma_wplat,
             date_part('year', date)  as rok,
             date_part('month', date) as miesiac,
             case
                 when fcc.action_group_two_id in (9, 10, 11, 12, 24, 67, 100) then fdagt.text
                 when fcc.action_group_one_id in (22, 24) then 'Druki i prawdopodobne druki'
                 when fcc2.kind_id in (7, 8) then 'Zbiórka przykościelna'
                 else 'Pozostałe' end as typ
      from fsaps_payment_payment fpp
               left outer join fsaps_order_order_answer fooa
                               on fpp.id = fooa.payment_id
               left outer join fsaps_campaign_subaction fcs
                               on fooa.subaction_id = fcs.id
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
               left outer join fsaps_correspondent_correspondent fcc2
                               on fooa.correspondent_id = fcc2.id

      group by rok, miesiac, typ) foo
order by rok, miesiac, typ
