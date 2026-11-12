from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .master("local[2]")
    .appName("test")
    .config("spark.driver.memory", "2g")
    .getOrCreate()
)

df = spark.createDataFrame(
    [(1, "Green", 12.5), (2, "Yellow", 8.0), (3, "Green", 21.0)],
    ["trip_id", "service_type", "fare"],
)
df.show()
df.groupBy("service_type").sum("fare").show()

print("Spark version:", spark.version)
input("Open http://localhost:4040 to see the Spark UI, then press Enter to stop...")
spark.stop()
