select id_korespondenta,
       case
           when okreg_pocztowy = 0 then 'warszawski'
           when okreg_pocztowy = 1 then 'olsztyński'
           when okreg_pocztowy = 2 then 'lubelski'
           when okreg_pocztowy = 3 then 'krakowski'
           when okreg_pocztowy = 4 then 'katowicki'
           when okreg_pocztowy = 5 then 'wrocławski'
           when okreg_pocztowy = 6 then 'poznański'
           when okreg_pocztowy = 7 then 'szczeciński'
           when okreg_pocztowy = 8 then 'gdański'
           when okreg_pocztowy = 9 then 'łódzki'
           end as okreg_pocztowy
from (select id_korespondenta, substring(kod_pocztowy, 1, 1)::int as okreg_pocztowy
      from raporty.fsaps_v_adresy_do_mailingow) a