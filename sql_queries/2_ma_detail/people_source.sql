select correspondent_id                   as id_korespondenta,
       subaction                          as kod_akcji_dodania,
       grupa_akcji_1                      as grupa_akcji_1_dodania,
       grupa_akcji_2                      as grupa_akcji_2_dodania,
       grupa_akcji_3                      as grupa_akcji_3_dodania,
       date_part('year', data_pozyskania) as rok_dodania,
       data_pozyskania                    as data_dodania
from fsaps_v_zrodlo_pozyskania_darczyncy
order by id_korespondenta