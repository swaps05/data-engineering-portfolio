# Power BI Dashboards - E-Commerce Data Migration

## Overview

Four comprehensive dashboards providing real-time analytics on sales, inventory, customers, and executive KPIs.

**Data Source:** Azure Data Lake (Delta Lake)  
**Refresh Rate:** Every hour  
**Users:** Marketing, Merchandising, Finance, Executives

---

## 1. Sales Analytics Dashboard 📈

### Purpose
Real-time sales performance tracking and trend analysis.

### Key Visuals

#### 1.1 Sales Performance Cards
- **Total Revenue (YTD):** $X million
- **Total Orders:** X,XXX
- **Average Order Value:** $XXX
- **Growth vs. Last Year:** XX%

#### 1.2 Daily Sales Trend (Line Chart)
- **X-Axis:** Date (last 90 days)
- **Y-Axis:** Daily revenue ($)
- **Trend Line:** 7-day moving average
- **Insight:** Identify seasonal patterns and spikes

#### 1.3 Revenue by Country (Map Visual)
- **Geographic:** Country-level heatmap
- **Color Intensity:** Revenue ($)
- **Top Market:** Israel
- **Other Markets:** EU, US, Asia

#### 1.4 Top 10 Customers by Revenue (Bar Chart)
- **Customers:** Top spenders
- **Values:** Lifetime value ($)
- **Interaction:** Click to drill into order history

#### 1.5 Order Status Distribution (Pie Chart)
- **Segments:** Pending, Confirmed, Shipped, Delivered, Cancelled
- **Metrics:** Order count, % of total
- **Insight:** How many orders are stuck in each stage

#### 1.6 Payment Method Analysis (Stacked Bar)
- **Categories:** Credit Card, PayPal, Bank Transfer, Other
- **Values:** Count & revenue by method
- **Trend:** Month-over-month

#### 1.7 Sales by Product Category (Clustered Column)
- **Categories:** Fashion, Accessories, Footwear, etc.
- **Values:** Revenue (Blue), Order count (Green)
- **Sorting:** By revenue (descending)

---

## 2. Inventory Management Dashboard 📦

### Purpose
Monitor stock levels and optimize inventory across warehouses.

### Key Visuals

#### 2.1 Inventory Health Cards
- **Total SKUs:** X,XXX
- **Low Stock Items:** X
- **Out of Stock:** X
- **Average Stock Level:** X units

#### 2.2 Stock Levels by Warehouse (Clustered Bar)
- **Warehouses:** Main, Regional, Distribution
- **Values:** Total units in stock
- **Color:** By product category

#### 2.3 Low Stock Alerts Table
- **Columns:**
  - Product Name
  - Current Stock
  - Reorder Level
  - Days Until Stockout
  - Action Required
- **Filter:** Items below reorder level
- **Highlight:** Red for critical (<7 days)

#### 2.4 Product Stock Aging (Heatmap)
- **Rows:** Top 50 products by stock
- **Columns:** Days in inventory
- **Color Intensity:** Aging severity (red = old stock)
- **Insight:** Identify slow-moving inventory

#### 2.5 Inventory Turnover by Category (Gauge Charts)
- **Metric:** Inventory turnover ratio
- **Target:** X times/year (industry benchmark)
- **Status:** Green (good), Yellow (caution), Red (alert)

#### 2.6 Stock Availability % (KPI)
- **Metric:** % of products in stock
- **Target:** 95%+
- **Trend:** Month-over-month comparison

#### 2.7 Reorder Analysis (Scatter)
- **X-Axis:** Current stock
- **Y-Axis:** Reorder level
- **Bubble Size:** Monthly sales
- **Color:** By category
- **Insight:** Which products need reordering

---

## 3. Customer Segmentation Dashboard 👥

### Purpose
Understand customer behavior and segment for targeted marketing.

### Key Visuals

#### 3.1 Customer Metrics Cards
- **Total Customers:** X,XXX
- **Active Customers (90d):** X,XXX
- **New Customers (Month):** X
- **Churn Rate:** X%

#### 3.2 RFM Segmentation (Scatter Plot)
- **X-Axis:** Recency (days since purchase)
- **Y-Axis:** Frequency (purchase count)
- **Bubble Size:** Monetary value ($)
- **Quadrants:** Champions, Loyal, At-Risk, Lost

