from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

SEED = 42
rng = np.random.default_rng(SEED)

OUTPUT_DIR = Path(__file__).resolve().parent / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

START_DATE = pd.Timestamp("2024-07-01")
END_DATE = pd.Timestamp("2026-06-30")

N_DEPARTMENTS = 10
N_PROVIDERS = 75
N_PATIENTS = 8_000
N_REQUESTS = 30_000


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def random_dates(
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    count: int,
) -> pd.Series:
    """Generate random dates between start_date and end_date."""
    total_days = (end_date - start_date).days
    offsets = rng.integers(0, total_days + 1, size=count)
    return pd.Series(start_date + pd.to_timedelta(offsets, unit="D"))


def save_csv(df: pd.DataFrame, filename: str) -> None:
    path = OUTPUT_DIR / filename
    df.to_csv(path, index=False)
    print(f"Created {filename}: {len(df):,} rows")


# ---------------------------------------------------------
# Departments
# ---------------------------------------------------------

departments = pd.DataFrame(
    [
        [1, "North Family Medicine", "Primary Care", "North", "Family Medicine", True],
        [2, "Central Internal Medicine", "Primary Care", "Central", "Internal Medicine", True],
        [3, "East Cardiology", "Medical Specialties", "East", "Cardiology", True],
        [4, "North Neurology", "Medical Specialties", "North", "Neurology", True],
        [5, "Central Gastroenterology", "Medical Specialties", "Central", "Gastroenterology", True],
        [6, "West Endocrinology", "Medical Specialties", "West", "Endocrinology", True],
        [7, "East Orthopedics", "Surgical Specialties", "East", "Orthopedics", True],
        [8, "South General Surgery", "Surgical Specialties", "South", "General Surgery", True],
        [9, "Central Women's Health", "Women's Health", "Central", "Obstetrics and Gynecology", True],
        [10, "West Dermatology", "Medical Specialties", "West", "Dermatology", True],
    ],
    columns=[
        "department_id",
        "department_name",
        "division_name",
        "region_name",
        "specialty_name",
        "active_flag",
    ],
)

save_csv(departments, "raw_departments.csv")


# ---------------------------------------------------------
# Providers
# ---------------------------------------------------------

provider_department_ids = rng.choice(
    departments["department_id"],
    size=N_PROVIDERS,
    replace=True,
)

provider_types = rng.choice(
    ["Physician", "APP"],
    size=N_PROVIDERS,
    p=[0.72, 0.28],
)

providers = pd.DataFrame(
    {
        "provider_id": [f"PROV_{i:04d}" for i in range(1, N_PROVIDERS + 1)],
        "provider_name": [f"Provider {i:03d}" for i in range(1, N_PROVIDERS + 1)],
        "department_id": provider_department_ids,
        "provider_type": provider_types,
        "fte": rng.choice(
            [0.5, 0.6, 0.75, 0.8, 1.0],
            size=N_PROVIDERS,
            p=[0.05, 0.08, 0.12, 0.15, 0.60],
        ),
        "active_flag": rng.choice(
            [True, False],
            size=N_PROVIDERS,
            p=[0.96, 0.04],
        ),
    }
)

save_csv(providers, "raw_providers.csv")


# ---------------------------------------------------------
# Patients
# ---------------------------------------------------------

patients = pd.DataFrame(
    {
        "patient_id": [f"PAT_{i:06d}" for i in range(1, N_PATIENTS + 1)],
        "age_group": rng.choice(
            ["0-17", "18-34", "35-49", "50-64", "65-79", "80+"],
            size=N_PATIENTS,
            p=[0.12, 0.18, 0.20, 0.24, 0.20, 0.06],
        ),
        "gender": rng.choice(
            ["Female", "Male", "Nonbinary", "Unknown"],
            size=N_PATIENTS,
            p=[0.50, 0.47, 0.01, 0.02],
        ),
        "region_name": rng.choice(
            ["North", "Central", "East", "South", "West"],
            size=N_PATIENTS,
        ),
        "created_date": random_dates(
            pd.Timestamp("2018-01-01"),
            END_DATE,
            N_PATIENTS,
        ).dt.date,
    }
)

