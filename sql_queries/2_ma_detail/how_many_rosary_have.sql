select distinct id_korespondenta, 'posiada ' || count(distinct materialy)::text || ' dziesiątek' as ilosc_dziesiatek
from (select correspondent_id as id_korespondenta, regexp_replace(fmm.name, E' po koszcie.*', '') as materialy
      from fsaps_campaign_person fcp
               left outer join fsaps_campaign_material fcm
                               on fcp.subaction_id = fcm.subaction_id
               left outer join fsaps_material_material fmm
                               on fcm.material_id = fmm.id) foo
where materialy in ('RÓŻANIEC_2_PIERWSZA_DZIESIĄTKA',
                    'RÓŻANIEC-CZWARTA DZIESIĄTKA',
                    'RÓŻANIEC-DRUGA DZIESIĄTKA',
                    'RÓŻANIEC-DRUGA DZIESIĄTKA',
                    'RÓŻANIEC-DRUGA DZIESIĄTKA',
                    'RÓŻANIEC-PIĄTA DZIESIĄTKA',
                    'RÓŻANIEC-PIERWSZA DZIESIĄTKA',
                    'RÓŻANIEC-TRZECIA DZIESIĄTKA'
    )
group by id_korespondenta
order by id_korespondenta