#### 3.3 Customer Lifetime Value Distribution (Histogram)
- **X-Axis:** CLV ($)
- **Y-Axis:** Customer count
- **Percentiles:** 25th, 50th, 75th marked
- **Average Line:** Mean CLV

#### 3.4 Repeat Purchase Rate Trend (Line Chart)
- **X-Axis:** Month
- **Y-Axis:** % of repeat customers
- **Goal Line:** Target repeat rate
- **Insight:** Customer retention trend

#### 3.5 Customer Acquisition Cost (Funnel)
- **Stages:**
  - Website Visitors: 100K
  - Add to Cart: 10K
  - Checkout Start: 5K
  - Purchase: 3K
- **Insight:** Dropout rates at each stage

#### 3.6 Geographic Distribution (Map)
- **Color:** Customer count by country
- **Size:** By total revenue
- **Hotspots:** Israel (main market)

#### 3.7 Customer Segmentation Summary (Table)
- **Segments:** VIP, Regular, Occasional, Inactive
- **Metrics:**
  - Customer count
  - Avg LTV
  - Purchase frequency
  - Churn rate
- **Sorting:** By customer count

---

## 4. Executive KPI Dashboard 👔

### Purpose
High-level business metrics for C-suite decision making.

### Key Visuals

#### 4.1 Main KPI Cards (4-Card Layout)
- **Card 1 - YTD Revenue:** $X.XXM (vs. last year: +XX%)
- **Card 2 - Order Volume:** X,XXX orders (vs. last year: +XX%)
- **Card 3 - Gross Margin:** XX% (target: XX%)
- **Card 4 - Customer Satisfaction:** NPS score XX

#### 4.2 Revenue Waterfall
- **Starting Point:** Last year YTD revenue
- **Flows:**
  - New customers revenue
  - Repeat customer growth
  - Seasonal adjustments
  - Returns/cancellations
- **Ending:** Current year YTD

#### 4.3 Monthly Revenue Trend (Combination Chart)
- **Column:** Monthly revenue
- **Line:** Growth rate %
- **Benchmark:** Last year monthly values
- **Insight:** Year-over-year comparison

#### 4.4 Key Metrics Scorecard
- **Rows:**
  - Revenue Growth: XX% ✅
  - Order Growth: XX% ✅
  - Margin %: XX% ⚠️
  - Customer Retention: XX% ✅
- **Traffic Lights:** Green/Yellow/Red

#### 4.5 Product Category Performance (Pie)
- **Segments:** Top categories by revenue
- **Size:** Revenue contribution %
- **Growth:** YoY change indicator

#### 4.6 Operational Efficiency Metrics (Gauges)
- **Gauge 1:** Inventory Turnover (xx days)
- **Gauge 2:** Order Fulfillment (xx%)
- **Gauge 3:** Returns Rate (xx%)
- **Gauge 4:** Customer Satisfaction (NPS xx)

#### 4.7 Market Performance vs. Targets (Matrix)
- **Rows:** Markets (Israel, EU, US, Asia)
- **Columns:** Revenue, Orders, Growth
- **Values:** Actual vs. Target (% variance)
- **Highlight:** Red for underperformance

---

## Power BI Data Model

### Tables
- `silver_orders` - Order transactions
- `silver_products` - Product master
- `silver_customers` - Customer master
- `silver_inventory` - Stock levels

### Key Measures (DAX)

```dax
-- Total Revenue
TOTAL_REVENUE = SUMX(orders, orders[order_amount])

-- Average Order Value
AVG_ORDER_VALUE = AVERAGE(orders[order_amount])

-- Customer Lifetime Value
CLV = SUMX(
    DISTINCT(customers[customer_id]),
    CALCULATE(TOTAL_REVENUE)
)

-- Repeat Purchase Rate
REPEAT_CUSTOMER_RATE = 
    DIVIDE(
        CALCULATE(DISTINCTCOUNT(orders[customer_id]), 
                  FILTER(ALL(orders), COUNTROWS(orders) > 1)),
        DISTINCTCOUNT(orders[customer_id])
    )

-- Inventory Turnover
INVENTORY_TURNOVER = 
    COGS / AVERAGE([inventory])
```

---

## Dashboard Access

- **Owner:** Analytics Team
- **Workspace:** E-Commerce Analytics
- **Users:** Sales, Inventory, Finance, Executives
- **Refresh:** Hourly (automated)
- **Performance:** <3 second load time

---

**Last Updated:** June 2026
