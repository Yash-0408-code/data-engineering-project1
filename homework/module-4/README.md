# Module 4 Homework: Analytics Engineering with dbt

## Setup
- dbt Core 1.12 with the BigQuery adapter, installed with uv in `04-analytics-engineering/`
- Project: `04-analytics-engineering/taxi_rides_ny`
- Sources: green and yellow taxi 2019 to 2020 in BigQuery (`zoomcamp` dataset)
- Layers: staging (views) → intermediate (`int_trips_unioned`) → marts (`fct_trips` partitioned by month
  and clustered, `dim_zones` from a seed, `fct_monthly_zone_revenue`)
- Tests: generic, singular and `dbt_utils.accepted_range`; packages: dbt_utils, codegen
- Built with `dbt build --target prod` into the `dbt_prod` dataset

## Q1. `dbt run --select int_trips_unioned` builds which models?
**Answer:** `int_trips_unioned` only. Without `+`, only the selected model is built
(`+model` adds upstream, `model+` adds downstream).

## Q2. A new value `6` appears in `payment_type` with `accepted_values: [1, 2, 3, 4, 5]`
**Answer:** dbt fails the test, returning a non-zero exit code. Tests default to severity `error`.

## Q3. Count of records in `fct_monthly_zone_revenue`
```sql
SELECT COUNT(*) FROM `double-reef-370319.dbt_prod.fct_monthly_zone_revenue`;
```
**My result:** 12,104 → **Answer: 12,184** (closest).
My `fct_trips` excludes trips with unknown pickup zones (inner join to `dim_zones`, `borough != 'Unknown'`),
while the course model keeps them as 'Unknown Zone', which removes about 80 zone-month groups.

## Q4. Pickup zone with the highest revenue for Green taxis in 2020
```sql
SELECT pickup_zone, ROUND(SUM(revenue_monthly_total_amount), 2) AS total_revenue_2020
FROM `double-reef-370319.dbt_prod.fct_monthly_zone_revenue`
WHERE service_type = 'Green'
  AND revenue_month >= '2020-01-01' AND revenue_month < '2021-01-01'
GROUP BY pickup_zone
ORDER BY total_revenue_2020 DESC
LIMIT 5;
```
**Answer:** East Harlem North (1,827,081.39)

## Q5. Total Green taxi trips in October 2019
```sql
SELECT SUM(total_monthly_trips) AS green_trips_oct_2019
FROM `double-reef-370319.dbt_prod.fct_monthly_zone_revenue`
WHERE service_type = 'Green' AND revenue_month = '2019-10-01';
```
**My result:** 384,890 → **Answer: 384,624** (closest).
My model keeps duplicate trip IDs (flagged as a warning by the `unique` test), while the course model
de-duplicates them.



