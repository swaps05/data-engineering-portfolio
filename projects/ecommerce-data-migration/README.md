# E-Commerce Data Migration to Cloud Data Lake 🛍️

**On-Premises SQL Server → Azure Data Lake migration** for Israeli clothing e-commerce brand, processing 500GB monthly (16-20 GB daily) with 30% ETL optimization.

---

## 📋 Business Requirements

### Challenge
An established Israeli clothing e-commerce brand faced critical scalability issues:
- **Legacy on-premises SQL Server** unable to scale with business growth
- **Slow query performance** affecting real-time inventory visibility
- **Manual data pipelines** prone to errors and delays
- **High infrastructure costs** with limited elasticity
- **Monthly data volume:** 500GB (growing 15% YoY)

### Objective
Migrate to cloud-based data lake with:
- ✅ 30% reduction in ETL processing time
- ✅ Real-time inventory and sales analytics
- ✅ Scalable infrastructure for growth
- ✅ 99.9% uptime SLA
- ✅ Cost-optimized cloud solution

---

## 🏗️ Solution Architecture

```
ON-PREMISES
┌─────────────────┐
│  SQL Server DB  │
│  - Orders       │
│  - Products     │
│  - Customers    │
│  - Inventory    │
└────────┬────────┘
         │
         │ Azure Data Factory
         │ (Daily scheduled pipelines)
         ↓
CLOUD (AZURE)
┌──────────────────────────────────────────────────────────────┐
│           ADLS Gen2 (Data Lake)                              │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│ Raw Layer (Bronze)                                           │
│  └── Parquet files (daily extracts from SQL Server)          │
│                                                                │
│ Transformed Layer (Silver)                                   │
│  ├── Orders_Silver (deduplicated, cleaned)                   │
│  ├── Products_Silver (enriched product info)                 │
│  ├── Customers_Silver (unified customer view)                │
│  └── Inventory_Silver (real-time stock levels)               │
│                                                                │
│ Analytics Layer (Gold)                                       │
│  ├── Sales_Analytics (aggregated sales facts)                │
│  ├── Product_Performance (KPIs by product)                   │
│  └── Customer_Analytics (RFM segmentation)                   │
│                                                                │
└──────────────────────────────────────────────────────────────┘
         │
         ↓
┌──────────────────────────────────────────────────────────────┐
│  Databricks Cluster (Transformations)                        │
│  ├── PySpark jobs (data cleaning, deduplication)             │
│  ├── Spark SQL transformations                               │
│  ├── Delta Lake optimization (partitioning, Z-ordering)      │
│  └── Data quality checks                                     │
└──────────────────────────────────────────────────────────────┘
         │
         ↓
┌──────────────────────────────────────────────────────────────┐
│  Azure SQL Database (Optional DW for specific use cases)     │
│  └── Views for real-time reporting                           │
└──────────────────────────────────────────────────────────────┘
         │
         ↓
┌──────────────────────────────────────────────────────────────┐
│  Power BI Dashboards                                         │
│  ├── Sales Analytics Dashboard                               │
│  ├── Inventory Management Dashboard                          │
│  ├── Customer Segmentation Dashboard                         │
│  └── Executive KPI Dashboard                                 │
└──────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Source** | SQL Server (On-Prem) | Legacy system |
| **Ingestion** | Azure Data Factory | Scheduled data extracts |
| **Storage** | ADLS Gen2 | Data lake storage (Parquet) |
| **Processing** | Databricks + PySpark | ETL transformations |
| **Format** | Delta Lake | Optimized table format |
| **Optimization** | Spark SQL | Query optimization |
| **BI** | Power BI | Analytics dashboards |

---

## 📊 Project Results

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **ETL Processing Time** | 4.5 hours | 3.1 hours | 31% faster |
| **Query Response Time** | 45 seconds | 2 seconds | 22x faster |
| **Data Freshness** | Daily (batch) | Real-time | 24h → real-time |
| **Storage Cost** | $8,000/month | $2,500/month | 69% savings |
| **System Uptime** | 95% | 99.9% | +4.9% reliability |
| **Scalability** | Fixed capacity | Elastic | Unlimited growth |
| **Data Volume** | 500GB/month | 500GB+/month | Supports growth |

---

## 📁 Project Structure

```
ecommerce-data-migration/
├── README.md (this file)
├── BUSINESS_REQUIREMENTS.md
├── SOLUTION_ARCHITECTURE.md
├── 01-sql-server-schema/
│   ├── original_tables.sql
│   └── extraction_queries.sql
├── 02-databricks-notebooks/
│   ├── 01_ingest_sql_server_data.py
│   ├── 02_bronze_to_silver.py
│   ├── 03_silver_to_gold.py
│   └── 04_data_quality_validations.py
├── 03-delta-tables/
│   ├── create_delta_schema.sql
│   └── delta_table_structure.md
├── 04-optimization/
│   ├── partitioning_strategy.md
│   ├── z_order_optimization.py
│   └── query_optimization_guide.sql
├── 05-power-bi/
│   ├── dashboard_descriptions.md
│   └── data_model.md
└── 06-deployment/
    ├── migration_playbook.md
    └── post_migration_validation.sql
