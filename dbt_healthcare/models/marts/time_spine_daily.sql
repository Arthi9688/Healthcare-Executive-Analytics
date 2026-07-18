{{
    config(
        materialized = 'table'
    )
}}

with calendar as (

    select
        calendar_date
    from {{ ref('stg_calendar') }}
    where calendar_date is not null

),

final as (

    select distinct
        cast(calendar_date as date) as date_day
    from calendar

)

select *
from final
order by date_day