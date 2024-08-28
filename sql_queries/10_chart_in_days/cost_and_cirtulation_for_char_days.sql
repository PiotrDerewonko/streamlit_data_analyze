select distinct fdagt2.text as grupa_akcji_3_wysylki, fdagt.text as grupa_akcji_2_wysylki, sum(new_cost) as koszt,
    fsaps_campaign_person.correspondent_id as id_korespondenta, 1 as naklad,
    case when typ is null then 'nowy' else typ::text end as nowy_stary, 1 as dzien_po_mailingu
                from fsaps_campaign_person
                left outer join (select distinct correspondent_id, 'stary' as typ
                                         from fsaps_campaign_person where subaction_id in (select id from fsaps_campaign_subaction where action_id in (
    select id from fsaps_campaign_action where action_main_id in (
        select id from fsaps_campaign_main_action where campaign_id in (
            select id from fsaps_campaign_campaign where action_group_two_id = #A#
                                                   and action_group_three_id = #C#
            )
        )
    ))) old
                        on old.correspondent_id = fsaps_campaign_person.correspondent_id
                left outer join fsaps_campaign_subaction fcs on fsaps_campaign_person.subaction_id = fcs.id
                left outer join fsaps_campaign_action fca on fcs.action_id = fca.id
                left outer join fsaps_campaign_main_action fcma on fca.action_main_id = fcma.id
                left outer join fsaps_campaign_campaign fcc on fcma.campaign_id = fcc.id
                left outer join fsaps_dictionary_action_group_two fdagt on fcc.action_group_two_id = fdagt.id
                left outer join fsaps_dictionary_action_group_three fdagt2 on fcc.action_group_three_id = fdagt2.id
                left outer join (select subaction_id,
                                               round(sum((fcc.real_cost::float8/1000) * fcc.number)::numeric,3) as new_cost
                                       from fsaps_campaign_cost fcc group by subaction_id) fcc2 on fsaps_campaign_person.subaction_id = fcc2.subaction_id

    where fcc.action_group_two_id = #A# and fcc.action_group_three_id=#B#
group by grupa_akcji_3_wysylki, grupa_akcji_2_wysylki, id_korespondenta, typ
order by nowy_stary desc