```

---

## 🚀 Migration Approach

### Phase 1: Preparation (Weeks 1-2)
- ✅ Assess SQL Server schema & data volume
- ✅ Design medallion architecture
- ✅ Set up Azure infrastructure (ADLS, Databricks)
- ✅ Create ADF pipelines for data extraction

### Phase 2: Initial Load (Weeks 3-4)
- ✅ Full data export from SQL Server
- ✅ Load to ADLS Bronze layer
- ✅ Run initial transformations (Bronze → Silver)
- ✅ Validate data integrity

### Phase 3: Transformation & Optimization (Weeks 5-6)
- ✅ Build Silver & Gold layer tables
- ✅ Apply partitioning & Z-ordering
- ✅ Implement data quality checks
- ✅ Optimize Delta table performance

### Phase 4: Analytics & BI (Weeks 7-8)
- ✅ Connect Power BI to data lake
- ✅ Create dashboards
- ✅ Validate analytics accuracy
- ✅ User training

### Phase 5: Go-Live & Optimization (Week 9+)
- ✅ Cutover from SQL Server to cloud
- ✅ Monitor query performance
- ✅ Fine-tune partitioning
- ✅ Cost optimization

---

## 📊 Power BI Dashboards

### 1. Sales Analytics Dashboard
- Daily/Monthly sales trends
- Revenue by product category
- Top products & performers
- Customer acquisition metrics

### 2. Inventory Management Dashboard
- Current stock levels by warehouse
- Low stock alerts
- Inventory turnover by product
- Stock aging analysis

### 3. Customer Segmentation Dashboard
- RFM segmentation
- Customer lifetime value
- Repeat purchase rate
- Geographic distribution

### 4. Executive KPI Dashboard
- Total revenue (YTD)
- Order count & average value
- Gross margin %
- Inventory health index

---

## 🔍 Data Quality Validations

All data passes through automated checks at each layer:

```python
# Validations applied:
✅ No null primary keys
✅ No duplicate records
✅ Foreign key referential integrity
✅ Date ranges are valid
✅ Numeric values within acceptable ranges
✅ Row counts match between layers
✅ Data freshness (processed within SLA)
```

---

## 💡 Technical Highlights

✅ **Medallion Architecture** — Clean separation of raw, transformed, and refined data  
✅ **Delta Lake Format** — ACID transactions, time travel, schema enforcement  
✅ **Smart Partitioning** — By order_date for optimal query performance  
✅ **Z-Order Optimization** — Pruning for multi-column filters  
✅ **Incremental Loads** — Only new/changed data processed daily  
✅ **Automated Testing** — Data quality checks at each transformation layer  
✅ **Cost Optimization** — Spot instances, auto-scaling Databricks clusters  

---

## 👥 Team & Responsibilities

| Role | Responsibility |
|------|-----------------|
| **Junior Data Engineer (Swapnil)** | End-to-end migration, Databricks, pipeline development |
| **Senior Data Engineer** | Architecture review, optimization |
| **DBA** | SQL Server extraction, performance tuning |
| **Cloud Architect** | Azure infrastructure, networking |
| **Power BI Developer** | Dashboard design & development |

---

## 📈 Key Learnings

1. **Partition Strategy Matters** — Proper partitioning reduced queries by 90%
2. **Z-Order Optimization** — Essential for multi-column filter performance
3. **Incremental Loads** — Reduced daily processing time from 4.5h to 3.1h
4. **Data Quality First** — Caught issues early with automated validations
5. **Cost Monitoring** — Regular cost optimization saved 69% monthly spend

---

## 🔐 Security & Compliance

- ✅ Azure Blob Storage encryption (at-rest & in-transit)
- ✅ Azure Key Vault for credential management
- ✅ Network isolation (VNet, NSG)
- ✅ Role-based access control (RBAC)
- ✅ Audit logging for compliance

---

**Project Timeline:** Aug 2021 - Apr 2022 (9 weeks)  
**Migration Scope:** 500GB+ monthly data  
**Status:** ✅ Successfully Completed  
**Last Updated:** June 2026
