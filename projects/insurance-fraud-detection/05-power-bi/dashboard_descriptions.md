# Power BI Dashboards - Insurance Fraud Detection Platform

## Overview

Four comprehensive Power BI dashboards connected to Azure Synapse Analytics data warehouse, providing real-time fraud detection insights and claims analytics.

**Data Refresh:** Every 15 minutes (real-time)
**User Base:** Claims Investigators, Risk Managers, Executives
**Performance:** <2 second query response time

---

## 1. Fraud Detection Dashboard 🚨

### Purpose
Real-time monitoring of fraudulent claims and alerts for investigation teams.

### Key Visuals

#### 1.1 High-Risk Claims Alert Card
- **Visual Type:** Multi-row Card
- **Metrics:** 
  - Total high-risk claims (fraud_score >= 70)
  - Fraud confirmed count (past 24h)
  - Average fraud score
- **Filter:** Claim status = 'Filed' or 'Under Review'
- **Interaction:** Click to drill into specific claim

#### 1.2 Claims by Fraud Risk Category (Pie Chart)
- **Visual Type:** Pie Chart
- **Data:** 
  - HIGH_RISK (Red)
  - MEDIUM_RISK (Orange)
  - LOW_RISK (Yellow)
  - NO_RISK (Green)
- **Metrics:** Claim count, Total amount
- **Interactivity:** Hover for details, click to filter other visuals

#### 1.3 Fraud Score Distribution (Histogram)
- **Visual Type:** Histogram
- **X-Axis:** Fraud Score (0-100 in bins of 10)
- **Y-Axis:** Number of claims
- **Annotations:** 
  - High-risk threshold line (70)
  - Medium-risk threshold line (40)
- **Insight:** Shows distribution of fraud risk across all claims

#### 1.4 Top 20 Claims Requiring Investigation (Table)
- **Columns:**
  - Claim ID
  - Customer Name
  - Claim Amount (Formatted: $)
  - Fraud Score (Conditional formatting: Red for >70)
  - Policy Type
  - Claim Status
  - Days Since Claim
- **Sorting:** Descending by Fraud Score
- **Row Limit:** 20 (top risks)
- **Interaction:** Click claim ID to see detailed investigation page

#### 1.5 Fraud Alerts Timeline (Line Chart)
- **X-Axis:** Date (Daily)
- **Y-Axis:** Count of high-risk claims identified
- **Time Range:** Last 90 days
- **Trend:** Moving average (7-day)
- **Insight:** Detect seasonal patterns and spikes

#### 1.6 Investigation Queue by Investigator (Clustered Bar)
- **Categories:** Investigator names
- **Values:** 
  - Claims assigned (Blue)
  - Claims resolved (Green)
  - Claims pending (Orange)
- **Sorting:** By pending claims (descending)

---

## 2. Risk Assessment Dashboard 📊

### Purpose
Strategic view of customer risk segmentation and claim patterns by risk tier.

### Key Visuals

#### 2.1 Customer Risk Distribution (Donut Chart)
- **Segments:**
  - High Risk: prior_claims_count >= 3
  - Medium Risk: prior_claims_count 1-2
  - Low Risk: prior_claims_count = 0
- **Metrics:** Customer count, % of total, avg fraud score
- **Color Coding:** Red, Orange, Green

#### 2.2 Claims by Customer Risk Segment (Stacked Column)
- **X-Axis:** Risk Segment
- **Y-Axis:** Count of claims
- **Stack:** By claim status (Approved, Rejected, Under Review, etc.)
- **Insight:** Shows which risk segments have highest claim volume

#### 2.3 Average Fraud Score by Policy Type (Bar Chart)
- **Categories:** Auto, Home, Life, Health, Disability
- **Values:** Average fraud score
- **Sorting:** Descending
- **Benchmark Line:** Overall average fraud score
- **Insight:** Which policy types are most susceptible to fraud

#### 2.4 Customer Claim History Heatmap
- **Rows:** Top 50 customers by total claims
- **Columns:** Time periods (Months)
- **Values:** Claim frequency (heatmap color intensity)
- **Highlight:** Customers with sudden claim increase (red flags)

#### 2.5 Risk Metrics by Age Group (Scatter Chart)
- **X-Axis:** Customer age
- **Y-Axis:** Fraud score
- **Bubble Size:** Claim amount
- **Color:** By policy type
- **Insight:** Age vs. fraud risk correlation

#### 2.6 Prior Claims vs. Fraud Score (Correlation)
- **X-Axis:** Prior claims count
- **Y-Axis:** Average fraud score
- **Trendline:** Linear regression
- **Insight:** Does more claims history = higher fraud risk?

---

## 3. Claims Analytics Dashboard 📈

### Purpose
Operational metrics tracking claim processing efficiency and compliance.

### Key Visuals

#### 3.1 Daily Claims Volume (KPI Card)
- **Metric:** Claims filed today
- **Trend:** % change vs. yesterday
- **Target:** Daily SLA target
- **Sparkline:** Last 30 days trend

#### 3.2 Average Processing Time (Gauge Chart)
- **Metric:** Days to process claims
- **Target:** <14 days (green zone), <21 days (yellow), >21 (red)
- **Current:** Today's average
- **Benchmark:** Policy type average

