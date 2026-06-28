# E-Commerce Data Pipeline 🛍️

End-to-end real-time and batch data pipeline for an e-commerce platform, handling inventory, orders, and customer analytics.

---

## 📋 Problem Statement

E-commerce business needed:
- Real-time inventory synchronization across warehouses
- Daily sales analytics and forecasting
- Customer segmentation for marketing campaigns
- Order fulfillment optimization

**Challenge:** Legacy batch system causing 12-hour data delays, inventory mismatches, and inability to respond to demand spikes.

---

## 🏗️ Architecture

```
Data Sources (SQL Server, APIs)
           ↓
    Azure Data Factory
    (Ingestion & Orchestration)
           ↓
    Azure Data Lake (Bronze)
           ↓
    Apache Spark / PySpark
    (Transformations)
           ↓
    Azure Data Lake (Silver/Gold)
           ↓
    dbt (Data Modeling)
           ↓
    Power BI Dashboards
    (Analytics & Insights)
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Ingestion | Azure Data Factory |
| Processing | PySpark + Databricks |
| Storage | Azure Data Lake Gen2 |
| Transformation | dbt |
| BI | Power BI |

---

## 📊 Results

| Metric | Before | After |
|--------|--------|-------|
| Data Freshness | 12 hours | 5 minutes |
| Inventory Accuracy | 89% | 99.2% |
| Query Performance | 45 sec | 2 sec |

---

**Status:** ✅ Production | **Last Updated:** June 2026
