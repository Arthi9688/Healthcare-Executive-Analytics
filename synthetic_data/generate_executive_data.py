from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# Configuration
# ============================================================

RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)

OUTPUT_DIR = Path(__file__).resolve().parent / "generated"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 24 completed months for this portfolio scenario.
START_DATE = pd.Timestamp("2024-07-01")
END_DATE = pd.Timestamp("2026-06-30")

N_PATIENTS = 10_000
N_PROVIDERS = 80
N_APPOINTMENTS = 45_000
N_SURVEY_ANSWERS = 18_000
N_GROWTH_EVENTS = 18_000

ACCESS_QUESTION_KEYS = [
    "ACCESS_Q1",
    "ACCESS_Q2",
    "ACCESS_Q3",
    "ACCESS_Q4",
]


# ============================================================
# Helpers
# ============================================================

def save_csv(df: pd.DataFrame, filename: str) -> None:
    """Save a dataframe to the generated-data directory."""
    filepath = OUTPUT_DIR / filename
    df.to_csv(filepath, index=False)

    print(
        f"Created {filename:<35} "
        f"{len(df):>8,} rows"
    )


def random_dates(
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    count: int,
) -> pd.Series:
    """Return random timestamps between two dates."""
    total_days = (end_date - start_date).days

    offsets = rng.integers(
        low=0,
        high=total_days + 1,
        size=count,
    )

    return pd.Series(
        start_date + pd.to_timedelta(offsets, unit="D")
    )


def month_difference(
    later_date: pd.Timestamp,
    earlier_date: pd.Timestamp,
) -> int:
    return (
        (later_date.year - earlier_date.year) * 12
        + later_date.month
        - earlier_date.month
    )


# ============================================================
# 1. Departments
# Grain: one row per department
# ============================================================

departments = pd.DataFrame(
    [
        [
            101,
            "North Family Medicine",
            "Primary Care",
            "North Health System",
            "North",
            "Family Medicine",
            "N",
            "Y",
            "Y",
        ],
        [
            102,
            "Central Internal Medicine",
            "Primary Care",
            "Central Health System",
            "Central",
            "Internal Medicine",
            "N",
            "Y",
            "Y",
        ],
        [
            103,
            "East Cardiology",
            "Medical Specialties",
            "East Health System",
            "East",
            "Cardiology",
            "Y",
            "Y",
            "Y",
        ],
        [
            104,
            "North Neurology",
            "Medical Specialties",
            "North Health System",
            "North",
            "Neurology",
            "Y",
            "Y",
            "Y",
        ],
        [
            105,
            "Central Gastroenterology",
            "Medical Specialties",
            "Central Health System",
            "Central",
            "Gastroenterology",
            "Y",
            "Y",
            "Y",
        ],
        [
            106,
            "West Endocrinology",
            "Medical Specialties",
            "West Health System",
            "West",
            "Endocrinology",
            "N",
            "Y",
            "Y",
        ],
        [
            107,
            "East Orthopedics",
            "Surgical Specialties",
            "East Health System",
            "East",
            "Orthopedics",
            "Y",
            "Y",
            "Y",
        ],
        [
            108,
            "South General Surgery",
            "Surgical Specialties",
            "South Health System",
            "South",
            "General Surgery",
            "Y",
            "Y",
            "Y",
        ],
        [
            109,
            "Central Women's Health",
            "Women's Health",
            "Central Health System",
            "Central",
            "Obstetrics and Gynecology",
            "N",
            "Y",
            "Y",
        ],
        [
            110,
            "West Dermatology",
            "Medical Specialties",
            "West Health System",
            "West",
            "Dermatology",
            "N",
            "Y",
            "Y",
        ],
        [
            111,
            "Coastal Pulmonology",
            "Medical Specialties",
            "Coastal Health System",
            "Coastal",
            "Pulmonology",
            "Y",
            "Y",
            "Y",
        ],
        [
            112,
            "Trellis Specialty Clinic",
            "Medical Specialties",
            "Trellis Health System",
            "Trellis",
            "Rheumatology",
            "N",
            "Y",
            "Y",
        ],
    ],
    columns=[
        "department_id",
        "department_name",
        "division",
        "lhs",
        "region",
        "specialty",
        "hospital_outpatient_flag",
        "count_resource_flag",
        "active_flag",
    ],
)

save_csv(departments, "departments.csv")


