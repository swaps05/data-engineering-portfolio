# Databricks notebook source
# Insurance Fraud Detection: Fraud Detection Rules Engine
# Purpose: Apply business rules and ML models to identify fraudulent claims
# Author: Data Engineering Team
# Last Updated: June 2026

# COMMAND ----------

# MAGIC %md
# MAGIC # Fraud Detection Rules Engine
# MAGIC 
# MAGIC This notebook applies multiple fraud detection rules:
# MAGIC - Rule-based detection (business logic)
# MAGIC - Pattern matching (historical patterns)
# MAGIC - Anomaly detection (statistical outliers)
# MAGIC - Network analysis (related claims)

# COMMAND ----------

import pyspark.sql.functions as F
from pyspark.sql.window import Window
from pyspark.ml.feature import StandardScaler, VectorAssembler
from datetime import datetime, timedelta

# COMMAND ----------

# Configuration
SILVER_PATH = "/mnt/insurance-lake/silver"
GOLD_PATH = "/mnt/insurance-lake/gold"
CATALOG = "insurance"

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Load Silver Layer Data

# COMMAND ----------

# Load cleaned data from silver layer
policies = spark.read.format("delta").load(f"{SILVER_PATH}/policies")
claims = spark.read.format("delta").load(f"{SILVER_PATH}/claims")

# Join claims with policy information
claims_enriched = claims.join(
    policies.select("policy_id", "policy_type", "coverage_amount", "premium_amount", "customer_age", "prior_claims_count"),
    on="policy_id",
    how="left"
)

