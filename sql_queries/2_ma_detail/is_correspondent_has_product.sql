select id_korespondenta, 'posiada \n'||kod_materialu as "#A#" from (
select distinct correspondent_id as id_korespondenta,  regexp_replace(name, E' po koszcie.*', '') as kod_materialu
from fsaps_campaign_person fcp
         left outer join fsaps_campaign_material fcm
                         on fcp.subaction_id = fcm.subaction_id
         left outer join fsaps_material_material fmm
                         on fcm.material_id = fmm.id
order by id_korespondenta, kod_materialu)foo
where kod_materialu = '#A#'
