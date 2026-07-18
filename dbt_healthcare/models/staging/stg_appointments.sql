with source_data as (

    select *
    from {{ ref('appointments') }}

),

cleaned as (

    select
        trim(appointment_id) as appointment_id,
        trim(patient_encounter_id) as patient_encounter_id,
        trim(patient_id) as patient_id,

        cast(department_id as integer) as department_id,
        trim(provider_id) as provider_id,

        cast(appointment_made_date as date)
            as appointment_made_date,

        cast(appointment_date as date)
            as appointment_date,

        nullif(trim(referral_id), '')
            as referral_id,

        cast(referral_entry_date as date)
            as referral_entry_date,

        cast(wait_days as integer) as source_wait_days,
        cast(admin_days as integer) as source_admin_days,

        case
            when cast(new_visit_flag as integer) = 1 then true
            when cast(new_visit_flag as integer) = 0 then false
            else null
        end as is_new_visit,

        case
            when cast(scheduled_online_flag as integer) = 1 then true
            when cast(scheduled_online_flag as integer) = 0 then false
            else null
        end as is_scheduled_online,

        trim(visit_type_id) as visit_type_id,
        trim(visit_type_name) as visit_type_name,

        case
            when cast(new_to_enterprise_flag as integer) = 1 then true
            when cast(new_to_enterprise_flag as integer) = 0 then false
            else null
        end as is_new_to_enterprise,

        case
            when cast(new_to_division_flag as integer) = 1 then true
            when cast(new_to_division_flag as integer) = 0 then false
            else null
        end as is_new_to_division

    from source_data

)

select *
from cleaned