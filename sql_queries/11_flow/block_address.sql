select correspondent_id from fsaps_correspondent_member fcm
left outer join fsaps_correspondent_member_address fcma
on fcm.id = fcma.member_id
where fcma.is_blocked=True