# ============================================================
# 2. Providers
# Grain: one row per provider
# ============================================================

active_department_ids = departments.loc[
    departments["active_flag"].eq("Y"),
    "department_id",
].to_numpy()

provider_department_ids = rng.choice(
    active_department_ids,
    size=N_PROVIDERS,
    replace=True,
)

department_specialty_map = dict(
    zip(
        departments["department_id"],
        departments["specialty"],
    )
)

provider_types = rng.choice(
    ["Physician", "APP"],
    size=N_PROVIDERS,
    p=[0.72, 0.28],
)

providers = pd.DataFrame(
    {
        "provider_durable_key": np.arange(
            50_001,
            50_001 + N_PROVIDERS,
        ),
        "provider_id": [
            f"PROV_{i:04d}"
            for i in range(1, N_PROVIDERS + 1)
        ],
        "provider_name": [
            f"Provider {i:03d}"
            for i in range(1, N_PROVIDERS + 1)
        ],
        "provider_type": provider_types,
        "provider_type_group": np.where(
            provider_types == "Physician",
            "Physician",
            "Advanced Practice Provider",
        ),
        "primary_department_id": provider_department_ids,
        "primary_specialty": [
            department_specialty_map[department_id]
            for department_id in provider_department_ids
        ],
        "active_status": rng.choice(
            ["ACTIVE", "INACTIVE"],
            size=N_PROVIDERS,
            p=[0.97, 0.03],
        ),
        "is_current": rng.choice(
            [1, 0],
            size=N_PROVIDERS,
            p=[0.98, 0.02],
        ),
        "npi": [
            f"900000{i:04d}"
            for i in range(1, N_PROVIDERS + 1)
        ],
        "user_id": [
            f"USER_{i:04d}"
            for i in range(1, N_PROVIDERS + 1)
        ],
    }
)

save_csv(providers, "providers.csv")


# ============================================================
# 3. Calendar
# Grain: one row per calendar date
# ============================================================

calendar_dates = pd.date_range(
    START_DATE,
    END_DATE,
    freq="D",
)

calendar = pd.DataFrame(
    {
        "calendar_date": calendar_dates,
    }
)

calendar["month_begin_date"] = (
    calendar["calendar_date"].dt.to_period("M").dt.start_time
)

calendar["month_end_date"] = (
    calendar["calendar_date"].dt.to_period("M").dt.end_time.dt.normalize()
)

calendar["month_name"] = calendar[
    "calendar_date"
].dt.month_name()

calendar["month_name_short"] = calendar[
    "calendar_date"
].dt.strftime("%b")

calendar["month_year"] = calendar[
    "calendar_date"
].dt.strftime("%b %Y")

calendar["year_month"] = calendar[
    "calendar_date"
].dt.strftime("%Y%m").astype(int)

calendar["year_month_sequence"] = [
    month_difference(date, START_DATE) + 1
    for date in calendar["calendar_date"]
]

calendar["calendar_year"] = calendar[
    "calendar_date"
].dt.year

# Fiscal year begins July 1.
calendar["fiscal_year"] = np.where(
    calendar["calendar_date"].dt.month >= 7,
    calendar["calendar_date"].dt.year + 1,
    calendar["calendar_date"].dt.year,
)

calendar["weekend_flag"] = np.where(
    calendar["calendar_date"].dt.dayofweek >= 5,
    "Y",
    "N",
)

# A small fictional holiday set.
holiday_month_day = {
    (1, 1),
    (7, 4),
    (11, 27),
    (12, 25),
}

calendar["holiday_flag"] = [
    "Y"
    if (date.month, date.day) in holiday_month_day
    else "N"
    for date in calendar["calendar_date"]
]

calendar["business_day_flag"] = np.where(
    calendar["weekend_flag"].eq("N")
    & calendar["holiday_flag"].eq("N"),
    1,
    0,
)

save_csv(calendar, "calendar.csv")


# ============================================================
# 4. Patients
# Grain: one row per valid synthetic patient
# ============================================================

patients = pd.DataFrame(
    {
        "patient_id": [
            f"PAT_{i:07d}"
            for i in range(1, N_PATIENTS + 1)
        ],
        "valid_patient_flag": rng.choice(
            [1, 0],
            size=N_PATIENTS,
            p=[0.995, 0.005],
        ),
    }
)

