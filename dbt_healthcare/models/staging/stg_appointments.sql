with source_data as (

    select *
    from {{ ref('raw_appointments') }}

),

cleaned as (

    select
        trim(appointment_id) as appointment_id,
        trim(request_id) as request_id,
        trim(provider_id) as provider_id,
        cast(scheduled_date as date) as scheduled_date,
        cast(appointment_date as date) as appointment_date,
        lower(trim(appointment_status)) as appointment_status,
        lower(trim(visit_type)) as visit_type,
        lower(trim(scheduling_channel)) as scheduling_channel
    from source_data

)

select *
from cleaned