with requests as (

    select
        request_id,
        patient_id,
        department_id,
        request_date,
        patient_type,
        request_channel,
        priority
    from {{ ref('stg_appointment_requests') }}

),

appointments as (

    select
        appointment_id,
        request_id,
        provider_id,
        scheduled_date,
        appointment_date,
        appointment_status,
        visit_type,
        scheduling_channel
    from {{ ref('stg_appointments') }}

),

combined as (

    select
        r.request_id,
        r.patient_id,
        r.department_id,
        r.request_date,
        r.patient_type,
        r.request_channel,
        r.priority,

        a.appointment_id,
        a.provider_id,
        a.scheduled_date,
        a.appointment_date,
        a.appointment_status,
        a.visit_type,
        a.scheduling_channel,

        case
            when a.appointment_id is not null then 1
            else 0
        end as scheduled_flag,

        case
            when a.scheduled_date is not null
            then date_diff('day', r.request_date, a.scheduled_date)
            else null
        end as days_to_schedule,

        case
            when a.scheduled_date is null then null
            when date_diff('day', r.request_date, a.scheduled_date) <= 14
                then 1
            else 0
        end as scheduled_within_14_days_flag,

        case
            when lower(a.scheduling_channel) in (
                'self-scheduling',
                'portal'
            ) then 1
            else 0
        end as digital_scheduling_flag,

        case
            when a.appointment_status = 'completed' then 1
            else 0
        end as completed_flag

    from requests r

    left join appointments a
        on r.request_id = a.request_id

)

select *
from combined