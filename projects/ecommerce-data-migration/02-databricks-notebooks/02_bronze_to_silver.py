# Databricks notebook source
# E-Commerce Data Migration: Bronze to Silver Transformation
# Purpose: Clean, deduplicate, and prepare data from SQL Server extracts
# Author: Data Engineering Team
# Last Updated: June 2026

# COMMAND ----------

# MAGIC %md
# MAGIC # Bronze → Silver: Data Cleaning & Deduplication
# MAGIC 
# MAGIC Process:
# MAGIC 1. Load raw parquet files from ADLS Bronze layer
# MAGIC 2. Apply data cleaning & standardization
# MAGIC 3. Remove duplicates & handle missing values
# MAGIC 4. Create Delta tables in Silver layer
# MAGIC 5. Validate quality metrics

# COMMAND ----------

import pyspark.sql.functions as F
from pyspark.sql.window import Window
from datetime import datetime

# Configuration
BRONZE_PATH = "/mnt/ecommerce-lake/bronze"
SILVER_PATH = "/mnt/ecommerce-lake/silver"

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Load Orders Data

# COMMAND ----------

# Read orders from SQL Server parquet extract
orders_bronze = spark.read.parquet(f"{BRONZE_PATH}/orders")

print(f"Total order records: {orders_bronze.count()}")
print(f"Schema: {orders_bronze.printSchema()}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Clean Orders Data

# COMMAND ----------

orders_silver = orders_bronze.select(
    F.col("OrderID").cast("string").alias("order_id"),
    F.col("CustomerID").cast("string").alias("customer_id"),
    F.col("OrderDate").cast("date").alias("order_date"),
    F.col("OrderAmount").cast("decimal(12,2)").alias("order_amount"),
    F.col("Currency").cast("string").alias("currency"),
    F.col("OrderStatus").cast("string").alias("order_status"),  # Pending, Confirmed, Shipped, Delivered, Cancelled
    F.col("ShippingAddress").cast("string").alias("shipping_address"),
    F.col("ShippingCountry").cast("string").alias("shipping_country"),
    F.col("PaymentMethod").cast("string").alias("payment_method"),
    F.col("CreatedDate").cast("timestamp").alias("created_date"),
    F.col("UpdatedDate").cast("timestamp").alias("updated_date")
) \
.filter(F.col("order_id").isNotNull() & F.col("customer_id").isNotNull()) \
.filter(F.col("order_amount") > 0) \
.filter(F.col("order_date") <= F.current_date()) \
.dropDuplicates(["order_id"])  # Remove exact duplicates

# Handle null dates
orders_silver = orders_silver.fillna({
    "updated_date": F.col("created_date"),
    "shipping_country": "UNKNOWN"
})

print(f"Orders after cleaning: {orders_silver.count()}")
display(orders_silver.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Clean Products Data

# COMMAND ----------

# Load products
products_bronze = spark.read.parquet(f"{BRONZE_PATH}/products")

products_silver = products_bronze.select(
    F.col("ProductID").cast("string").alias("product_id"),
    F.col("ProductName").cast("string").alias("product_name"),
    F.col("Category").cast("string").alias("category"),
    F.col("Subcategory").cast("string").alias("subcategory"),
    F.col("Price").cast("decimal(10,2)").alias("price"),
    F.col("Cost").cast("decimal(10,2)").alias("cost"),
    F.col("SKU").cast("string").alias("sku"),
    F.col("CurrentStock").cast("int").alias("current_stock"),
    F.col("ReorderLevel").cast("int").alias("reorder_level"),
    F.col("IsActive").cast("boolean").alias("is_active"),
    F.col("CreatedDate").cast("timestamp").alias("created_date")
) \
.filter(F.col("product_id").isNotNull()) \
.filter(F.col("price") >= 0) \
.dropDuplicates(["product_id"])

# Calculate profit margin
products_silver = products_silver.withColumn(
    "profit_margin_pct",
    F.round(((F.col("price") - F.col("cost")) / F.col("price") * 100), 2)
)

print(f"Products after cleaning: {products_silver.count()}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Clean Customers Data

# COMMAND ----------

customers_bronze = spark.read.parquet(f"{BRONZE_PATH}/customers")

customers_silver = customers_bronze.select(
    F.col("CustomerID").cast("string").alias("customer_id"),
    F.col("FirstName").cast("string").alias("first_name"),
    F.col("LastName").cast("string").alias("last_name"),
    F.col("Email").cast("string").alias("email"),
    F.col("Country").cast("string").alias("country"),
    F.col("City").cast("string").alias("city"),
    F.col("JoinDate").cast("date").alias("join_date"),
    F.col("TotalOrders").cast("int").alias("total_orders"),
    F.col("LifetimeValue").cast("decimal(12,2)").alias("lifetime_value"),
    F.col("IsActive").cast("boolean").alias("is_active")
) \
.filter(F.col("customer_id").isNotNull()) \
.filter(F.col("email").isNotNull()) \
.dropDuplicates(["customer_id"])

# Create customer name field
customers_silver = customers_silver.withColumn(
    "full_name",
    F.concat_ws(" ", F.col("first_name"), F.col("last_name"))
)

print(f"Customers after cleaning: {customers_silver.count()}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Load Inventory Data (Real-time)

# COMMAND ----------

inventory_bronze = spark.read.parquet(f"{BRONZE_PATH}/inventory")

inventory_silver = inventory_bronze.select(
    F.col("InventoryID").cast("string").alias("inventory_id"),
    F.col("ProductID").cast("string").alias("product_id"),
    F.col("WarehouseID").cast("string").alias("warehouse_id"),
    F.col("Quantity").cast("int").alias("quantity"),
    F.col("LastUpdated").cast("timestamp").alias("last_updated"),
    F.current_timestamp().alias("silver_processed_timestamp")
) \
.filter(F.col("product_id").isNotNull()) \
.filter(F.col("quantity") >= 0) \
.dropDuplicates(["product_id", "warehouse_id"])

print(f"Inventory records: {inventory_silver.count()}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Data Quality Validation

# COMMAND ----------

# Validation: Orders
null_order_ids = orders_silver.filter(F.col("order_id").isNull()).count()
null_customers = orders_silver.filter(F.col("customer_id").isNull()).count()
invalid_amounts = orders_silver.filter(F.col("order_amount") <= 0).count()

print(f"Orders QA:")
print(f"  Null order IDs: {null_order_ids}")
print(f"  Null customer IDs: {null_customers}")
print(f"  Invalid amounts: {invalid_amounts}")

# Validation: Products
null_product_names = products_silver.filter(F.col("product_name").isNull()).count()
invalid_prices = products_silver.filter(F.col("price") < 0).count()

print(f"\nProducts QA:")
print(f"  Null product names: {null_product_names}")
print(f"  Invalid prices: {invalid_prices}")

# Validation: Customers
null_emails = customers_silver.filter(F.col("email").isNull()).count()
null_names = customers_silver.filter(F.col("full_name").isNull()).count()

print(f"\nCustomers QA:")
print(f"  Null emails: {null_emails}")
print(f"  Null names: {null_names}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Write to Silver Layer (Delta)

# COMMAND ----------

# Write orders to delta
orders_silver.write \
  .format("delta") \
  .mode("overwrite") \
  .save(f"{SILVER_PATH}/orders")

# Write products to delta
products_silver.write \
  .format("delta") \
  .mode("overwrite") \
  .save(f"{SILVER_PATH}/products")

# Write customers to delta
customers_silver.write \
  .format("delta") \
  .mode("overwrite") \
  .save(f"{SILVER_PATH}/customers")

# Write inventory to delta
inventory_silver.write \
  .format("delta") \
  .mode("overwrite") \
  .save(f"{SILVER_PATH}/inventory")

print("✅ All tables written to Silver layer")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Create Managed Tables

# COMMAND ----------

# Create or replace tables
spark.sql(f"""
CREATE OR REPLACE TABLE ecommerce.silver_orders
USING DELTA
LOCATION '{SILVER_PATH}/orders'
""")

spark.sql(f"""
CREATE OR REPLACE TABLE ecommerce.silver_products
USING DELTA
LOCATION '{SILVER_PATH}/products'
""")

spark.sql(f"""
CREATE OR REPLACE TABLE ecommerce.silver_customers
USING DELTA
LOCATION '{SILVER_PATH}/customers'
""")

spark.sql(f"""
CREATE OR REPLACE TABLE ecommerce.silver_inventory
USING DELTA
LOCATION '{SILVER_PATH}/inventory'
""")

print("✅ Delta tables created")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary

# COMMAND ----------

summary = {
    "orders": orders_silver.count(),
    "products": products_silver.count(),
    "customers": customers_silver.count(),
    "inventory": inventory_silver.count(),
    "processing_time": "Bronze to Silver transformation",
    "status": "SUCCESS"
}

for key, value in summary.items():
    print(f"{key}: {value}")
