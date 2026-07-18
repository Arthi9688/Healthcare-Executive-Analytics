with source_data as (

    select *
    from {{ ref('departments') }}

),

cleaned as (

    select
        cast(department_id as integer) as department_id,
        trim(department_name) as department_name,
        trim(division) as division,
        trim(lhs) as lhs,
        trim(region) as region,
        trim(specialty) as specialty,

        case
            when upper(trim(hospital_outpatient_flag)) = 'Y' then true
            when upper(trim(hospital_outpatient_flag)) = 'N' then false
            else null
        end as is_hospital_outpatient,

        case
            when upper(trim(count_resource_flag)) = 'Y' then true
            when upper(trim(count_resource_flag)) = 'N' then false
            else null
        end as is_count_resource,

        case
            when upper(trim(active_flag)) = 'Y' then true
            when upper(trim(active_flag)) = 'N' then false
            else null
        end as is_active

    from source_data

)

select *
from cleaned