#### 3.3 Claims Processing Funnel (Funnel Chart)
- **Stages:**
  - Filed: 100% baseline
  - Under Review: % of filed
  - Approved: % of filed
  - Rejected: % of filed
  - Paid: % of filed
- **Insight:** Where claims drop off in process

#### 3.4 Claim Status Distribution (Waterfall)
- **Starting:** Total filed claims
- **Flow:** → Under Review, → Approved, → Paid, → Rejected
- **Ending:** Current claim inventory
- **Insight:** Claim processing bottlenecks

#### 3.5 SLA Compliance by Policy Type (Clustered Bar)
- **Categories:** Policy types
- **Values:** 
  - On-time % (Green)
  - Late % (Red)
- **Target:** 90% on-time SLA
- **Sorting:** By on-time %

#### 3.6 Approval Rate Trend (Line Chart)
- **X-Axis:** Week
- **Y-Axis:** Approval rate %
- **Lines:**
  - Overall approval rate
  - Auto approval rate
  - Property approval rate
  - Medical approval rate
- **Insight:** Trend over time, seasonal patterns

#### 3.7 Cost Impact Analysis (Table)
- **Columns:**
  - Policy Type
  - Total Claim Amount
  - Approved Amount
  - Avg Processing Cost
  - Cost per claim
- **Sorting:** By total amount

---

## 4. Executive Summary Dashboard 👔

### Purpose
High-level KPIs for management reporting and strategic decisions.

### Key Visuals

#### 4.1 Key Metrics (Card Array)
- **Card 1:** Total Claims (This Month)
- **Card 2:** Total Claim Value ($)
- **Card 3:** Fraud Cases Detected (#)
- **Card 4:** Prevention Rate (%)
- **Card 5:** Average Processing Days (#)
- **Card 6:** System Uptime (%)

#### 4.2 Monthly Claims Trend (Combination Chart)
- **Column:** Monthly claim volume
- **Line:** Average fraud score trend
- **X-Axis:** Month (Last 12 months)
- **Insight:** Seasonal patterns, year-over-year comparison

#### 4.3 Fraud Detection Effectiveness (KPI)
- **Metric:** % of claims flagged as fraud
- **Comparison:** vs. industry benchmark
- **Status:** Above/Below target
- **Arrow:** Trending direction

#### 4.4 Claims by Policy Type (Pie Chart)
- **Segments:** Auto, Home, Life, Health, Disability
- **Metrics:** Count, %, total amount
- **Interaction:** Click to see detailed page for policy type

#### 4.5 Top Regions by Fraud Rate (Map Visual)
- **Geographic:** Regional heatmap
- **Color Intensity:** Fraud rate %
- **Hover:** Region name, fraud rate, claim count
- **Insight:** Geographic fraud hotspots

#### 4.6 Department Performance Scorecard
- **Rows:** 
  - Claims Processing (% SLA met)
  - Fraud Detection (cases detected)
  - Customer Satisfaction (NPS)
  - Cost per Claim (trend)
- **Traffic Light:** Green (good), Yellow (caution), Red (alert)

#### 4.7 YoY Comparison (Year-over-Year)
- **Metrics:**
  - Claims filed
  - Total amount
  - Fraud cases
  - Processing days
- **Format:** Current year vs. last year with % change

---

## Power BI Data Model

### Tables Connected
- `fact_claims` - Main claim transactions
- `dim_customer` - Customer master
- `dim_policy` - Policy master
- `dim_claim_type` - Claim type lookup
- `dim_date` - Calendar dimension

### Key Measures (DAX)

```dax
-- High-Risk Claims
HIGH_RISK_CLAIMS = CALCULATE(
    COUNTROWS('fact_claims'),
    'fact_claims'[fraud_score] >= 70
)

-- Fraud Detection Rate
FRAUD_DETECTION_RATE = 
    DIVIDE(
        CALCULATE(COUNTROWS('fact_claims'), 'fact_claims'[fraud_confirmed] = 1),
        COUNTROWS('fact_claims'),
        0
    ) * 100

-- Average Processing Days
AVG_PROCESSING_DAYS = AVERAGE('fact_claims'[processing_days])

-- Claims SLA Compliance
CLAIMS_ON_TIME = 
    DIVIDE(
        CALCULATE(COUNTROWS('fact_claims'), 'fact_claims'[processing_days] <= 14),
        COUNTROWS('fact_claims'),
        0
    ) * 100
```

---

## Dashboard Access & Permissions

- **Owner:** Data Analytics Team
- **Workspace:** Insurance Analytics (Premium Capacity)
- **Refresh:** Every 15 minutes (automated)
- **Users:** Claims Investigators, Risk Managers, Executives
- **Row-Level Security (RLS):** By investigator team assignment

---

## Performance Optimization

✅ **Direct Query:** Used for real-time metrics  
✅ **Aggregation Tables:** Pre-aggregated for daily metrics  
✅ **Incremental Refresh:** Only new claims processed  
✅ **Query Folding:** Optimized DAX queries  
✅ **Caching:** Premium capacity auto-caching enabled

---

## Support & Maintenance

- **Last Updated:** June 2026
- **Next Review:** Quarterly
- **Support Contact:** analytics@insurance.com
- **Known Limitations:** Real-time refresh lags during high-load periods
