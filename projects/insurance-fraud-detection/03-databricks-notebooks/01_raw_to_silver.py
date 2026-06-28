# Databricks notebook source
# Insurance Fraud Detection: Raw to Silver Layer Transformation
# Purpose: Flatten JSON data from Azure Functions into structured tables
# Author: Data Engineering Team
# Last Updated: June 2026

# COMMAND ----------

# MAGIC %md
# MAGIC # Raw → Silver Layer Transformation
# MAGIC 
# MAGIC This notebook:
# MAGIC 1. Reads raw JSON from ADLS Gen2 Bronze layer
# MAGIC 2. Flattens nested JSON structures
# MAGIC 3. Applies data quality validations
# MAGIC 4. Creates deduplicated Silver layer tables in Delta format
# MAGIC 5. Tracks data lineage

# COMMAND ----------

import pyspark.sql.functions as F
from pyspark.sql.types import *
from datetime import datetime, timedelta
import logging

# COMMAND ----------

# Configuration
BRONZE_PATH = "/mnt/insurance-lake/raw"
SILVER_PATH = "/mnt/insurance-lake/silver"
CATALOG = "insurance"
SCHEMA = "silver_layer"

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Read Raw Policy Data

# COMMAND ----------

# Read raw policy JSON files from bronze layer
raw_policies_df = spark.read \
  .format("json") \
  .option("recursiveFileLookup", "true") \
  .load(f"{BRONZE_PATH}/policy_created") \
  .unionByName(
    spark.read.format("json").option("recursiveFileLookup", "true").load(f"{BRONZE_PATH}/policy_updated"),
    allowMissingColumns=True
  )

print(f"Raw policies loaded: {raw_policies_df.count()} records")
display(raw_policies_df.limit(3))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Flatten and Transform Policy Data

# COMMAND ----------

# Flatten nested JSON and apply transformations
policies_silver = raw_policies_df.select(
    F.col("policy_id").cast("string"),
    F.col("customer_id").cast("string"),
    F.col("policy_number").cast("string"),
    F.col("policy_type").cast("string"),  # Auto, Home, Life, Health
    F.col("coverage_amount").cast("decimal(12,2)"),
    F.col("premium_amount").cast("decimal(12,2)"),
    F.col("start_date").cast("date"),
    F.col("end_date").cast("date"),
    F.col("policy_status").cast("string"),  # Active, Lapsed, Cancelled
    F.col("customer.name").cast("string").alias("customer_name"),
    F.col("customer.age").cast("int").alias("customer_age"),
    F.col("customer.location").cast("string").alias("customer_location"),
    F.col("customer.claim_history_count").cast("int").alias("prior_claims_count"),
    F.col("ingestion_timestamp").cast("timestamp"),
    F.col("event_hash").cast("string"),
    F.current_timestamp().alias("silver_processed_timestamp"),
    F.lit("POLICIES").alias("data_entity")
) \
.filter(F.col("policy_id").isNotNull()) \
.dropDuplicates(["policy_id", "event_hash"])

print(f"Policies after flattening: {policies_silver.count()} unique records")
display(policies_silver.limit(3))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Read and Transform Claims Data

# COMMAND ----------

# Read raw claims JSON
raw_claims_df = spark.read \
  .format("json") \
  .option("recursiveFileLookup", "true") \
  .load(f"{BRONZE_PATH}/claims")

print(f"Raw claims loaded: {raw_claims_df.count()} records")

# Flatten and transform claims
claims_silver = raw_claims_df.select(
    F.col("claim_id").cast("string"),
    F.col("policy_id").cast("string"),
    F.col("customer_id").cast("string"),
    F.col("claim_amount").cast("decimal(12,2)"),
    F.col("claim_date").cast("date"),
    F.col("claim_type").cast("string"),  # Auto, Property, Medical, Life
    F.col("claim_status").cast("string"),  # Filed, Under Review, Approved, Rejected, Paid
    F.col("claim_description").cast("string"),
    F.col("injury_type").cast("string").alias("injury_code"),
    F.col("medical_provider").cast("string"),
    F.col("police_report_number").cast("string"),
    F.col("witness_count").cast("int"),
    F.col("estimated_repair_cost").cast("decimal(12,2)"),
    F.col("ingestion_timestamp").cast("timestamp"),
    F.col("event_hash").cast("string"),
    F.current_timestamp().alias("silver_processed_timestamp"),
    F.lit("CLAIMS").alias("data_entity")
) \
.filter(F.col("claim_id").isNotNull()) \
.dropDuplicates(["claim_id", "event_hash"])

print(f"Claims after flattening: {claims_silver.count()} unique records")
display(claims_silver.limit(3))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Data Quality Validations

# COMMAND ----------

# Validate policies
null_policy_ids = policies_silver.filter(F.col("policy_id").isNull()).count()
null_customer_ids = policies_silver.filter(F.col("customer_id").isNull()).count()
invalid_coverage = policies_silver.filter(F.col("coverage_amount") <= 0).count()

print(f"Policy Quality Checks:")
print(f"  Null policy_id: {null_policy_ids}")
print(f"  Null customer_id: {null_customer_ids}")
print(f"  Invalid coverage amount: {invalid_coverage}")

# Validate claims
null_claim_ids = claims_silver.filter(F.col("claim_id").isNull()).count()
invalid_amount = claims_silver.filter(F.col("claim_amount") <= 0).count()
future_dates = claims_silver.filter(F.col("claim_date") > F.current_date()).count()

print(f"\nClaim Quality Checks:")
print(f"  Null claim_id: {null_claim_ids}")
print(f"  Invalid claim amount: {invalid_amount}")
print(f"  Future claim dates: {future_dates}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Write to Silver Layer (Delta Format)

# COMMAND ----------

# Write policies to silver layer
policies_silver.write \
  .format("delta") \
  .mode("overwrite") \
  .option("mergeSchema", "true") \
  .save(f"{SILVER_PATH}/policies")

print("✅ Policies written to silver layer")

# Write claims to silver layer
claims_silver.write \
  .format("delta") \
  .mode("overwrite") \
  .option("mergeSchema", "true") \
  .save(f"{SILVER_PATH}/claims")

print("✅ Claims written to silver layer")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Create Delta Tables for Analytics

# COMMAND ----------

# Create or replace managed tables
spark.sql(f"""
CREATE OR REPLACE TABLE {CATALOG}.{SCHEMA}.policies
USING DELTA
LOCATION '{SILVER_PATH}/policies'
""")

spark.sql(f"""
CREATE OR REPLACE TABLE {CATALOG}.{SCHEMA}.claims
USING DELTA
LOCATION '{SILVER_PATH}/claims'
""")

# Add table properties for governance
spark.sql(f"""
ALTER TABLE {CATALOG}.{SCHEMA}.policies
SET TBLPROPERTIES (
  'owner' = 'Data Engineering',
  'last_updated' = '{datetime.now().isoformat()}',
  'data_quality_checks' = 'null_checks, range_checks, duplicate_checks'
)
""")

print("✅ Delta tables created and registered")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Summary and Metrics

# COMMAND ----------

# Generate summary metrics
summary = {
    "bronze_to_silver_transformation": {
        "policies_loaded": policies_silver.count(),
        "claims_loaded": claims_silver.count(),
        "policies_columns": len(policies_silver.columns),
        "claims_columns": len(claims_silver.columns),
        "processing_timestamp": datetime.now().isoformat(),
        "status": "SUCCESS"
    }
}

for key, value in summary["bronze_to_silver_transformation"].items():
    print(f"{key}: {value}")
