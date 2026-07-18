with source_data as (

    select *
    from {{ ref('provider_productivity') }}

),

cleaned as (

    select
        cast(month_begin_date as date)
            as month_begin_date,

        cast(month_end_date as date)
            as month_end_date,

        trim(provider_id) as provider_id,

        cast(fte_department_id as integer)
            as fte_department_id,

        cast(clinical_fte as decimal(8, 4))
            as clinical_fte,

        cast(business_days_in_month as integer)
            as business_days_in_month,

        cast(regular_available_hours as decimal(12, 4))
            as regular_available_hours,

        cast(expected_patient_facing_hours as decimal(12, 4))
            as source_expected_patient_facing_hours,

        cast(percent_patient_facing as decimal(12, 6))
            as source_percent_patient_facing,

        cast(meets_80_percent_flag as integer)
            as source_meets_80_percent_flag

    from source_data

)

select *
from cleaned