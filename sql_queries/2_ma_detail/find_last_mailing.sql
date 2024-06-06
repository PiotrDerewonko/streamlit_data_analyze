select fdagt.text as grupa_akcji_2, f.text as grupa_akcji_3 from fsaps_campaign_campaign
    left outer join fsaps_dictionary_action_group_two fdagt on fsaps_campaign_campaign.action_group_two_id = fdagt.id
    left outer join fsaps_dictionary_action_group_three f on fsaps_campaign_campaign.action_group_three_id = f.id
    where date_from is not null
    and fsaps_campaign_campaign.action_group_two_id is not null and fsaps_campaign_campaign.action_group_three_id is not null
    and fsaps_campaign_campaign.action_group_one_id = 23
    order by date_from desc limit 1