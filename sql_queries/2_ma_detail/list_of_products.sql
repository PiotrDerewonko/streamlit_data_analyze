select distinct regexp_replace(name, E' po koszcie.*', '') as nazwa_materiału
from fsaps_material_material
where type_id in (2, 4, 25, 34)

