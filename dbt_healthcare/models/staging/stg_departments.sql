with source_data as (

    select *
    from {{ ref('raw_departments') }}

),

cleaned as (

    select
        cast(department_id as integer) as department_id,
        trim(department_name) as department_name,
        trim(division_name) as division_name,
        trim(region_name) as region_name,
        trim(specialty_name) as specialty_name,
        cast(active_flag as boolean) as is_active
    from source_data

)

select *
from cleaned