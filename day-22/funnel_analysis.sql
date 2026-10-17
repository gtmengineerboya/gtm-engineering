WITH funnel AS (
    SELECT
        COUNT(*) AS lead_count,
        SUM(CASE WHEN lifecycle_stage = 'MQL' THEN 1 ELSE 0 END) AS mql_count,
        SUM(CASE WHEN lifecycle_stage = 'SQL' THEN 1 ELSE 0 END) AS sql_count,
        SUM(CASE WHEN lifecycle_stage = 'Opportunity' THEN 1 ELSE 0 END) AS opportunity_count,
        SUM(CASE WHEN lifecycle_stage = 'Customer' THEN 1 ELSE 0 END) AS customer_count
    FROM leads
)
SELECT
    *,
    1.0 * mql_count / NULLIF(lead_count, 0) AS lead_to_mql_rate,
    1.0 * sql_count / NULLIF(mql_count, 0) AS mql_to_sql_rate,
    1.0 * opportunity_count / NULLIF(sql_count, 0) AS sql_to_opportunity_rate,
    1.0 * customer_count / NULLIF(opportunity_count, 0) AS opportunity_to_customer_rate
FROM funnel;

SELECT
    lifecycle_stage,
    COUNT(*) AS record_count,
    AVG(icp_score) AS average_icp_score
FROM leads
GROUP BY lifecycle_stage
ORDER BY lifecycle_stage;

SELECT
    original_source,
    COUNT(*) AS lead_count,
    SUM(CASE WHEN lifecycle_stage = 'Customer' THEN 1 ELSE 0 END) AS customers
FROM leads
GROUP BY original_source
ORDER BY lead_count DESC;

SELECT
    stage,
    COUNT(*) AS transitions,
    AVG(duration_days) AS average_duration_days
FROM stage_history
GROUP BY stage
ORDER BY stage;
