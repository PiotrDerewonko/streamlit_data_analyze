select correspondent_id as id_korespondenta, data, sum((fcc.real_cost::float8/1000) * fcc.number) as koszt_utrzymania
from fsaps_campaign_person fcp
         left outer join fsaps_campaign_cost fcc
                         on fcp.subaction_id = fcc.subaction_id
         left outer join (select fcs.id, fcc2.date_from as data
                          from fsaps_campaign_subaction fcs
                                   left outer join fsaps_campaign_action fca
                                                   on fcs.action_id = fca.id
                                   left outer join fsaps_campaign_main_action fcma
                                                   on fca.action_main_id = fcma.id
                                   left outer join fsaps_campaign_campaign fcc2
                                                   on fcma.campaign_id = fcc2.id) foo
                         on fcp.subaction_id = foo.id
group by id_korespondenta, data
order by id_korespondenta
