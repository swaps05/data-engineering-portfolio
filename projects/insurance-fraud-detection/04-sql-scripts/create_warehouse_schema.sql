-- Insurance Fraud Detection Data Warehouse Schema
-- Azure Synapse Analytics
-- Purpose: Star schema for fraud detection and claims analytics
-- Author: Data Engineering Team
-- Last Updated: June 2026

-- ============================================================================
-- 1. CREATE SCHEMA
-- ============================================================================

CREATE SCHEMA dw_insurance;
GO

-- ============================================================================
-- 2. DIMENSION TABLES
-- ============================================================================

-- Dim_Customer: Customer master data
CREATE TABLE dw_insurance.dim_customer (
    customer_key INT IDENTITY(1,1) PRIMARY KEY,
    customer_id VARCHAR(50) UNIQUE NOT NULL,
    customer_name VARCHAR(255),
    age INT,
    location VARCHAR(255),
    prior_claims_count INT,
    risk_tier VARCHAR(50),  -- Low, Medium, High
    created_date DATETIME DEFAULT GETDATE(),
    updated_date DATETIME DEFAULT GETDATE()
)
WITH (CLUSTERED COLUMNSTORE INDEX);

-- Dim_Policy: Policy master data
CREATE TABLE dw_insurance.dim_policy (
    policy_key INT IDENTITY(1,1) PRIMARY KEY,
    policy_id VARCHAR(50) UNIQUE NOT NULL,
    policy_number VARCHAR(100),
    policy_type VARCHAR(50),  -- Auto, Home, Life, Health
    coverage_amount DECIMAL(12,2),
    premium_amount DECIMAL(12,2),
    start_date DATE,
    end_date DATE,
    status VARCHAR(50),  -- Active, Lapsed, Cancelled
    created_date DATETIME DEFAULT GETDATE()
)
WITH (CLUSTERED COLUMNSTORE INDEX);

-- Dim_Claim_Type: Claim type lookup
CREATE TABLE dw_insurance.dim_claim_type (
    claim_type_key INT IDENTITY(1,1) PRIMARY KEY,
    claim_type VARCHAR(50) UNIQUE NOT NULL,
    claim_type_description VARCHAR(255),
    average_settlement_days INT,
    created_date DATETIME DEFAULT GETDATE()
);

INSERT INTO dw_insurance.dim_claim_type (claim_type, claim_type_description, average_settlement_days)
VALUES 
    ('Auto', 'Auto Insurance Claims', 14),
    ('Property', 'Property Damage Claims', 21),
    ('Medical', 'Medical Insurance Claims', 7),
    ('Life', 'Life Insurance Claims', 30),
    ('Disability', 'Disability Claims', 45);

-- Dim_Date: Calendar dimension
CREATE TABLE dw_insurance.dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    year INT,
    quarter INT,
    month INT,
    day INT,
    week INT,
    day_of_week INT,
    is_weekend BIT
);

-- Populate date dimension (last 5 years)
WITH date_range AS (
    SELECT DATEADD(DAY, number, CAST('2021-01-01' AS DATE)) AS full_date
    FROM master..spt_values
    WHERE type = 'P' AND number < 1826
)
INSERT INTO dw_insurance.dim_date
SELECT 
    CAST(FORMAT(full_date, 'yyyyMMdd') AS INT) AS date_key,
    full_date,
    YEAR(full_date),
    QUARTER(full_date),
    MONTH(full_date),
    DAY(full_date),
    DATEPART(WEEK, full_date),
    DATEPART(WEEKDAY, full_date),
    CASE WHEN DATEPART(WEEKDAY, full_date) IN (1,7) THEN 1 ELSE 0 END
FROM date_range;

-- ============================================================================
-- 3. FACT TABLES
-- ============================================================================