save_csv(patients, "patients.csv")


# ============================================================
# 5. Appointments
# Grain: one row per appointment/encounter
#
# Confirmed logic:
# wait_days = appointment_date - appointment_made_date
# admin_days = appointment_made_date - referral_entry_date
# ============================================================

department_weights = np.array(
    [
        0.16,  # Family Medicine
        0.14,  # Internal Medicine
        0.11,  # Cardiology
        0.09,  # Neurology
        0.09,  # Gastroenterology
        0.07,  # Endocrinology
        0.09,  # Orthopedics
        0.06,  # General Surgery
        0.08,  # Women's Health
        0.06,  # Dermatology
        0.04,  # Pulmonology
        0.01,  # Trellis, later excluded
    ]
)

appointment_department_ids = rng.choice(
    departments["department_id"],
    size=N_APPOINTMENTS,
    p=department_weights,
)

providers_by_department = {
    department_id: group["provider_id"].tolist()
    for department_id, group
    in providers.groupby("primary_department_id")
}

appointment_provider_ids = []

for department_id in appointment_department_ids:
    available_providers = providers_by_department.get(
        department_id,
        [],
    )

    if available_providers:
        appointment_provider_ids.append(
            rng.choice(available_providers)
        )
    else:
        appointment_provider_ids.append(
            rng.choice(providers["provider_id"])
        )

appointment_made_dates = random_dates(
    START_DATE,
    END_DATE - pd.Timedelta(days=90),
    N_APPOINTMENTS,
).sort_values(ignore_index=True)

# Synthetic wait-day patterns by department.
base_wait_days = {
    101: 8,
    102: 10,
    103: 19,
    104: 29,
    105: 22,
    106: 17,
    107: 15,
    108: 20,
    109: 12,
    110: 16,
    111: 18,
    112: 14,
}

wait_days_values: list[int] = []

for department_id, made_date in zip(
    appointment_department_ids,
    appointment_made_dates,
):
    months_from_start = month_difference(
        made_date,
        START_DATE,
    )

    # Slight systemwide improvement over time.
    improvement = months_from_start * 0.18

    expected_wait = max(
        2,
        base_wait_days[department_id] - improvement,
    )

    calculated_wait = int(
        round(
            rng.normal(
                expected_wait,
                max(expected_wait * 0.28, 2),
            )
        )
    )

    wait_days_values.append(
        max(calculated_wait, 0)
    )

appointment_dates = (
    appointment_made_dates
    + pd.to_timedelta(wait_days_values, unit="D")
)

new_visit_flags = rng.choice(
    [1, 0],
    size=N_APPOINTMENTS,
    p=[0.43, 0.57],
)

has_referral_flags = rng.choice(
    [1, 0],
    size=N_APPOINTMENTS,
    p=[0.70, 0.30],
)

admin_days_values = np.maximum(
    rng.normal(
        loc=7.5,
        scale=3.5,
        size=N_APPOINTMENTS,
    ).round().astype(int),
    0,
)

referral_entry_dates: list[pd.Timestamp | pd.NaT] = []
referral_ids: list[str | None] = []

for index, (
    made_date,
    has_referral,
    admin_days,
) in enumerate(
    zip(
        appointment_made_dates,
        has_referral_flags,
        admin_days_values,
    ),
    start=1,
):
    if has_referral == 1:
        referral_entry_dates.append(
            made_date - pd.Timedelta(days=int(admin_days))
        )
        referral_ids.append(f"REF_{index:07d}")
    else:
        referral_entry_dates.append(pd.NaT)
        referral_ids.append(None)

scheduled_online_probabilities = []

for made_date in appointment_made_dates:
    months_from_start = month_difference(
        made_date,
        START_DATE,
    )

    probability = min(
        0.09 + months_from_start * 0.004,
        0.22,
    )

    scheduled_online_probabilities.append(probability)

scheduled_online_flags = [
    int(rng.random() < probability)
    for probability in scheduled_online_probabilities
]

visit_type_ids = np.where(
    new_visit_flags == 1,
    "VT_NEW",
    rng.choice(
        ["VT_FOLLOWUP", "VT_VIRTUAL", "VT_PROCEDURE"],
        size=N_APPOINTMENTS,
        p=[0.68, 0.22, 0.10],
    ),
)

