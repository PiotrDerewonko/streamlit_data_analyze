select fcs.name as kod_akcji, round(sum((fcc.real_cost::float8/1000) * fcc.number)::numeric,
     3) * ilosc as koszt_calkowity, ilosc as naklad_calkowity
from (select subaction_id, count(correspondent_id) as ilosc
     from fsaps_campaign_person group by subaction_id) fcp
left outer join fsaps_campaign_cost fcc on fcp.subaction_id = fcc.subaction_id
left outer join fsaps_campaign_subaction fcs on fcp.subaction_id = fcs.id
group by  fcs.name, naklad_calkowity
union
select fcs2.name as kod_akcji, round(sum((f.real_cost::float8/1000) * f.number)::numeric,
     3) * ilosc_db as new_cost, ilosc_db as naklad
from (select subaction_id, sum(quantity) as ilosc_db from fsaps_campaign_subaction_copy group by subaction_id) quantity
left outer join fsaps_campaign_subaction fcs2 on quantity.subaction_id = fcs2.id
left outer join fsaps_campaign_cost f on fcs2.id = f.subaction_id
group by kod_akcji, naklad
order by kod_akcji desc
