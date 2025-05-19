select correspondent_id as id_korespondenta,
       count(amount)    as liczba_wplat_#A#

from fsaps_payment_payment
where date between '#A#-01-01' and '#A#-12-31'
group by correspondent_id