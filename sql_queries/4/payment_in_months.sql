select correspondent_id as id_korespondenta,
       sum(amount)      as wplaty, {miesiac} as month, {rok} as year
from fsaps_payment_payment
where date
                between '{row3['first_day']}' and '{row3['last_day']}' and id_korespondenta in {list_of_id2}
                group by id_korespondenta