-- Fact_Claims: Main fact table for claims
CREATE TABLE dw_insurance.fact_claims (
    claim_key BIGINT IDENTITY(1,1) PRIMARY KEY,
    claim_id VARCHAR(50) NOT NULL,
    policy_key INT FOREIGN KEY REFERENCES dw_insurance.dim_policy(policy_key),
    customer_key INT FOREIGN KEY REFERENCES dw_insurance.dim_customer(customer_key),
    claim_type_key INT FOREIGN KEY REFERENCES dw_insurance.dim_claim_type(claim_type_key),
    claim_date_key INT FOREIGN KEY REFERENCES dw_insurance.dim_date(date_key),
    processing_date_key INT FOREIGN KEY REFERENCES dw_insurance.dim_date(date_key),
    
    -- Claim metrics
    claim_amount DECIMAL(12,2),
    approved_amount DECIMAL(12,2),
    deductible_amount DECIMAL(12,2),
    claim_status VARCHAR(50),  -- Filed, Under Review, Approved, Rejected, Paid
    processing_days INT,
    
    -- Fraud detection metrics
    fraud_score INT,  -- 0-100
    fraud_risk_category VARCHAR(50),  -- HIGH_RISK, MEDIUM_RISK, LOW_RISK, NO_RISK
    fraud_flag BIT DEFAULT 0,
    fraud_confirmed BIT DEFAULT 0,
    
    -- Quality metrics
    claim_description VARCHAR(MAX),
    witness_count INT,
    police_report_filed BIT,
    
    created_date DATETIME DEFAULT GETDATE(),
    updated_date DATETIME DEFAULT GETDATE(),
    INDEX idx_claim_id (claim_id),
    INDEX idx_fraud_score (fraud_score),
    INDEX idx_claim_status (claim_status)
)
WITH (CLUSTERED COLUMNSTORE INDEX, DISTRIBUTION = HASH(claim_id));

-- Fact_Claims_Daily_Metrics: Daily aggregated metrics
CREATE TABLE dw_insurance.fact_claims_daily_metrics (
    date_key INT PRIMARY KEY,
    total_claims INT,
    total_claim_amount DECIMAL(15,2),
    average_claim_amount DECIMAL(12,2),
    approved_claims INT,
    rejected_claims INT,
    high_risk_fraud_claims INT,
    average_processing_days INT,
    created_date DATETIME DEFAULT GETDATE()
);

-- ============================================================================
-- 4. MATERIALIZED VIEWS FOR REPORTING
-- ============================================================================

-- Claims by Risk Category
CREATE VIEW dw_insurance.vw_claims_by_risk_category AS
SELECT 
    c.fraud_risk_category,
    c.claim_type_key,
    ct.claim_type,
    COUNT(*) AS claim_count,
    SUM(c.claim_amount) AS total_amount,
    AVG(c.fraud_score) AS avg_fraud_score,
    COUNT(CASE WHEN c.fraud_confirmed = 1 THEN 1 END) AS confirmed_fraud_count
FROM dw_insurance.fact_claims c
JOIN dw_insurance.dim_claim_type ct ON c.claim_type_key = ct.claim_type_key
GROUP BY c.fraud_risk_category, c.claim_type_key, ct.claim_type;

-- Customer Claim History
CREATE VIEW dw_insurance.vw_customer_claim_history AS
SELECT 
    cust.customer_key,
    cust.customer_id,
    cust.customer_name,
    COUNT(fc.claim_key) AS total_claims,
    SUM(fc.claim_amount) AS total_claim_amount,
    COUNT(CASE WHEN fc.fraud_confirmed = 1 THEN 1 END) AS fraud_count,
    AVG(fc.fraud_score) AS avg_fraud_score
FROM dw_insurance.dim_customer cust
LEFT JOIN dw_insurance.fact_claims fc ON cust.customer_key = fc.customer_key
GROUP BY cust.customer_key, cust.customer_id, cust.customer_name;

-- Monthly Claims Trend
CREATE VIEW dw_insurance.vw_monthly_claims_trend AS
SELECT 
    YEAR(d.full_date) AS year,
    MONTH(d.full_date) AS month,
    COUNT(fc.claim_key) AS claim_count,
    SUM(fc.claim_amount) AS total_amount,
    AVG(fc.fraud_score) AS avg_fraud_score
