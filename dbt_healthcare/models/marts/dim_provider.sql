with providers as (

    select
        provider_id,
        provider_name,
        provider_type,
        provider_type_group,
        primary_specialty
    from {{ ref('stg_providers') }}

),

productivity as (

    select
        provider_id,
        count(*) as productivity_month_count,
        avg(source_percent_patient_facing)
            as average_patient_facing_percent
    from {{ ref('stg_provider_productivity') }}
    group by provider_id

),

appointments as (

    select
        provider_id,
        count(*) as appointment_count,
        median(
            date_diff(
                'day',
                appointment_made_date,
                appointment_date
            )
        ) as median_wait_days
    from {{ ref('stg_appointments') }}
    where is_new_visit = true
    group by provider_id

),

final as (

    select
        p.provider_id,
        p.provider_name,
        p.provider_type,
        p.provider_type_group,
        p.primary_specialty,

        coalesce(a.appointment_count, 0)
            as appointment_count,

        a.median_wait_days,

        coalesce(pr.productivity_month_count, 0)
            as productivity_month_count,

        pr.average_patient_facing_percent

    from providers p

    left join appointments a
        on p.provider_id = a.provider_id

    left join productivity pr
        on p.provider_id = pr.provider_id

)

select *
from final