select max(id_grupy_akcji_2) as max from t_akcje where id_grupy_akcji_2 in (9,10,11,12) and id_grupy_akcji_3 in (
    select id_grupy_akcji_3 from t_grupy_akcji_3 where grupa_akcji_3 = '{rok}'::text
    )