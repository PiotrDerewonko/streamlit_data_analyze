select kod_akcji,grupa_akcji_2, grupa_akcji_3::int, fcma.name as akcja_glowna_mailingu, fca.name as akcja_mailingu
from t_akcje ta
    left outer join t_grupy_akcji_2 gr2
    on gr2.id_grupy_akcji_2=ta.id_grupy_akcji_2
    left outer join t_grupy_akcji_3 gr3
    on gr3.id_grupy_akcji_3=ta.id_grupy_akcji_3
left outer join fsaps_campaign_campaign fcc
on fcc.action_group_one_id=ta.id_grupy_akcji_1 and fcc.action_group_two_id = ta.id_grupy_akcji_2 and
   fcc.action_group_three_id = ta.id_grupy_akcji_3
left outer join (select * from fsaps_campaign_main_action where newly_acquired=False) fcma on fcc.id = fcma.campaign_id and
                                                   ta.kod_akcji like '%'||fcma.prefix||'%'
left outer join fsaps_campaign_action fca on fcma.id = fca.action_main_id and
                                                   ta.kod_akcji like '%'||fca.prefix||'%'
where id_grupy_akcji_1=23 and  ta.id_grupy_akcji_2 in (9,10,11,12,24,67,100)