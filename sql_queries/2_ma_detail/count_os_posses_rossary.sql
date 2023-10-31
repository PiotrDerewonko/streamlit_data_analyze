select correspondent_id as id_korespondenta, 'posiada ' ||count(material_id)::text||' dziesiątek' as ilosc_dziesiatek  from (
select distinct correspondent_id, material_id from fsaps_campaign_person fcp
left outer join fsaps_campaign_subaction fcs on fcp.subaction_id = fcs.id
left outer join fsaps_campaign_material fcm on fcs.id = fcm.subaction_id
where  fcm.material_id in (select id from fsaps_material_material where name like '%DZIES%')) foo
group by id_korespondenta