visit_type_names = np.where(
    visit_type_ids == "VT_NEW",
    "New Patient",
    np.where(
        visit_type_ids == "VT_FOLLOWUP",
        "Follow-Up",
        np.where(
            visit_type_ids == "VT_VIRTUAL",
            "Virtual",
            "Procedure",
        ),
    ),
)

appointments = pd.DataFrame(
    {
        "appointment_id": [
            f"APT_{i:07d}"
            for i in range(1, N_APPOINTMENTS + 1)
        ],
        "patient_encounter_id": [
            f"CSN_{i:09d}"
            for i in range(1, N_APPOINTMENTS + 1)
        ],
        "patient_id": rng.choice(
            patients["patient_id"],
            size=N_APPOINTMENTS,
            replace=True,
        ),
        "department_id": appointment_department_ids,
        "provider_id": appointment_provider_ids,
        "appointment_made_date": appointment_made_dates.dt.date,
        "appointment_date": appointment_dates.dt.date,
        "referral_id": referral_ids,
        "referral_entry_date": pd.to_datetime(
            referral_entry_dates
        ).date,
        "wait_days": wait_days_values,
        "admin_days": np.where(
            has_referral_flags == 1,
            admin_days_values,
            np.nan,
        ),
        "new_visit_flag": new_visit_flags,
        "scheduled_online_flag": scheduled_online_flags,
        "visit_type_id": visit_type_ids,
        "visit_type_name": visit_type_names,
        "new_to_enterprise_flag": rng.choice(
            [1, 0],
            size=N_APPOINTMENTS,
            p=[0.22, 0.78],
        ),
        "new_to_division_flag": rng.choice(
            [1, 0],
            size=N_APPOINTMENTS,
            p=[0.31, 0.69],
        ),
    }
)

save_csv(appointments, "appointments.csv")


# ============================================================
# 6. Survey Questions
# Grain: one row per survey question
# ============================================================

survey_questions = pd.DataFrame(
    [
        [
            "ACCESS_Q1",
            "Ease of getting an appointment",
            "How easy was it to get an appointment?",
            1,
            5,
            1,
            0,
        ],
        [
            "ACCESS_Q2",
            "Ease of scheduling an appointment",
            "How easy was it to schedule your appointment?",
            1,
            5,
            1,
            0,
        ],
        [
            "ACCESS_Q3",
            "Convenience of available appointment times",
            "How convenient were the available appointment times?",
            1,
            5,
            1,
            0,
        ],
        [
            "ACCESS_Q4",
            "Ease of contacting the clinic",
            "How easy was it to contact the clinic?",
            1,
            5,
            1,
            0,
        ],
        [
            "OTHER_Q1",
            "General communication",
            "How would you rate general communication?",
            1,
            5,
            1,
            0,
        ],
    ],
    columns=[
        "survey_question_key",
        "question_name",
        "question_text",
        "minimum_score",
        "maximum_score",
        "press_ganey_source_flag",
        "deleted_flag",
    ],
)

save_csv(survey_questions, "survey_questions.csv")


# ============================================================
# 7. Encounters
# Grain: one row per appointment-linked encounter
# ============================================================

provider_durable_key_map = dict(
    zip(
        providers["provider_id"],
        providers["provider_durable_key"],
    )
)

encounters = pd.DataFrame(
    {
        "encounter_key": np.arange(
            100_001,
            100_001 + len(appointments),
        ),
        "patient_encounter_id": appointments[
            "patient_encounter_id"
        ],
        "provider_durable_key": appointments[
            "provider_id"
        ].map(provider_durable_key_map),
        "encounter_date": appointments["appointment_date"],
    }
)

save_csv(encounters, "encounters.csv")


# ============================================================
# 8. Survey Answers
# Grain: one response to one survey question
# ============================================================

# Patient experience starts February 2025.
eligible_encounters = encounters.loc[
    pd.to_datetime(encounters["encounter_date"])
    >= pd.Timestamp("2025-02-01")
].copy()

survey_encounter_sample = eligible_encounters.sample(
    n=N_SURVEY_ANSWERS,
    replace=True,
    random_state=RANDOM_SEED,
)

survey_question_choices = rng.choice(
    survey_questions["survey_question_key"],
    size=N_SURVEY_ANSWERS,
    p=[0.235, 0.235, 0.235, 0.235, 0.06],
)

