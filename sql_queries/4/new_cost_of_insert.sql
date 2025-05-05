select fcs.id as id_akcji, ((ddd.suma_wplat_nowi / ddd.suma_wplat) * ddd.koszt_calkowity) as koszt_insertu
from raporty.dash_db_data ddd
         left outer join fsaps_campaign_subaction fcs
                         on ddd.kod_akcji = fcs.name
where fcs.id = #id#
