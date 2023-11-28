select distinct id_korespondenta, 'brał_udział' as udzial from t_akcje_korespondenci where id_akcji in (
    select id_akcji from t_akcje where id_grupy_akcji_2=12 and id_grupy_akcji_3 in (
        select id_grupy_akcji_3 from t_grupy_akcji_3 where grupa_akcji_3 = {rok}::text
        )
    )