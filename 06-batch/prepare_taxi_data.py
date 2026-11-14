import argparse
from pathlib import Path

from pyspark.sql import SparkSession, DataFrame, types as T

GREEN_SCHEMA = T.StructType([
    T.StructField("VendorID", T.IntegerType()),
    T.StructField("lpep_pickup_datetime", T.TimestampType()),
    T.StructField("lpep_dropoff_datetime", T.TimestampType()),
    T.StructField("store_and_fwd_flag", T.StringType()),
    T.StructField("RatecodeID", T.IntegerType()),
    T.StructField("PULocationID", T.IntegerType()),
    T.StructField("DOLocationID", T.IntegerType()),
    T.StructField("passenger_count", T.IntegerType()),
    T.StructField("trip_distance", T.DoubleType()),
    T.StructField("fare_amount", T.DoubleType()),
    T.StructField("extra", T.DoubleType()),
    T.StructField("mta_tax", T.DoubleType()),
    T.StructField("tip_amount", T.DoubleType()),
    T.StructField("tolls_amount", T.DoubleType()),
    T.StructField("ehail_fee", T.DoubleType()),
    T.StructField("improvement_surcharge", T.DoubleType()),
    T.StructField("total_amount", T.DoubleType()),
    T.StructField("payment_type", T.IntegerType()),
    T.StructField("trip_type", T.IntegerType()),
    T.StructField("congestion_surcharge", T.DoubleType()),
])

YELLOW_SCHEMA = T.StructType([
    T.StructField("VendorID", T.IntegerType()),
    T.StructField("tpep_pickup_datetime", T.TimestampType()),
    T.StructField("tpep_dropoff_datetime", T.TimestampType()),
    T.StructField("passenger_count", T.IntegerType()),
    T.StructField("trip_distance", T.DoubleType()),
    T.StructField("RatecodeID", T.IntegerType()),
    T.StructField("store_and_fwd_flag", T.StringType()),
    T.StructField("PULocationID", T.IntegerType()),
    T.StructField("DOLocationID", T.IntegerType()),
    T.StructField("payment_type", T.IntegerType()),
    T.StructField("fare_amount", T.DoubleType()),
    T.StructField("extra", T.DoubleType()),
    T.StructField("mta_tax", T.DoubleType()),
    T.StructField("tip_amount", T.DoubleType()),
    T.StructField("tolls_amount", T.DoubleType()),
    T.StructField("improvement_surcharge", T.DoubleType()),
    T.StructField("total_amount", T.DoubleType()),
    T.StructField("congestion_surcharge", T.DoubleType()),
])

SCHEMAS = {"green": GREEN_SCHEMA, "yellow": YELLOW_SCHEMA}


def read_month(spark: SparkSession, color: str, year: int, month: int) -> DataFrame:
    path = f"data/raw/{color}/{year}/{month:02d}/"
    return spark.read.option("header", True).schema(SCHEMAS[color]).csv(path)


def write_month(df: DataFrame, color: str, year: int, month: int) -> None:
    path = f"data/pq/{color}/{year}/{month:02d}/"
    df.repartition(4).write.mode("overwrite").parquet(path)


def main(color: str, year: int) -> None:
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName(f"prepare_{color}_{year}")
        .config("spark.driver.memory", "2g")
        .getOrCreate()
    )
    for month in range(1, 13):
        if not Path(f"data/raw/{color}/{year}/{month:02d}").exists():
            print(f"{color} {year}-{month:02d}: no raw data, skipping")
            continue
        df = read_month(spark, color, year, month)
        write_month(df, color, year, month)
        print(f"{color} {year}-{month:02d}: written")
    spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert taxi CSVs to Parquet")
    parser.add_argument("--color", required=True, choices=["green", "yellow"])
    parser.add_argument("--year", required=True, type=int)
    args = parser.parse_args()
    main(args.color, args.year)