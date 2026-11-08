with zones as (
    select * from {{ ref('taxi_zone_lookup') }}
)

select 
    locationid as location_id,
    borough,
    zone,
    replace(service_zone, 'Boro', 'Green') as service_zone
from zones