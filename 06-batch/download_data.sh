#!/bin/bash
set -e

TAXI_TYPE=$1   # yellow or green
YEAR=$2        # e.g. 2020

URL_PREFIX="https://github.com/DataTalksClub/nyc-tlc-data/releases/download"

for MONTH in {1..12}; do
  FMONTH=$(printf "%02d" "${MONTH}")
  URL="${URL_PREFIX}/${TAXI_TYPE}/${TAXI_TYPE}_tripdata_${YEAR}-${FMONTH}.csv.gz"
  LOCAL_DIR="data/raw/${TAXI_TYPE}/${YEAR}/${FMONTH}"
  LOCAL_FILE="${LOCAL_DIR}/${TAXI_TYPE}_tripdata_${YEAR}_${FMONTH}.csv.gz"

  mkdir -p "${LOCAL_DIR}"
  echo "Downloading ${URL}"
  if ! wget -q "${URL}" -O "${LOCAL_FILE}"; then
    echo "  Not available, skipping"
    rm -f "${LOCAL_FILE}"
    rmdir "${LOCAL_DIR}" 2>/dev/null || true
  fi
done