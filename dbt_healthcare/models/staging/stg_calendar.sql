with source_data as (

    select *
    from {{ ref('calendar') }}

),

cleaned as (

    select
        cast(calendar_date as date) as calendar_date,
        cast(month_begin_date as date) as month_begin_date,
        cast(month_end_date as date) as month_end_date,

        trim(month_name) as month_name,
        trim(month_name_short) as month_name_short,
        trim(month_year) as month_year,

        month(cast(calendar_date as date)) as month_number,

        cast(year_month as integer) as year_month,

        cast(year_month_sequence as integer)
            as year_month_sequence,

        cast(calendar_year as integer) as calendar_year,
        cast(fiscal_year as integer) as fiscal_year,

        case
            when upper(trim(weekend_flag)) = 'Y' then true
            when upper(trim(weekend_flag)) = 'N' then false
            else null
        end as is_weekend,

        case
            when upper(trim(holiday_flag)) = 'Y' then true
            when upper(trim(holiday_flag)) = 'N' then false
            else null
        end as is_holiday,

        cast(business_day_flag as integer)
            as business_day_flag

    from source_data

)

select *
from cleaned