save_csv(patients, "raw_patients.csv")


# ---------------------------------------------------------
# Appointment Requests
# ---------------------------------------------------------

department_weights = np.array(
    [
        0.17,  # Family Medicine - high demand
        0.14,  # Internal Medicine - high demand
        0.11,  # Cardiology
        0.09,  # Neurology
        0.10,  # Gastroenterology
        0.07,  # Endocrinology
        0.10,  # Orthopedics
        0.06,  # General Surgery
        0.09,  # Women's Health
        0.07,  # Dermatology
    ]
)

request_dates = random_dates(START_DATE, END_DATE, N_REQUESTS)
request_dates = request_dates.sort_values(ignore_index=True)

request_department_ids = rng.choice(
    departments["department_id"],
    size=N_REQUESTS,
    p=department_weights,
)

request_channels: list[str] = []

for request_date in request_dates:
    months_since_start = (
        (request_date.year - START_DATE.year) * 12
        + request_date.month
        - START_DATE.month
    )

    digital_probability = min(0.15 + months_since_start * 0.012, 0.42)

    request_channels.append(
        rng.choice(
            ["phone", "portal", "referral", "self_schedule"],
            p=[
                0.46 - digital_probability / 2,
                0.18 + digital_probability / 4,
                0.26,
                0.10 + digital_probability / 4,
            ],
        )
    )

appointment_requests = pd.DataFrame(
    {
        "request_id": [f"REQ_{i:07d}" for i in range(1, N_REQUESTS + 1)],
        "patient_id": rng.choice(
            patients["patient_id"],
            size=N_REQUESTS,
            replace=True,
        ),
        "department_id": request_department_ids,
        "request_date": request_dates.dt.date,
        "patient_type": rng.choice(
            ["New", "Established"],
            size=N_REQUESTS,
            p=[0.38, 0.62],
        ),
        "request_channel": request_channels,
        "priority": rng.choice(
            ["Routine", "Urgent", "High"],
            size=N_REQUESTS,
            p=[0.78, 0.17, 0.05],
        ),
    }
)

save_csv(appointment_requests, "raw_appointment_requests.csv")


# ---------------------------------------------------------
# Appointments
# ---------------------------------------------------------

# Approximately 84% of requests convert into appointments.
converted_requests = appointment_requests.sample(
    frac=0.84,
    random_state=SEED,
).copy()

department_delay = {
    1: 5,   # Family Medicine
    2: 7,   # Internal Medicine
    3: 12,  # Cardiology
    4: 22,  # Neurology - intentionally longer
    5: 15,  # Gastroenterology
    6: 13,  # Endocrinology
    7: 11,  # Orthopedics
    8: 16,  # General Surgery
    9: 9,   # Women's Health
    10: 14, # Dermatology
}

priority_multiplier = {
    "Routine": 1.0,
    "Urgent": 0.45,
    "High": 0.25,
}

days_to_schedule: list[int] = []

for row in converted_requests.itertuples():
    base_delay = department_delay[row.department_id]
    multiplier = priority_multiplier[row.priority]

    delay = max(
        0,
        int(rng.normal(base_delay * multiplier, max(base_delay * 0.30, 1))),
    )
    days_to_schedule.append(delay)

converted_requests["days_to_schedule"] = days_to_schedule
converted_requests["request_date"] = pd.to_datetime(
    converted_requests["request_date"]
)

converted_requests["scheduled_date"] = (
    converted_requests["request_date"]
    + pd.to_timedelta(converted_requests["days_to_schedule"], unit="D")
)

appointment_lead_days = rng.integers(
    1,
    46,
    size=len(converted_requests),
)

converted_requests["appointment_date"] = (
    converted_requests["scheduled_date"]
    + pd.to_timedelta(appointment_lead_days, unit="D")
)

