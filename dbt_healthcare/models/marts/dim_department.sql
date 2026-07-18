with departments as (

    select
        department_id,
        department_name,
        region
    from {{ ref('stg_departments') }}

),

final as (

    select distinct
        department_id,
        department_name,
        region
    from departments

)

select *
from final