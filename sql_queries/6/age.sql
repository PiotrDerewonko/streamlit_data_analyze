select distinct correspondent_id as id_korespondenta, case
    when wiek between 20 and 29 then '20 - 29'
    when wiek between 30 and 39 then '30 - 39'
    when wiek between 40 and 49 then '40 - 49'
    when wiek between 50 and 59 then '50 - 59'
    when wiek between 60 and 69 then '60 - 69'
    when wiek between 70 and 79 then '70 - 79'
    when wiek between 80 and 89 then '80 - 89'
    when wiek between 90 and 99 then '90 - 99'
    when wiek > 99 then ' 100 i więcej'
else 'brak danych' end as przedzial_wieku, #A# as rok
from (select correspondent_id,
             #A#::int -  date_part('year', birthday)::int as wiek,
             row_number() over (partition by correspondent_id order by correspondent_id, birthday) as numer
      from fsaps_correspondent_member) foo
where numer = 1
  and correspondent_id in (select correspondent_id
                           from fsaps_campaign_person
                           where subaction_id in (select id
                                                  from fsaps_campaign_subaction
                                                  where action_id in (select id
                                                                      from fsaps_campaign_action
                                                                      where action_main_id in (select id
                                                                                               from fsaps_campaign_main_action
                                                                                               where campaign_id in
                                                                                                     (select id
                                                                                                      from fsaps_campaign_campaign
                                                                                                      where action_group_two_id = 12
                                                                                                        and action_group_three_id in
                                                                                                            (select id
                                                                                                             from fsaps_dictionary_action_group_three
                                                                                                             where text = '#A#'))))))

