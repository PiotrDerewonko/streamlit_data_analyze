select date_part('year', adod.data_pozyskania) as rok_dodania, grupa_akcji_1, grupa_akcji_2, kod_akcji,
        case when date_part('month', adod.data_pozyskania)<10 then '0'||date_part('month', adod.data_pozyskania)::text
        else date_part('month', adod.data_pozyskania)::text end as miesiac_dodania, count(correspondent_id) as ilosc
        from fsaps_v_zrodlo_pozyskania_darczyncy adod
        group by rok_dodania, grupa_akcji_1, grupa_akcji_2,kod_akcji, miesiac_dodania