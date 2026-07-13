# Data Model

## Objective

Design a simple healthcare analytics model that supports executive questions about:

- Patient access
- Provider capacity
- Appointment completion
- Digital scheduling
- New-patient demand
- Department performance

The model uses entirely synthetic data and contains no protected health information.

---

## Core Business Entities

### 1. Departments

Represents ambulatory practices or specialty departments.

**Grain:** One row per department.

| Column | Description |
|---|---|
| department_id | Unique department identifier |
| department_name | Fictional department name |
| division_name | Broader operational division |
| region_name | Geographic or administrative region |
| specialty_name | Medical specialty |
| active_flag | Whether the department is active |

---

### 2. Providers

Represents clinicians working within departments.

**Grain:** One row per provider.

| Column | Description |
|---|---|
| provider_id | Unique provider identifier |
| provider_name | Synthetic provider label |
| department_id | Department assignment |
| provider_type | Physician, APP, or other provider type |
| fte | Full-time-equivalent value |
| active_flag | Whether the provider is active |

---

### 3. Patients

Represents synthetic ambulatory patients.

**Grain:** One row per patient.

| Column | Description |
|---|---|
| patient_id | Synthetic patient identifier |
| age_group | Patient age category |
| gender | Synthetic demographic category |
| region_name | Patient region |
| created_date | Date patient entered the system |

No names, addresses, dates of birth, or real identifiers will be used.

---

### 4. Appointment Requests

Represents demand for ambulatory appointments.

**Grain:** One row per appointment request.

| Column | Description |
|---|---|
| request_id | Unique appointment-request identifier |
| patient_id | Patient requesting care |
| department_id | Requested department |
| request_date | Date the request was created |
| patient_type | New or established patient |
| request_channel | Phone, portal, referral, or self-scheduling |
| priority | Routine, urgent, or high priority |

---

### 5. Appointments

Represents scheduled ambulatory visits.

**Grain:** One row per appointment.

| Column | Description |
|---|---|
| appointment_id | Unique appointment identifier |
| request_id | Related appointment request |
| provider_id | Scheduled provider |
| scheduled_date | Date appointment was booked |
| appointment_date | Date care was scheduled to occur |
| appointment_status | Completed, cancelled, no-show, or scheduled |
| visit_type | New patient, follow-up, virtual, or procedure |
| scheduling_channel | Phone, portal, staff, or self-scheduling |

---

### 6. Provider Monthly Capacity

Represents available and utilized provider time.

**Grain:** One row per provider per month.

| Column | Description |
|---|---|
| provider_id | Provider identifier |
| month_start | Reporting month |
| available_hours | Total available clinical hours |
| booked_hours | Hours associated with booked appointments |
| patient_facing_hours | Hours designated for patient-facing work |

---

## Relationships

```text
Departments
    |
    | one-to-many
    v
Providers

Departments
    |
    | one-to-many
    v
Appointment Requests

Patients
    |
    | one-to-many
    v
Appointment Requests

Appointment Requests
    |
    | zero-or-one to one-or-many
    v
Appointments

Providers
    |
    | one-to-many
    v
Appointments

Providers
    |
    | one-to-many
    v
Provider Monthly Capacity