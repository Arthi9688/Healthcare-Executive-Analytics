with source_data as (

    select *
    from {{ ref('raw_appointment_requests') }}

),

cleaned as (

    select
        trim(request_id) as request_id,
        trim(patient_id) as patient_id,
        cast(department_id as integer) as department_id,
        cast(request_date as date) as request_date,
        lower(trim(patient_type)) as patient_type,
        lower(trim(request_channel)) as request_channel,
        lower(trim(priority)) as priority
    from source_data

)

select *
from cleaned