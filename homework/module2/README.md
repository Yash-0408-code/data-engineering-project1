# Module 2 Homework: Workflow Orchestration with Kestra

Data Engineering Zoomcamp (DataTalksClub), self-paced.

## Approach
- Kestra (Docker Compose) with GCS + BigQuery, flows in `02-workflow-orchestration/flows/`
- Green 2019–2020 and 2021 loaded with Kestra **backfills** of `09_gcp_taxi_scheduled`
- Yellow 2019–2020 bulk-loaded via **Cloud Shell → GCS → BigQuery external table → CTAS**
  (8 GB laptop could not process the large yellow files through Kestra in Docker)
- Deduplication key (`unique_row_id`) aligned with the Kestra flow's 5-column MD5 recipe
  so both loading methods stay idempotent

## Q1. Uncompressed size of yellow_tripdata_2020-12.csv
Ran `08_gcp_taxi` (yellow / 2020 / 12) with `purge_files` disabled; read the size of the
`extract` task output file.
**Answer:** 128.3 MiB

## Q2. Rendered value of `file` (green / 2020 / 04)
`{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv`
**Answer:** green_tripdata_2020-04.csv

## Q3. Yellow rows, 2020
```sql
SELECT COUNT(*) FROM `double-reef-370319.zoomcamp.yellow_tripdata`
WHERE filename LIKE 'yellow_tripdata_2020-%';
```
**Answer:** 24,648,499

## Q4. Green rows, 2020
```sql
SELECT COUNT(*) FROM `double-reef-370319.zoomcamp.green_tripdata`
WHERE filename LIKE 'green_tripdata_2020-%';
```
**Answer:** 1,734,051

## Q5. Yellow rows, March 2021
Loaded with a Kestra backfill (yellow_schedule, 2021-03-01 to 2021-03-31).
```sql
SELECT COUNT(*) FROM `double-reef-370319.zoomcamp.yellow_tripdata`
WHERE filename = 'yellow_tripdata_2021-03.csv';
```
**Answer:** 1,925,152

## Q6. Schedule trigger in New York time
Use a named IANA zone (handles daylight saving), not a fixed offset:
```yaml
timezone: America/New_York
```
**Answer:** Add a `timezone` property set to `America/New_York`

## Lessons learned
- A dedup key is a contract: two pipelines hashing different columns silently created duplicates
- Streaming large uploads from Cloud Shell truncated files at ~110 MB; download-verify-upload fixed it
- Size comparison against the source is a cheap integrity check for file transfers
