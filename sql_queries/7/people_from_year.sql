select id_korespondenta, grupa_akcji_1, grupa_akcji_2, grupa_akcji_3, data, date_part('year', data)::int as rok_dodania
from v_akcja_dodania_korespondenta where data between ({rok}::text||'-01-01')::date and ({rok}::text||'-12-31')::date