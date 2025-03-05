select * from
(select distinct correspondent_id as id_korespondenta , date as data_wplywu_srodkow, row_number() over (PARTITION BY correspondent_id
        order by correspondent_id, date) as numer from fsaps_payment_payment) foo
where numer <=2