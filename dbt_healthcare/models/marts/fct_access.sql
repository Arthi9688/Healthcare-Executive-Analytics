with appointments as (

    select
        appointment_id,
        patient_encounter_id,
        patient_id,
        department_id,
        provider_id,
        appointment_made_date,
        appointment_date,
        referral_id,
        referral_entry_date,
        source_wait_days,
        source_admin_days,
        is_new_visit,
        is_scheduled_online,
        visit_type_id,
        visit_type_name,
        is_new_to_enterprise,
        is_new_to_division
    from {{ ref('stg_appointments') }}

),

valid_patients as (

    select
        patient_id
    from {{ ref('stg_patients') }}
    where is_valid_patient = true

),

departments as (

    select
        department_id,
        department_name,
        division,
        lhs,
        region,
        specialty,
        is_hospital_outpatient
    from {{ ref('stg_departments') }}

),

providers as (

    select
        provider_id,
        provider_name,
        provider_type,
        provider_type_group,
        primary_specialty
    from {{ ref('stg_providers') }}

),

calendar as (

    select
        calendar_date,
        month_begin_date,
        month_end_date,
        month_name_short,
        month_year,
        year_month,
        year_month_sequence,
        calendar_year,
        fiscal_year
    from {{ ref('stg_calendar') }}

),

eligible_appointments as (

    select
        a.appointment_id,
        a.patient_encounter_id,
        a.patient_id,
        a.department_id,
        a.provider_id,

        a.appointment_made_date,
        a.appointment_date,
        a.referral_id,
        a.referral_entry_date,

        a.source_wait_days,
        a.source_admin_days,

        DATEDIFF(
            day,
            a.appointment_made_date,
            a.appointment_date
        ) as calculated_wait_days,

        case
            when a.referral_entry_date is not null then
                DATEDIFF(
                    day,
                    a.referral_entry_date,
                    a.appointment_made_date
                )
            else null
        end as calculated_admin_days,

        a.is_scheduled_online,
        a.visit_type_id,
        a.visit_type_name,
        a.is_new_to_enterprise,
        a.is_new_to_division,

        d.department_name,
        d.division,
        d.lhs,
        d.region,
        d.specialty,
        d.is_hospital_outpatient,

        p.provider_name,
        p.provider_type,
        p.provider_type_group,
        p.primary_specialty,

        c.month_begin_date,
        c.month_end_date,
        c.month_name_short,
        c.month_year,
        c.year_month,
        c.year_month_sequence,
        c.calendar_year,
        c.fiscal_year

    from appointments a

    inner join valid_patients pat
        on a.patient_id = pat.patient_id

    inner join departments d
        on a.department_id = d.department_id

    inner join providers p
        on a.provider_id = p.provider_id

    inner join calendar c
        on a.appointment_made_date = c.calendar_date

    where a.is_new_visit = true

      and (
          a.source_wait_days is not null
          or a.source_admin_days is not null
      )

      and d.region <> 'Trellis'

      and c.month_begin_date >= (
          date_trunc('month', current_date)
          - interval '24 months'
      )

      and c.month_begin_date < date_trunc('month', current_date)

),

final as (

    select
        appointment_id,
        patient_encounter_id,
        patient_id,
        department_id,
        provider_id,

        appointment_made_date,
        appointment_date,
        referral_id,
        referral_entry_date,

        source_wait_days,
        source_admin_days,
        calculated_wait_days,
        calculated_admin_days,

        case
            when calculated_wait_days is null then null
            when calculated_wait_days <= 14 then 1
            else 0
        end as meets_14_wait_days_flag,

        case
            when calculated_wait_days is not null then 1
            else 0
        end as wait_days_denominator_flag,

        case
            when calculated_admin_days is null then null
            when calculated_admin_days <= 7 then 1
            else 0
        end as meets_7_admin_days_flag,

        case
            when calculated_admin_days is not null then 1
            else 0
        end as admin_days_denominator_flag,

        case
            when is_scheduled_online then 'Y'
            else 'N'
        end as scheduled_online,

        'New Visit Types' as visit_type_category,
        visit_type_id,
        visit_type_name as visit_type,

        case
            when is_new_to_enterprise then 'Y'
            else 'N'
        end as new_to_enterprise,

        case
            when is_new_to_division then 'Y'
            else 'N'
        end as new_to_division,

        department_name,
        division,
        lhs,
        region,
        specialty,

        case
            when is_hospital_outpatient then 'Y'
            else 'N'
        end as hospital_outpatient_flag,

        provider_name,
        provider_type,
        provider_type_group,
        primary_specialty,

        month_begin_date,
        month_end_date,
        month_name_short,
        month_year,
        year_month,
        year_month_sequence,
        calendar_year,
        fiscal_year,
        case
            when calendar_year = extract(year from current_date) then 'Current Year'
            when calendar_year = extract(year from current_date) - 1 then 'Prior Year'
            else 'Other'
        end as chart_period,
        current_date as refresh_date

    from eligible_appointments

)

select *
from final