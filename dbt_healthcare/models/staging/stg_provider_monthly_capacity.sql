with source_data as (

    select *
    from {{ ref('raw_provider_monthly_capacity') }}

),

cleaned as (

    select
        trim(provider_id) as provider_id,
        cast(month_start as date) as month_start,
        cast(available_hours as decimal(10, 2)) as available_hours,
        cast(booked_hours as decimal(10, 2)) as booked_hours,
        cast(patient_facing_hours as decimal(10, 2))
            as patient_facing_hours
    from source_data

)

select *
from cleaned