# Data Warehouse Modernization with Microsoft Fabric 🏢

Migrating legacy SQL Server data warehouse to Microsoft Fabric with medallion architecture.

---

## 🎯 Objective

Modernize data warehouse by:
- Consolidating fragmented data sources
- Implementing medallion architecture (Bronze/Silver/Gold)
- Reducing infrastructure costs by 60%
- Improving query performance & reliability
- Enabling self-service analytics

---

## 📊 Before & After

| Aspect | Before | After |
|--------|--------|-------|
| Platform | SQL Server | Microsoft Fabric |
| Load Time | 4 hours | 15 minutes |
| Monthly Cost | $2,500 | $1,000 |
| Query Performance | 45 sec avg | 2 sec avg |
| Uptime | 95% | 99.2% |

---

## 🏗️ Architecture

```
Staging DB (SQL Server)
           ↓
    Azure Data Factory
    (Extract & Load)
           ↓
    OneLake (Fabric's Data Lake)
           ├── Bronze (Raw data)
           ├── Silver (Cleaned data)
           └── Gold (Business-ready)
           ↓
    dbt Transformations
           ↓
    Power BI Semantic Model
           ↓
    Executive Dashboards
```

---

## 🛠️ Tech Stack

- **Ingestion:** Azure Data Factory
- **Data Platform:** Microsoft Fabric
- **Transformation:** dbt
- **Storage:** OneLake (Lakehouse format)
- **Modeling:** Power BI Semantic Model
- **Testing:** dbt tests & data quality checks

---

## ✨ Key Features

✅ **Medallion Architecture** — Clear data staging layers  
✅ **dbt Testing** — Automated quality checks  
✅ **Cost Optimization** — Dynamic pricing model  
✅ **Scalability** — Auto-scaling compute  
✅ **Governance** — Row-level & column-level security  

---

## 📈 Outcomes

- ✅ 60% cost reduction
- ✅ 16x faster load times
- ✅ 99.2% uptime achieved
- ✅ 200+ self-service dashboards enabled
- ✅ Zero data quality incidents in 6 months

---

**Status:** ✅ Production | **Last Updated:** June 2026
