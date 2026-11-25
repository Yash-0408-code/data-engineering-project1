import argparse

from pyspark.sql import SparkSession, functions as F

parser = argparse.ArgumentParser()
parser.add_argument("--input_green", required=True)
parser.add_argument("--input_yellow", required=True)
parser.add_argument("--output", required=False, help="Parquet output path")
parser.add_argument("--output_table", required=False, help="BigQuery table: dataset.table")
parser.add_argument("--temp_bucket", required=False, help="GCS bucket for BigQuery writes")
args = parser.parse_args()

spark = SparkSession.builder.appName("taxi_revenue_report").getOrCreate()

df_green = (
    spark.read.parquet(args.input_green)
    .withColumnRenamed("lpep_pickup_datetime", "pickup_datetime")
    .withColumnRenamed("lpep_dropoff_datetime", "dropoff_datetime")
)
df_yellow = (
    spark.read.parquet(args.input_yellow)
    .withColumnRenamed("tpep_pickup_datetime", "pickup_datetime")
    .withColumnRenamed("tpep_dropoff_datetime", "dropoff_datetime")
)

yellow_columns = set(df_yellow.columns)
common_columns = [c for c in df_green.columns if c in yellow_columns]

df_trips = (
    df_green.select(common_columns).withColumn("service_type", F.lit("green"))
    .unionAll(df_yellow.select(common_columns).withColumn("service_type", F.lit("yellow")))
)
df_trips.createOrReplaceTempView("trips_data")

df_revenue = spark.sql("""
    SELECT
        PULocationID AS revenue_zone,
        date_trunc('month', pickup_datetime) AS revenue_month,
        service_type,
        SUM(fare_amount) AS revenue_monthly_fare,
        SUM(extra) AS revenue_monthly_extra,
        SUM(mta_tax) AS revenue_monthly_mta_tax,
        SUM(tip_amount) AS revenue_monthly_tip_amount,
        SUM(tolls_amount) AS revenue_monthly_tolls_amount,
        SUM(improvement_surcharge) AS revenue_monthly_improvement_surcharge,
        SUM(total_amount) AS revenue_monthly_total_amount,
        SUM(congestion_surcharge) AS revenue_monthly_congestion_surcharge,
        AVG(passenger_count) AS avg_monthly_passenger_count,
        AVG(trip_distance) AS avg_monthly_trip_distance
    FROM trips_data
    GROUP BY 1, 2, 3
""")

if args.output:
    df_revenue.coalesce(1).write.mode("overwrite").parquet(args.output)

if args.output_table:
    (df_revenue.write.format("bigquery")
        .option("table", args.output_table)
        .option("temporaryGcsBucket", args.temp_bucket)
        .mode("overwrite")
        .save())

spark.stop()