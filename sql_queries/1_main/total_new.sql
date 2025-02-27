select kod_akcji, count(correspondent_id) as pozyskano from fsaps_v_zrodlo_pozyskania_darczyncy
group by kod_akcji