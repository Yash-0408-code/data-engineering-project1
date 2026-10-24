variable "credentials" {
  description = "Path to the service account key"
  default     = "/home/velpu/.gc/my-creds.json"
}

variable "project" {
  description = "GCP Project ID"
  default     = "double-reef-370319"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "Location for bucket and dataset"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "BigQuery dataset name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "GCS bucket name (globally unique)"
  default     = "double-reef-370319-terra-bucket"
}
