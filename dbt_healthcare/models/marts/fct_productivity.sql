with productivity as (

    select
        month_begin_date,
        month_end_date,
        provider_id,
        fte_department_id,
        clinical_fte,
        business_days_in_month,
        regular_available_hours,
        source_expected_patient_facing_hours,
        source_percent_patient_facing,
        source_meets_80_percent_flag
    from {{ ref('stg_provider_productivity') }}

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

calendar as (

    select
        calendar_date,
        month_name_short,
        month_year,
        year_month,
        year_month_sequence,
        calendar_year,
        fiscal_year
    from {{ ref('stg_calendar') }}

),

joined as (

    select
        pr.month_begin_date,
        pr.month_end_date,

        pr.provider_id,
        pr.fte_department_id as department_id,

        pr.clinical_fte,
        pr.business_days_in_month,
        pr.regular_available_hours,
        pr.source_expected_patient_facing_hours,
        pr.source_percent_patient_facing,
        pr.source_meets_80_percent_flag,

        p.provider_name,
        p.provider_type,
        p.provider_type_group,
        p.primary_specialty,

        d.department_name,
        d.division,
        d.lhs,
        d.region,
        d.specialty,
        d.is_hospital_outpatient,

        c.month_name_short,
        c.month_year,
        c.year_month,
        c.year_month_sequence,
        c.calendar_year,
        c.fiscal_year
        

    from productivity pr

    inner join providers p
        on pr.provider_id = p.provider_id

    inner join departments d
        on pr.fte_department_id = d.department_id

    inner join calendar c
        on pr.month_begin_date = c.calendar_date

    where d.region <> 'Trellis'

      and pr.month_begin_date >= (
          dateadd(
              month,
              -24,
              date_trunc('month', current_date)
          )
      )

      and pr.month_begin_date
          < date_trunc('month', current_date)

),

final as (

    select
        month_begin_date,
        month_end_date,

        provider_id,
        department_id,

        provider_name,
        provider_type,
        provider_type_group,
        primary_specialty,

        department_name,
        division,
        lhs,
        region,
        specialty,

        case
            when is_hospital_outpatient = true then 'Y'
            else 'N'
        end as hospital_outpatient_flag,

        clinical_fte,
        business_days_in_month,
        regular_available_hours,
        source_expected_patient_facing_hours,

        source_percent_patient_facing
            as percent_patient_facing,

        case
            when source_meets_80_percent_flag is null then null
            when source_meets_80_percent_flag = true then 1
            else 0
        end as meets_80_percent_flag,

        case
            when source_percent_patient_facing is not null then 1
            else 0
        end as patient_facing_denominator_flag,
        

        month_name_short,
        month_year,
        year_month,
        year_month_sequence,
        calendar_year,
        case
            when calendar_year = extract(year from current_date) then 'Current Year'
            when calendar_year = extract(year from current_date) - 1 then 'Prior Year'
            else 'Other'
        end as chart_period,
        fiscal_year,

        current_date as refresh_date

    from joined

)

select *
from final