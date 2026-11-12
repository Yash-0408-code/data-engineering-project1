with green as ( 
    select
        trip_id,
        'Green' as service_type,
        vendor_id,
        rate_code_id,
        pickup_location_id,
        dropoff_location_id,
        pickup_datetime,
        dropoff_datetime,
        store_and_fwd_flag,
        passenger_count,
        trip_distance,
        trip_type,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        ehail_fee,
        improvement_surcharge,
        total_amount,
        payment_type,
        congestion_surcharge,
        filename
    from {{ ref('stg_green_tripdata') }}
),

yellow as (
    select
        trip_id,
        'Yellow' as service_type,
        vendor_id,
        rate_code_id,
        pickup_location_id,
        dropoff_location_id,
        pickup_datetime,
        dropoff_datetime,
        store_and_fwd_flag,
        passenger_count,
        trip_distance,
        1 as trip_type,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        cast(0 as numeric) as ehail_fee,
        improvement_surcharge,
        total_amount,
        payment_type,
        congestion_surcharge,
        filename
    from {{ ref('stg_yellow_tripdata') }}
),

unioned as (
    select * from green
    union all
    select * from yellow
)

select * from unioned