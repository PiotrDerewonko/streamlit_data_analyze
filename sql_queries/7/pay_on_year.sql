select id_korespondenta, 'wpłata' as wplata, min(date_part('month', data_wplywu_srodkow))::int as miesiac_pierwszej_wplaty_w_roku from t_transakcje where data_wplywu_srodkow
    between ({rok}::text||'-01-01')::date and ({rok}::text||'-12-31')::date
group by id_korespondenta