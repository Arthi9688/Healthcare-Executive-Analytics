# Synthetic Data Specification

## Dataset Size

- 10 departments
- 75 providers
- 8,000 patients
- 30,000 appointment requests
- Approximately 25,000 appointments
- 24 months of provider capacity data

## Divisions

- Primary Care
- Medical Specialties
- Surgical Specialties
- Women's Health

## Specialties

- Family Medicine
- Internal Medicine
- Cardiology
- Neurology
- Orthopedics
- Gastroenterology
- Dermatology
- Endocrinology
- Obstetrics and Gynecology
- General Surgery

## Synthetic Business Patterns

The generated data should contain realistic operational variation:

- Neurology has relatively long scheduling delays.
- Primary Care has high appointment-request volume.
- Cardiology has high provider-capacity utilization.
- Digital scheduling adoption improves over time.
- Urgent requests are scheduled faster than routine requests.
- Some requests never convert into appointments.
- Some scheduled appointments are cancelled or become no-shows.
- One department shows improving access over time.
- One department has available capacity but relatively low demand.

## Data-Quality Scenarios

Include a small number of intentional issues for testing:

- Missing department identifiers
- Invalid appointment statuses
- Appointment dates before request dates
- Duplicate appointment identifiers
- Negative capacity hours

These invalid records should be isolated so dbt tests can demonstrate data-quality controls.