numeric_responses = rng.choice(
    [1, 2, 3, 4, 5],
    size=N_SURVEY_ANSWERS,
    p=[0.015, 0.025, 0.075, 0.17, 0.715],
)

survey_answers = pd.DataFrame(
    {
        "survey_answer_key": np.arange(
            500_001,
            500_001 + N_SURVEY_ANSWERS,
        ),
        "survey_question_key": survey_question_choices,
        "encounter_key": survey_encounter_sample[
            "encounter_key"
        ].to_numpy(),
        "provider_durable_key": survey_encounter_sample[
            "provider_durable_key"
        ].to_numpy(),
        "numeric_response": numeric_responses,
        "is_answered": 1,
        "source_top_box_flag": np.where(
            numeric_responses == 5,
            1,
            0,
        ),
        "valid_flag": rng.choice(
            [1, 0],
            size=N_SURVEY_ANSWERS,
            p=[0.995, 0.005],
        ),
    }
)

save_csv(survey_answers, "survey_answers.csv")


# ============================================================
# 9. Online Scheduling
# Grain: provider-department-visit-type-month
# ============================================================

month_starts = pd.date_range(
    START_DATE,
    END_DATE,
    freq="MS",
)

online_scheduling_rows: list[dict] = []

active_providers = providers.loc[
    providers["active_status"].eq("ACTIVE")
].copy()

for month_index, month_start in enumerate(month_starts):
    for provider in active_providers.itertuples():
        denominator = int(
            rng.integers(35, 125)
        )

        base_rate = 0.08 + month_index * 0.0035
        provider_variation = rng.normal(0, 0.018)

        online_rate = float(
            np.clip(
                base_rate + provider_variation,
                0.02,
                0.30,
            )
        )

        numerator = int(
            round(denominator * online_rate)
        )

        online_scheduling_rows.append(
            {
                "month_end_date": (
                    month_start
                    + pd.offsets.MonthEnd(0)
                ).date(),
                "department_id": provider.primary_department_id,
                "provider_id": provider.provider_id,
                "visit_type_id": "VT_NEW",
                "visit_type_name": "New Patient",
                "new_visit_flag": 1,
                "metric_label": "Appt_Sched_PF",
                "scheduling_workflow": rng.choice(
                    [
                        "Direct",
                        "Ticket",
                        "Open",
                        "On My Way",
                    ],
                    p=[0.42, 0.28, 0.20, 0.10],
                ),
                "online_scheduled_count": numerator,
                "online_enabled_count": denominator,
                "online_scheduling_start_date": pd.Timestamp(
                    "2023-01-01"
                ).date(),
            }
        )

online_scheduling = pd.DataFrame(
    online_scheduling_rows
)

save_csv(
    online_scheduling,
    "online_scheduling.csv",
)


# ============================================================
# 10. Patient Growth
# Grain: one acquisition or attrition event
# ============================================================

growth_rows: list[dict] = []

non_trellis_departments = departments.loc[
    departments["region"].ne("Trellis"),
    "department_id",
].to_numpy()

for event_number in range(
    1,
    N_GROWTH_EVENTS + 1,
):
    event_type = rng.choice(
        [
            "Arrived/Acquisition",
            "Attrition",
        ],
        p=[0.62, 0.38],
    )

    patient_id = rng.choice(
        patients["patient_id"]
    )

    department_id = int(
        rng.choice(non_trellis_departments)
    )

    event_date = random_dates(
        START_DATE,
        END_DATE,
        1,
    ).iloc[0]

    growth_rows.append(
        {
            "growth_event_id": (
                f"GROW_{event_number:07d}"
            ),
            "patient_id": patient_id,
            "department_id": department_id,
            "event_date": event_date.date(),
            "event_type": event_type,
            "acquisition_count": (
                1
                if event_type
                == "Arrived/Acquisition"
                else 0
            ),
        }
    )

patient_growth = pd.DataFrame(growth_rows)

save_csv(patient_growth, "patient_growth.csv")


# ============================================================
# 11. Provider Productivity
# Grain: provider x FTE department x month
#
# Confirmed calculation:
# expected hours = CFTE * 8 * business days
# percent patient-facing = regular available / expected hours
# ============================================================

business_days_by_month = (
    calendar.groupby("month_begin_date", as_index=False)
    ["business_day_flag"]
    .sum()
    .rename(
        columns={
            "business_day_flag":
                "business_days_in_month"
        }
    )
)