FROM dw_insurance.fact_claims fc
JOIN dw_insurance.dim_date d ON fc.claim_date_key = d.date_key
GROUP BY YEAR(d.full_date), MONTH(d.full_date);

-- ============================================================================
-- 5. SAMPLE QUERIES FOR ANALYTICS
-- ============================================================================

-- Query 1: High-Risk Fraud Claims Summary
SELECT 
    fraud_risk_category,
    COUNT(*) AS claim_count,
    SUM(claim_amount) AS total_amount,
    AVG(fraud_score) AS avg_score,
    MIN(fraud_score) AS min_score,
    MAX(fraud_score) AS max_score
FROM dw_insurance.fact_claims
WHERE fraud_risk_category IN ('HIGH_RISK', 'MEDIUM_RISK')
GROUP BY fraud_risk_category
ORDER BY claim_count DESC;

-- Query 2: Claims Requiring Investigation (Top 100)
SELECT TOP 100
    fc.claim_id,
    cust.customer_name,
    p.policy_type,
    fc.claim_amount,
    fc.fraud_score,
    fc.fraud_risk_category,
    fc.claim_status,
    DATEDIFF(DAY, d.full_date, GETDATE()) AS days_since_claim
FROM dw_insurance.fact_claims fc
JOIN dw_insurance.dim_customer cust ON fc.customer_key = cust.customer_key
JOIN dw_insurance.dim_policy p ON fc.policy_key = p.policy_key
JOIN dw_insurance.dim_date d ON fc.claim_date_key = d.date_key
WHERE fc.fraud_score >= 70 AND fc.claim_status IN ('Filed', 'Under Review')
ORDER BY fc.fraud_score DESC, fc.claim_amount DESC;

-- Query 3: Processing Efficiency Metrics
SELECT 
    p.policy_type,
    COUNT(*) AS claim_count,
    AVG(fc.processing_days) AS avg_processing_days,
    MIN(fc.processing_days) AS min_days,
    MAX(fc.processing_days) AS max_days,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fc.processing_days) OVER (PARTITION BY p.policy_type) AS median_days
FROM dw_insurance.fact_claims fc
JOIN dw_insurance.dim_policy p ON fc.policy_key = p.policy_key
GROUP BY p.policy_type;

-- Query 4: Customer Risk Segmentation
SELECT 
    CASE 
        WHEN cust.prior_claims_count >= 3 THEN 'High Risk'
        WHEN cust.prior_claims_count >= 1 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS risk_segment,
    COUNT(*) AS customer_count,
    AVG(CAST(fc.fraud_score AS INT)) AS avg_fraud_score,
    SUM(fc.claim_amount) AS total_claims_amount
FROM dw_insurance.dim_customer cust
LEFT JOIN dw_insurance.fact_claims fc ON cust.customer_key = fc.customer_key
GROUP BY risk_segment;

-- ============================================================================
-- 6. CREATE INDEXES FOR PERFORMANCE
-- ============================================================================

CREATE NONCLUSTERED INDEX idx_fact_claims_customer
ON dw_insurance.fact_claims (customer_key)
INCLUDE (claim_amount, fraud_score, fraud_risk_category);

CREATE NONCLUSTERED INDEX idx_fact_claims_policy
ON dw_insurance.fact_claims (policy_key)
INCLUDE (claim_amount, claim_status);

CREATE NONCLUSTERED INDEX idx_fact_claims_date
ON dw_insurance.fact_claims (claim_date_key)
INCLUDE (claim_amount, fraud_score);

-- ============================================================================
-- 7. GRANT PERMISSIONS
-- ============================================================================

-- Grant select to analytics users
GRANT SELECT ON SCHEMA::dw_insurance TO [analytics_users];
GRANT SELECT ON SCHEMA::dw_insurance TO [power_bi_service];
