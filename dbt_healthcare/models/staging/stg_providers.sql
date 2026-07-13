with source_data as (

    select *
    from {{ ref('raw_providers') }}

),

cleaned as (

    select
        trim(provider_id) as provider_id,
        trim(provider_name) as provider_name,
        cast(department_id as integer) as department_id,
        trim(provider_type) as provider_type,
        cast(fte as decimal(5, 2)) as provider_fte,
        cast(active_flag as boolean) as is_active
    from source_data

)

select *
from cleaned