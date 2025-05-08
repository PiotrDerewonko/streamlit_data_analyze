select correspondent_id as id_korespondenta,
       data_pozyskania::date as data_dodania,
       0               as wplaty,
       0               as koszt_utrzymania,
       subaction       as id_akcji,
       1 as miesiac_obecnosci_w_bazie
from fsaps_v_zrodlo_pozyskania_darczyncy
where subaction = #A#