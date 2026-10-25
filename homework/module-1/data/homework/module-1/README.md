# Module 1 Homework: Docker, SQL and Terraform

Data Engineering Zoomcamp (DataTalksClub), self-paced.
Data: NYC green taxi trips, November 2025, loaded into Postgres 18 (Docker Compose) with `load_data.py`.

## Question 1. Understanding Docker images
```bash
docker run -it --rm --entrypoint=bash python:3.13
pip --version
```
**Answer:** 26.2.2 (current image; the cohort options reflected an older image)

## Question 2. Docker networking and docker-compose
pgAdmin runs inside the Compose network, so it reaches Postgres by service or container name,
on the container port (right side of `5433:5432`).

**Answer:** `postgres:5432` (`db:5432` also works)

## Question 3. Counting short trips
```sql
SELECT COUNT(*)
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime <  '2025-12-01'
  AND trip_distance <= 1;
```
**Answer:** 8,007

## Question 4. Longest trip for each day
```sql
SELECT DATE(lpep_pickup_datetime) AS pickup_day,
       MAX(trip_distance) AS longest_trip
FROM green_taxi_trips
WHERE trip_distance < 100
GROUP BY pickup_day
ORDER BY longest_trip DESC
LIMIT 1;
```
**Answer:** 2025-11-14

## Question 5. Biggest pickup zone
```sql
SELECT z."Zone" AS pickup_zone,
       SUM(t.total_amount) AS total
FROM green_taxi_trips t
JOIN zones z ON t."PULocationID" = z."LocationID"
WHERE t.lpep_pickup_datetime >= '2025-11-18'
  AND t.lpep_pickup_datetime <  '2025-11-19'
GROUP BY z."Zone"
ORDER BY total DESC
LIMIT 1;
```
**Answer:** East Harlem North

## Question 6. Largest tip
```sql
SELECT dz."Zone" AS dropoff_zone,
       MAX(t.tip_amount) AS max_tip
FROM green_taxi_trips t
JOIN zones pz ON t."PULocationID" = pz."LocationID"
JOIN zones dz ON t."DOLocationID" = dz."LocationID"
WHERE pz."Zone" = 'East Harlem North'
  AND t.lpep_pickup_datetime >= '2025-11-01'
  AND t.lpep_pickup_datetime <  '2025-12-01'
GROUP BY dz."Zone"
ORDER BY max_tip DESC
LIMIT 1;
```
**Answer:** Yorkville West

## Question 7. Terraform workflow
Terraform files: [`../../terraform`](../../terraform)

**Answer:** `terraform init`, `terraform apply -auto-approve`, `terraform destroy`