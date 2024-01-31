select id_korespondenta,'vip' as vip, #A#::text as rok from
(select correspondent_id as id_korespondenta, sum(amount) as suma_wplat
from fsaps_payment_payment
where date between '2008-01-01' and '#B#-12-31'
group by id_korespondenta) foo
where suma_wplat >=10000