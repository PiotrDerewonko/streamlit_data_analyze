SELECT correspondent_id                   as id_korespondenta,
       'wpłata'                           as wplata,
       min(date_part('month', date))::int as miesiac_pierwszej_wplaty_w_roku
from fsaps_payment_payment
where date between ({rok}::text ||'-01-01')::date and ({rok}::text ||'-12-31')::date
group by correspondent_id