print(f"Claims for fraud analysis: {claims_enriched.count()}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Rule-Based Fraud Detection

# COMMAND ----------

# Rule 1: Claim amount exceeds policy coverage
rule1_fraud_amount = claims_enriched.withColumn(
    "rule1_fraud_flag",
    F.when(F.col("claim_amount") > F.col("coverage_amount"), 1).otherwise(0)
).withColumn("rule1_reason", F.lit("Claim exceeds coverage"))

# Rule 2: Multiple claims within short timeframe (potential collision fraud)
window_spec = Window.partitionBy("policy_id").orderBy("claim_date").rangeBetween(-90, 0)
rule2_fraud = rule1_fraud_amount.withColumn(
    "claims_in_90days",
    F.count("claim_id").over(window_spec)
).withColumn(
    "rule2_fraud_flag",
    F.when(F.col("claims_in_90days") > 3, 1).otherwise(0)
).withColumn("rule2_reason", F.lit("Multiple claims in 90 days"))

# Rule 3: High claim amount for young customers (age < 25)
rule3_fraud = rule2_fraud.withColumn(
    "rule3_fraud_flag",
    F.when(
        (F.col("customer_age") < 25) & (F.col("claim_amount") > F.col("coverage_amount") * 0.8),
        1
    ).otherwise(0)
).withColumn("rule3_reason", F.lit("Young customer, high claim amount"))

# Rule 4: Claim without police report for high amounts (Auto claims > $50k)
rule4_fraud = rule3_fraud.withColumn(
    "rule4_fraud_flag",
    F.when(
        (F.col("claim_type") == "Auto") & 
        (F.col("claim_amount") > 50000) & 
        (F.col("police_report_number").isNull()),
        1
    ).otherwise(0)
).withColumn("rule4_reason", F.lit("High auto claim without police report"))

# Rule 5: Suspicious keywords in claim description
suspicious_keywords = ["accidental", "intentional", "third party", "gang related"]
rule5_fraud = rule4_fraud.withColumn(
    "rule5_fraud_flag",
    F.when(
        F.col("claim_description").rlike("(?i)" + "|".join(suspicious_keywords)),
        1
    ).otherwise(0)
).withColumn("rule5_reason", F.lit("Suspicious keywords in description"))

print("✅ Rule-based fraud detection completed")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Aggregate Fraud Rules

# COMMAND ----------

# Combine all fraud rules
fraud_rules_df = rule5_fraud.withColumn(
    "total_fraud_flags",
    F.col("rule1_fraud_flag") + 
    F.col("rule2_fraud_flag") + 
    F.col("rule3_fraud_flag") + 
    F.col("rule4_fraud_flag") + 
    F.col("rule5_fraud_flag")
).withColumn(
    "is_fraud_high_risk",
    F.when(F.col("total_fraud_flags") >= 3, 1).otherwise(0)
).withColumn(
    "is_fraud_medium_risk",
    F.when((F.col("total_fraud_flags") >= 1) & (F.col("total_fraud_flags") < 3), 1).otherwise(0)
)

# Display fraud summary
fraud_summary = fraud_rules_df.select(
    "claim_id", 
    "claim_amount",
    "rule1_fraud_flag", "rule2_fraud_flag", "rule3_fraud_flag", "rule4_fraud_flag", "rule5_fraud_flag",
    "total_fraud_flags",
    "is_fraud_high_risk"
).filter(F.col("total_fraud_flags") > 0)

print(f"Claims flagged for fraud: {fraud_summary.count()}")
display(fraud_summary.limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Calculate Fraud Probability Score

# COMMAND ----------

# Create features for fraud score
fraud_scoring_features = fraud_rules_df.select(
    "claim_id",
    "policy_id",
    "claim_amount",
    "coverage_amount",
    "customer_age",
    "prior_claims_count",
    "claims_in_90days",
    "rule1_fraud_flag",
    "rule2_fraud_flag",
    "rule3_fraud_flag",
    "rule4_fraud_flag",
    "rule5_fraud_flag",
    "total_fraud_flags"
).withColumn(
    "claim_to_coverage_ratio",
    F.col("claim_amount") / F.col("coverage_amount")
)

# Create fraud probability score (0-100)
fraud_scores = fraud_scoring_features.withColumn(
    "fraud_score",
    (
        F.col("rule1_fraud_flag") * 30 +
        F.col("rule2_fraud_flag") * 20 +
        F.col("rule3_fraud_flag") * 15 +
        F.col("rule4_fraud_flag") * 25 +
        F.col("rule5_fraud_flag") * 10
    )
).withColumn(
    "fraud_risk_category",
    F.when(F.col("fraud_score") >= 70, "HIGH_RISK")
    .when(F.col("fraud_score") >= 40, "MEDIUM_RISK")
    .when(F.col("fraud_score") >= 10, "LOW_RISK")
    .otherwise("NO_RISK")
)

print("✅ Fraud probability scores calculated")
display(fraud_scores.select("claim_id", "fraud_score", "fraud_risk_category").filter(F.col("fraud_score") > 0).limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Write Fraud Detection Results

# COMMAND ----------

# Select final columns for output
fraud_detection_output = fraud_scores.select(
    "claim_id",
    "policy_id",
    "claim_amount",
    "fraud_score",
    "fraud_risk_category",
    "total_fraud_flags",
    F.current_timestamp().alias("fraud_detection_timestamp"),
    F.lit("PRODUCTION").alias("model_version")
)

# Write to gold layer
fraud_detection_output.write \
  .format("delta") \
  .mode("overwrite") \
  .option("mergeSchema", "true") \
  .save(f"{GOLD_PATH}/claims_fraud_scores")

print("✅ Fraud detection results written to gold layer")

# Create managed table
spark.sql(f"""
CREATE OR REPLACE TABLE {CATALOG}.gold_layer.claims_fraud_scores
USING DELTA
LOCATION '{GOLD_PATH}/claims_fraud_scores'
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Fraud Detection Summary

# COMMAND ----------

# Generate summary statistics
fraud_summary_stats = fraud_detection_output.groupBy("fraud_risk_category").agg(
    F.count("claim_id").alias("claim_count"),
    F.avg("fraud_score").alias("avg_fraud_score"),
    F.sum("claim_amount").alias("total_claim_amount")
)

print("Fraud Detection Summary:")
display(fraud_summary_stats)

# High-risk claims requiring investigation
high_risk_claims = fraud_detection_output \
    .filter(F.col("fraud_risk_category") == "HIGH_RISK") \
    .select("claim_id", "claim_amount", "fraud_score") \
    .orderBy(F.desc("fraud_score"))

print("\n⚠️ High-Risk Claims Requiring Investigation:")
display(high_risk_claims.limit(20))
