with source_data as (

    select *
    from {{ ref('providers') }}

),

cleaned as (

    select
        cast(provider_durable_key as bigint)
            as provider_durable_key,

        trim(provider_id) as provider_id,
        trim(provider_name) as provider_name,
        trim(provider_type) as provider_type,
        trim(provider_type_group) as provider_type_group,

        cast(primary_department_id as integer)
            as primary_department_id,

        trim(primary_specialty) as primary_specialty,
        upper(trim(active_status)) as active_status,

        case
            when cast(is_current as integer) = 1 then true
            when cast(is_current as integer) = 0 then false
            else null
        end as is_current,

        trim(npi) as npi,
        trim(user_id) as user_id

    from source_data

)

select *
from cleaned