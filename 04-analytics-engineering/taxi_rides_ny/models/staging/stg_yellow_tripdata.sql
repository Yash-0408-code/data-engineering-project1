with source as (
    select * from {{ source('zoomcamp', 'yellow_tripdata') }}
),

renamed as (
    select
        -- identifiers
        unique_row_id as trip_id,
        cast(safe_cast(vendorid as numeric) as integer) as vendor_id,
        cast(safe_cast(ratecodeid as numeric) as integer) as rate_code_id,
        cast(safe_cast(pulocationid as numeric) as integer) as pickup_location_id,
        cast(safe_cast(dolocationid as numeric) as integer) as dropoff_location_id,

        -- timestamps
        tpep_pickup_datetime as pickup_datetime,
        tpep_dropoff_datetime as dropoff_datetime,

        -- trip info
        store_and_fwd_flag,
        passenger_count,
        trip_distance,

        -- payment info
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        improvement_surcharge,
        total_amount,
        payment_type,
        congestion_surcharge,

        -- lineage
        filename

    from source
    where vendorid is not null
)

select * from renamed