# Assign a provider from the requested department.
providers_by_department = {
    department_id: group["provider_id"].tolist()
    for department_id, group in providers.groupby("department_id")
}

assigned_providers = []

for department_id in converted_requests["department_id"]:
    available_providers = providers_by_department.get(department_id)

    if not available_providers:
        assigned_providers.append(rng.choice(providers["provider_id"]))
    else:
        assigned_providers.append(rng.choice(available_providers))

converted_requests["provider_id"] = assigned_providers

converted_requests["appointment_status"] = rng.choice(
    ["Completed", "Cancelled", "No Show", "Scheduled"],
    size=len(converted_requests),
    p=[0.76, 0.10, 0.06, 0.08],
)

converted_requests["visit_type"] = np.where(
    converted_requests["patient_type"].eq("New"),
    "New Patient",
    rng.choice(
        ["Follow-Up", "Virtual", "Procedure"],
        size=len(converted_requests),
        p=[0.68, 0.22, 0.10],
    ),
)

converted_requests["scheduling_channel"] = np.where(
    converted_requests["request_channel"].eq("self_schedule"),
    "Self-Scheduling",
    np.where(
        converted_requests["request_channel"].eq("portal"),
        "Portal",
        rng.choice(
            ["Phone", "Staff"],
            size=len(converted_requests),
            p=[0.60, 0.40],
        ),
    ),
)

appointments = pd.DataFrame(
    {
        "appointment_id": [
            f"APT_{i:07d}" for i in range(1, len(converted_requests) + 1)
        ],
        "request_id": converted_requests["request_id"].values,
        "provider_id": converted_requests["provider_id"].values,
        "scheduled_date": converted_requests["scheduled_date"].dt.date,
        "appointment_date": converted_requests["appointment_date"].dt.date,
        "appointment_status": converted_requests["appointment_status"].values,
        "visit_type": converted_requests["visit_type"].values,
        "scheduling_channel": converted_requests[
            "scheduling_channel"
        ].values,
    }
)

save_csv(appointments, "raw_appointments.csv")


# ---------------------------------------------------------
# Provider Monthly Capacity
# ---------------------------------------------------------

month_starts = pd.date_range(
    START_DATE,
    END_DATE,
    freq="MS",
)

capacity_rows: list[dict] = []

specialty_utilization = {
    "Family Medicine": 0.88,
    "Internal Medicine": 0.85,
    "Cardiology": 0.94,
    "Neurology": 0.97,
    "Gastroenterology": 0.91,
    "Endocrinology": 0.82,
    "Orthopedics": 0.90,
    "General Surgery": 0.86,
    "Obstetrics and Gynecology": 0.87,
    "Dermatology": 0.72,  # Available capacity but lower demand
}

provider_details = providers.merge(
    departments[
        ["department_id", "specialty_name"]
    ],
    on="department_id",
    how="left",
)

for provider in provider_details.itertuples():
    for month_start in month_starts:
        available_hours = round(
            160 * provider.fte * rng.uniform(0.88, 1.02),
            2,
        )

        expected_utilization = specialty_utilization[
            provider.specialty_name
        ]

        utilization = np.clip(
            rng.normal(expected_utilization, 0.06),
            0.45,
            1.05,
        )

        booked_hours = round(available_hours * utilization, 2)

        patient_facing_hours = round(
            available_hours * rng.uniform(0.70, 0.90),
            2,
        )

        capacity_rows.append(
            {
                "provider_id": provider.provider_id,
                "month_start": month_start.date(),
                "available_hours": available_hours,
                "booked_hours": booked_hours,
                "patient_facing_hours": patient_facing_hours,
            }
        )

provider_monthly_capacity = pd.DataFrame(capacity_rows)

save_csv(
    provider_monthly_capacity,
    "raw_provider_monthly_capacity.csv",
)


# ---------------------------------------------------------
# Completion summary
# ---------------------------------------------------------

print("\nSynthetic healthcare dataset created successfully.")
print(f"Output directory: {OUTPUT_DIR}")