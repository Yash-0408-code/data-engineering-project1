{{
    config(
        materialized='table',
        partition_by={
            'field': 'pickup_datetime',
            'data_type': 'timestamp',
            'granularity': 'month'
        },
        cluster_by=['service_type','pickup_location_id']
    )
}}

with trips as (
    select * from {{ ref('int_trips_unioned') }}
),

zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)

select 
    -- identifiers
    trips.trip_id,
    trips.service_type,
    trips.vendor_id,
    trips.rate_code_id,

    -- pickup location
    trips.pickup_location_id,
    pickup_zone.borough as pickup_borough,
    pickup_zone.zone as pickup_zone,

    -- dropoff location
    trips.dropoff_location_id,
    dropoff_zone.borough as dropoff_borough,
    dropoff_zone.zone as dropoff_zone,

    -- timestamps
    trips.pickup_datetime,
    trips.dropoff_datetime,

    -- trip info
    trips.store_and_fwd_flag,
    trips.passenger_count,
    trips.trip_distance,
    trips.trip_type,

    -- payment info
    trips.fare_amount,
    trips.extra,
    trips.mta_tax,
    trips.tip_amount,
    trips.tolls_amount,
    trips.ehail_fee,
    trips.improvement_surcharge,
    trips.total_amount,
    trips.payment_type,
    {{ get_payment_type_description('trips.payment_type') }} as payment_type_description

from trips
inner join zones as pickup_zone
    on trips.pickup_location_id = pickup_zone.location_id
inner join zones as dropoff_zone
    on trips.dropoff_location_id = dropoff_zone.location_id