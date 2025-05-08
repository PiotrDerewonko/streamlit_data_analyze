select correspondent_id as id_korespondenta,
       sum(amount)      as wplaty, #MIESIAC# as month, #ROK# as year
from fsaps_payment_payment
where date
                between #DATE_FROM# and #DATE_TO# and correspondent_id in #LIST_COR_ID#
                group by id_korespondenta