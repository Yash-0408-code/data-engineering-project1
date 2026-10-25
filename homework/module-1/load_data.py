import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg://root:root@localhost:5432/ny_taxi")

trips = pd.read_parquet("data/green_tripdata_2025-11.parquet")
print("green trips:", len(trips))
trips.to_sql("green_taxi_trips", engine, if_exists="replace", index=False)

zones = pd.read_csv("data/taxi_zone_lookup.csv")
print("zones:", len(zones))
zones.to_sql("zones", engine, if_exists="replace", index=False)

print("done")