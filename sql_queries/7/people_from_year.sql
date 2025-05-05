select correspondent_id                        as id_korespondenta,
       grupa_akcji_1,
       grupa_akcji_2,
       grupa_akcji_3,
       data_pozyskania::date,
       date_part('year', data_pozyskania)::int as rok_dodania
from fsaps_v_zrodlo_pozyskania_darczyncy
where data_pozyskania between ({rok}::text ||'-01-01')::date and ({rok}::text ||'-12-31')::date