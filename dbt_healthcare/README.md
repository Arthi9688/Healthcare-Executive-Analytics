# Healthcare Executive Analytics Dashboard

## About the Project

I built this project to learn how a modern analytics engineering workflow comes together using **Snowflake, dbt, the dbt Semantic Layer, and Lightdash**. Instead of building a dashboard directly on top of raw data, I wanted to follow the same approach many organizations are moving toward where data is transformed, metrics are defined once, and dashboards simply consume those reusable metrics.

The project uses a synthetic healthcare dataset inspired by ambulatory healthcare operations. The goal was to build an executive dashboard that helps leaders monitor provider productivity and patient access while following analytics engineering best practices.

Although the data is synthetic, the project structure, modeling approach, and dashboard design are based on real-world healthcare analytics concepts.

---

## Tech Stack

- Snowflake
- dbt Core
- dbt Semantic Layer (MetricFlow)
- Lightdash Cloud
- Git & GitHub
- Visual Studio Code

---

## Project Architecture


Synthetic Healthcare Data → Snowflake → dbt (Staging Models → Dimension Models → Fact Models) → dbt Semantic Layer (MetricFlow) → Lightdash Cloud → Healthcare Executive Analytics Dashboard


---

## dbt Models

### Staging Models

These models clean and prepare the raw data before it's transformed into analytics-ready models.

- stg_appointments
- stg_calendar
- stg_departments
- stg_patients
- stg_provider_productivity
- stg_providers

### Dimension Models

- dim_department
- dim_provider
- time_spine_daily

### Fact Models

- fct_access
- fct_productivity

---

## Semantic Layer

One of the main goals of this project was learning the **dbt Semantic Layer**.

Instead of recreating calculations inside the dashboard, I defined reusable business metrics in the semantic layer so they could be used consistently across different reports. That made the dashboard much cleaner and helped separate the business logic from the visualization layer.

---

## Dashboard

The dashboard is organized into two main sections.

### Productivity

Metrics include:

- Average Patient-Facing %
- Providers Meeting the 80% Patient-Facing Goal
- Provider Count
- Clinical FTE

Visuals include:

- KPI cards
- Monthly productivity trends
- Department productivity scorecard
- Department-level performance comparison

### Access

Metrics include:

- Median Wait Days
- Appointments Meeting the 14-Day Goal
- Appointments Meeting the 7-Day Administrative Goal

Visuals include:

- KPI cards
- Monthly access trends
- Department access scorecard
- Department-level performance comparison

---

## What I Learned

This project taught me much more than building dashboards.

I learned how to organize data into staging, dimension, and fact models using dbt, define reusable business metrics in the Semantic Layer, and build executive dashboards in Lightdash using those centralized metrics.

It also gave me a much better understanding of how modern analytics platforms separate data transformation, business logic, and reporting into independent layers that are easier to maintain and scale.

---

## Why I Built This

I wanted to build something that felt close to what a healthcare analytics team would actually use.

Instead of focusing only on creating charts, I wanted to practice the complete analytics workflow, from data modeling and metric definitions to building an executive dashboard that supports operational decision-making.

This project helped me connect analytics engineering concepts with healthcare reporting and gave me hands-on experience with tools that are becoming increasingly common in modern data teams.

---

## Disclaimer

This project uses **synthetic healthcare data** created for learning and portfolio purposes. It does not contain any real patient or organizational data.
