# Insurance Fraud Detection Data Analysis Platform 🛡️

**End-to-end fraud detection and risk assessment platform** processing 20-25 GB daily claims data with 25% improvement in fraud detection latency.

---

## 📋 Business Requirements

### Challenge
A leading insurance company faced critical issues:
- **Manual fraud detection** was time-consuming and error-prone
- **Claim processing delays** caused customer dissatisfaction
- **Risk assessment** lacked data-driven insights
- **Daily data volume** (20-25 GB) from multiple policy platforms couldn't be processed efficiently

### Objective
Build an automated fraud detection and risk assessment platform to:
- ✅ Identify fraudulent claims in real-time
- ✅ Reduce claim processing time significantly
- ✅ Enable data-driven risk segmentation
- ✅ Improve operational efficiency by 20%+

---

## 🏗️ Solution Architecture

```
DATA SOURCES (Policy Platform)
         ↓
INGESTION LAYER (Azure Functions)
         ↓
STORAGE LAYER (ADLS Gen2 - Medallion)
├── Bronze (Raw JSON)
├── Silver (Cleaned & Deduplicated)
└── Gold (Business-Ready)
         ↓
TRANSFORMATION (Azure Databricks)
├── JSON Flattening
├── Fraud Detection Rules
├── Risk Scoring
└── Delta Table Optimization
         ↓
WAREHOUSE (Azure Synapse Analytics)
├── Fact Tables (Claims, Transactions)
├── Dimension Tables (Customers, Products)
└── Aggregated Views
         ↓
VISUALIZATION (Power BI)
├── Fraud Detection Dashboard
├── Risk Assessment Dashboard
├── Claims Analytics Dashboard
└── Executive Summary
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Ingestion | Azure Functions, Event Hubs |
| Orchestration | Azure Data Factory |
| Storage | ADLS Gen2 (Delta Lake) |
| Processing | Databricks, PySpark |
| Warehouse | Azure Synapse Analytics |
| Database | Azure SQL Database |
| DevOps | Azure DevOps, CI/CD |
| BI | Power BI |

---

## 📊 Results

| Metric | Achievement |
|--------|-------------|
| Processing Efficiency | 20% improvement |
| Fraud Detection Latency | 25% reduction |
| Data Cleanliness | 20% improvement |
| Query Performance | <2 seconds |
| System Uptime | 99.9% |
| Daily Data Volume | 20-25 GB |

---

## 📁 Project Contents

- **[Business Requirements](./BUSINESS_REQUIREMENTS.md)** - Detailed business case
- **[Solution Architecture](./SOLUTION_ARCHITECTURE.md)** - Technical deep dive
- **[Azure Functions Code](./01-azure-functions/)** - Event ingestion
- **[ADF Pipelines](./02-adf-pipelines/)** - Orchestration JSONs
- **[Databricks Notebooks](./03-databricks-notebooks/)** - PySpark transformations
- **[SQL Scripts](./04-sql-scripts/)** - Data warehouse schema & queries
- **[Power BI Dashboards](./05-power-bi/)** - Dashboard descriptions & designs
- **[Deployment Guide](./06-deployment/)** - Production deployment steps

---

**Project Timeline:** May 2022 - Nov 2025 | **Status:** ✅ Completed
