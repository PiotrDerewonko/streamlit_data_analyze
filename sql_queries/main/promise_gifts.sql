select kod_akcji, fmm.name as OBIECYWANY_GIFT, typ.rodzaj AS RODZAJ_GIFTU from t_akcje
    left outer join fsaps_campaign_subaction fcs
on fcs.name = t_akcje.kod_akcji
left outer join fsaps_campaign_action fca on fcs.action_id = fca.id
left outer join fsaps_campaign_main_action fcma on fca.action_main_id = fcma.id
left outer join fsaps_campaign_campaign fcc on fcma.campaign_id = fcc.id
left outer join fsaps_order_order foo on fcc.id = foo.campaign_id
left outer join fsaps_material_material fmm on foo.material_id = fmm.id
left outer join (select material_id, value AS rodzaj from fsaps_material_parameter where utility_parameter_name_id=1) typ
on typ.material_id=fmm.id
where id_grupy_akcji_1=22
ORDER BY ID_AKCJI DESC