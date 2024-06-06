import pandas as pd
import streamlit as st


def choose(con) -> [str, str, str]:
    sql = '''select fdagt.text as grupa_akcji_2, f.text as grupa_akcji_3 from fsaps_campaign_campaign
left outer join fsaps_dictionary_action_group_two fdagt on fsaps_campaign_campaign.action_group_two_id = fdagt.id
left outer join fsaps_dictionary_action_group_three f on fsaps_campaign_campaign.action_group_three_id = f.id
where date_from is not null
and fsaps_campaign_campaign.action_group_two_id is not null and fsaps_campaign_campaign.action_group_three_id is not null
and fsaps_campaign_campaign.action_group_one_id = 23
order by date_from desc limit 1'''
    data = pd.read_sql_query(sql, con)
    default_camp = data['grupa_akcji_2'].iloc[0]
    current_year = int(data['grupa_akcji_3'].iloc[0])
    type_of_campaign = st.multiselect(options=['MAILING ADRESOWY', 'INTENCJE ŚWIĘTYCH'], default='MAILING ADRESOWY',
                                      label='Typ kampanii', )
    qamp = st.multiselect(options=['KARDYNALSKA LUTY', 'MAILING Q1', 'MAILING Q2', 'KARDYNALSKA SIERPIEŃ',
                                   'MAILING Q3 KUSTOSZ LIPIEC', 'MAILING Q3', 'MAILING Q4'],
                          label='Proszę wybrać mailing',
                          default=[default_camp])
    years_options = []
    for i in range(2008, current_year + 1):
        years_options.append(str(i))
    years = st.multiselect(options=years_options, label='Proszę wybrać rok mailingu',
                           default=years_options[-5:])
    return qamp, years, type_of_campaign
