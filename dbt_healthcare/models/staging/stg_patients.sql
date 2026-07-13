with source_data as (

    select *
    from {{ ref('raw_patients') }}

),

cleaned as (

    select
        trim(patient_id) as patient_id,
        trim(age_group) as age_group,
        trim(gender) as gender,
        trim(region_name) as region_name,
        cast(created_date as date) as patient_created_date
    from source_data

)

select *
from cleaned