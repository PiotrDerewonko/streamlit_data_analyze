select distinct correspondent_id, blocked_at from fsaps_correspondent_member fcm
left outer join fsaps_correspondent_member_address fcma
                        on fcm.id = fcma.member_id
where city_id is not null and postal_code is not null  and street_object_id is not null
and building_number is not null and blocked_at is not null and country_id = 1
order by blocked_at;