productivity_rows: list[dict] = []

for provider in active_providers.itertuples():
    clinical_fte = float(
        rng.choice(
            [0.04, 0.10, 0.40, 0.50, 0.60, 0.75, 0.80, 1.00],
            p=[
                0.01,
                0.02,
                0.06,
                0.10,
                0.14,
                0.18,
                0.17,
                0.32,
            ],
        )
    )

    provider_baseline = float(
        np.clip(
            rng.normal(0.56, 0.15),
            0.15,
            1.10,
        )
    )

    for month_row in business_days_by_month.itertuples():
        month_start = pd.Timestamp(
            month_row.month_begin_date
        )

        business_days = int(
            month_row.business_days_in_month
        )

        expected_hours = (
            clinical_fte
            * 8
            * business_days
        )

        monthly_variation = rng.normal(
            0,
            0.035,
        )

        percent_patient_facing = float(
            np.clip(
                provider_baseline
                + monthly_variation,
                0.05,
                1.20,
            )
        )

        regular_available_hours = round(
            expected_hours
            * percent_patient_facing,
            2,
        )

        productivity_rows.append(
            {
                "month_begin_date": month_start.date(),
                "month_end_date": (
                    month_start
                    + pd.offsets.MonthEnd(0)
                ).date(),
                "provider_id": provider.provider_id,
                "fte_department_id": (
                    provider.primary_department_id
                ),
                "clinical_fte": clinical_fte,
                "business_days_in_month": business_days,
                "regular_available_hours": (
                    regular_available_hours
                ),
                "expected_patient_facing_hours": round(
                    expected_hours,
                    2,
                ),
                "percent_patient_facing": round(
                    percent_patient_facing,
                    5,
                ),
                "meets_80_percent_flag": (
                    1
                    if percent_patient_facing >= 0.80
                    else 0
                ),
            }
        )

provider_productivity = pd.DataFrame(
    productivity_rows
)

save_csv(
    provider_productivity,
    "provider_productivity.csv",
)


# ============================================================
# Validation summary
# ============================================================

print("\nValidation summary")
print("-" * 60)

new_appointments = appointments.loc[
    appointments["new_visit_flag"].eq(1)
]

wait_eligible = new_appointments.loc[
    new_appointments["wait_days"].notna()
]

admin_eligible = new_appointments.loc[
    new_appointments["admin_days"].notna()
]

wait_14_rate = (
    wait_eligible["wait_days"].le(14).mean()
)

admin_7_rate = (
    admin_eligible["admin_days"].le(7).mean()
)

median_wait_days = wait_eligible[
    "wait_days"
].median()

access_survey_answers = survey_answers.loc[
    survey_answers["survey_question_key"].isin(
        ACCESS_QUESTION_KEYS
    )
    & survey_answers["valid_flag"].eq(1)
]

top_box_rate = (
    access_survey_answers[
        "numeric_response"
    ].eq(5).mean()
)

online_rate = (
    online_scheduling[
        "online_scheduled_count"
    ].sum()
    / online_scheduling[
        "online_enabled_count"
    ].sum()
)

eligible_productivity = provider_productivity.loc[
    provider_productivity["clinical_fte"].ge(0.05)
    & provider_productivity[
        "regular_available_hours"
    ].gt(0)
]

average_patient_facing = eligible_productivity[
    "percent_patient_facing"
].mean()

providers_meeting_80 = eligible_productivity[
    "meets_80_percent_flag"
].mean()

print(
    f"New appointments: "
    f"{len(new_appointments):,}"
)

print(
    f"Appointments meeting ≤14 wait days: "
    f"{wait_14_rate:.1%}"
)

print(
    f"Appointments meeting ≤7 admin days: "
    f"{admin_7_rate:.1%}"
)

print(
    f"Median wait days: "
    f"{median_wait_days:.1f}"
)

print(
    f"Patient experience top-box rate: "
    f"{top_box_rate:.1%}"
)

print(
    f"Online scheduling rate: "
    f"{online_rate:.1%}"
)

print(
    f"Average patient-facing hours percent: "
    f"{average_patient_facing:.1%}"
)

print(
    f"Providers meeting 80% benchmark: "
    f"{providers_meeting_80:.1%}"
)

print("\nExecutive Summary synthetic datasets created successfully.")
print(f"Output directory: {OUTPUT_DIR}")