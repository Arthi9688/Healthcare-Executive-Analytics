with source_data as (

    select *
    from {{ ref('patients') }}

),

cleaned as (

    select
        trim(patient_id) as patient_id,

        case
            when cast(valid_patient_flag as integer) = 1 then true
            when cast(valid_patient_flag as integer) = 0 then false
            else null
        end as is_valid_patient

    from source_data

)

select *
from cleaned