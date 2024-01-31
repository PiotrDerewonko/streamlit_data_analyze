select id_korespondenta, case
    when wiek between 20 and 29 then '20 - 29'
    when wiek between 30 and 39 then '30 - 39'
    when wiek between 40 and 49 then '40 - 49'
    when wiek between 50 and 59 then '50 - 59'
    when wiek between 60 and 69 then '60 - 69'
    when wiek between 70 and 79 then '70 - 79'
    when wiek between 80 and 89 then '80 - 89'
    when wiek between 90 and 99 then '90 - 99'
    when wiek > 99 then ' 100 i więcej'
else '' end as przedzial_wieku, #A#::text as rok
from (select distinct id_korespondenta,#A#::int -  date_part('year', data_urodzenia)::int as wiek
                                        from t_dane_osobowe)foo
