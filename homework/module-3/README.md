# Module 3 Homework: Data Warehousing with BigQuery

## Setup
- Data: NYC yellow taxi trips, January to June 2024 (Parquet), from the NYC TLC site
- Loaded to GCS with a Cloud Shell script (download, then upload; no orchestrator):
  `gs://double-reef-370319-kestra-bucket/yellow_2024/`
- BigQuery dataset: `homework_3` (location `us-central1`)

```sql
-- External table over the Parquet files (schema comes from Parquet itself)
CREATE OR REPLACE EXTERNAL TABLE `double-reef-370319.homework_3.yellow_taxi_external`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://double-reef-370319-kestra-bucket/yellow_2024/yellow_tripdata_2024-*.parquet']
);

-- Regular (materialized) table, not partitioned or clustered
CREATE OR REPLACE TABLE `double-reef-370319.homework_3.yellow_taxi_native` AS
SELECT * FROM `double-reef-370319.homework_3.yellow_taxi_external`;
```

## Q1. Count of records for the 2024 yellow taxi data
```sql
SELECT COUNT(*) FROM `double-reef-370319.homework_3.yellow_taxi_native`;
```
**Answer:** 20,332,093

## Q2. Estimated bytes for distinct PULocationID: external vs materialized table
```sql
SELECT COUNT(DISTINCT PULocationID) FROM `double-reef-370319.homework_3.yellow_taxi_external`;
SELECT COUNT(DISTINCT PULocationID) FROM `double-reef-370319.homework_3.yellow_taxi_native`;
```
**Answer:** 0 MB for the external table, 155.12 MB for the materialized table.
BigQuery cannot estimate external data in advance because the files live in GCS;
the native table's size is known from its own storage.

## Q3. Why do estimates differ for PULocationID vs PULocationID, DOLocationID?
```sql
SELECT PULocationID FROM `double-reef-370319.homework_3.yellow_taxi_native`;
SELECT PULocationID, DOLocationID FROM `double-reef-370319.homework_3.yellow_taxi_native`;
```
**Answer:** BigQuery is a columnar database: it reads only the columns a query references,
so selecting two columns reads both columns' data and roughly doubles the bytes.

## Q4. Trips with fare_amount = 0
```sql
SELECT COUNT(*) FROM `double-reef-370319.homework_3.yellow_taxi_native`
WHERE fare_amount = 0;
```
**Answer:** 8,333

## Q5. Best strategy: always filter on tpep_dropoff_datetime, order by VendorID
Filter column → partition; ordering/secondary column → cluster.
```sql
CREATE OR REPLACE TABLE `double-reef-370319.homework_3.yellow_taxi_optimized`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `double-reef-370319.homework_3.yellow_taxi_native`;
```
**Answer:** Partition by tpep_dropoff_datetime and cluster on VendorID

## Q6. Distinct VendorIDs, drop-off 2024-03-01 to 2024-03-15 (inclusive): estimated bytes
```sql
SELECT DISTINCT VendorID FROM `double-reef-370319.homework_3.yellow_taxi_native`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

SELECT DISTINCT VendorID FROM `double-reef-370319.homework_3.yellow_taxi_optimized`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';
```
**Answer:** 310.24 MB (non-partitioned) vs 26.84 MB (partitioned): about 12x fewer bytes,
because only 15 daily partitions are read (about 15/182 of the data).

Note: `DATE(...) BETWEEN` is used because `tpep_dropoff_datetime <= '2024-03-15'` means
2024-03-15 00:00:00 and would exclude the rest of March 15.

## Q7. Where is the data of the external table stored?
**Answer:** In the GCS bucket. BigQuery stores only the table definition (schema and file location).

## Q8. Is it best practice to always cluster your data?
**Answer:** False. Clustering adds little on small tables (under about 1 GB), on columns rarely
used in filters, or on very low-cardinality columns.

## Q9 (bonus). Estimated bytes for SELECT COUNT(*) on the materialized table, and why
**Answer:** 0 B. BigQuery stores each native table's row count in its metadata, so a `COUNT(*)`
without filters is answered without scanning any data. Adding a filter (Q4) requires reading
the filtered column.

