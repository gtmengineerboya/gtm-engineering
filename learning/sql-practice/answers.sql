-- ANSWER KEY for learning/sql-skills.md. Attempt each question first.
-- Run: .\.venv\Scripts\python.exe learning\sql-practice\run_practice.py learning\sql-practice\answers.sql
-- Written for SQLite; Postgres differences are noted where they matter.

-- Q1: US companies with more than 100 employees, largest first
SELECT company_name, employees
FROM companies
WHERE country = 'USA' AND employees > 100
ORDER BY employees DESC;

-- Q2: contacts per company, INCLUDING companies with zero contacts
-- LEFT JOIN keeps companies with no match; COUNT(ct.contact_id) ignores the NULLs,
-- so they show 0. COUNT(*) would wrongly show 1 for them.
SELECT c.company_name, COUNT(ct.contact_id) AS contact_count
FROM companies AS c
LEFT JOIN contacts AS ct ON ct.company_id = c.company_id
GROUP BY c.company_id, c.company_name
ORDER BY contact_count DESC, c.company_name;

-- Q3: companies with NO activity at all (the "anti-join" pattern)
SELECT c.company_name
FROM companies AS c
LEFT JOIN activities AS a ON a.company_id = c.company_id
WHERE a.activity_id IS NULL
ORDER BY c.company_name;

-- Q4: average score by industry, only industries with 2+ score rows
-- TRAP: Acme AI has two score rows, so SaaS counts 5 rows, not 4 companies.
-- To average per company you must use the latest score only (see Q5).
SELECT c.industry, COUNT(*) AS scored_rows, AVG(ls.icp_score) AS avg_score
FROM companies AS c
JOIN lead_scores AS ls ON ls.company_id = c.company_id
GROUP BY c.industry
HAVING COUNT(*) >= 2
ORDER BY avg_score DESC;

-- Q5: latest score per company (window function)
WITH ranked AS (
    SELECT company_id, icp_score, scored_at,
           ROW_NUMBER() OVER (PARTITION BY company_id ORDER BY scored_at DESC) AS rn
    FROM lead_scores
)
SELECT c.company_name, r.icp_score, r.scored_at
FROM ranked AS r
JOIN companies AS c ON c.company_id = r.company_id
WHERE r.rn = 1
ORDER BY r.icp_score DESC;

-- Q6: win rate by lead source, treating NULL source as 'unknown'
-- Win rate = won / (won + lost). Open deals are excluded from the denominator.
-- NULLIF avoids divide-by-zero (outbound has only an open deal, so NULL not an error).
SELECT COALESCE(c.original_source, 'unknown') AS source,
       COUNT(*) AS deals,
       SUM(CASE WHEN d.stage = 'closed_won' THEN 1 ELSE 0 END) AS won,
       1.0 * SUM(CASE WHEN d.stage = 'closed_won' THEN 1 ELSE 0 END)
           / NULLIF(SUM(CASE WHEN d.stage IN ('closed_won', 'closed_lost') THEN 1 ELSE 0 END), 0)
           AS win_rate
FROM deals AS d
JOIN companies AS c ON c.company_id = d.company_id
GROUP BY COALESCE(c.original_source, 'unknown')
ORDER BY source;

-- Q7: duplicate contacts after cleaning email (trim + lowercase)
SELECT LOWER(TRIM(email)) AS clean_email, COUNT(*) AS copies
FROM contacts
GROUP BY LOWER(TRIM(email))
HAVING COUNT(*) > 1;

-- Q8: days from a company's first activity to each deal being created
-- julianday() is SQLite. Postgres: (d.created_at::date - MIN(a.activity_date::date))
SELECT d.deal_id, c.company_name,
       CAST(julianday(d.created_at) - julianday(MIN(a.activity_date)) AS INTEGER)
           AS days_first_touch_to_deal
FROM deals AS d
JOIN companies AS c ON c.company_id = d.company_id
JOIN activities AS a ON a.company_id = d.company_id
GROUP BY d.deal_id, c.company_name, d.created_at
ORDER BY d.deal_id;

-- Q9: pipeline created per month and change vs the previous month (LAG)
-- Postgres: use DATE_TRUNC('month', created_at) instead of substr().
WITH monthly AS (
    SELECT substr(created_at, 1, 7) AS month, SUM(amount) AS pipeline_created
    FROM deals
    GROUP BY substr(created_at, 1, 7)
)
SELECT month, pipeline_created,
       LAG(pipeline_created) OVER (ORDER BY month) AS previous_month,
       pipeline_created - LAG(pipeline_created) OVER (ORDER BY month) AS change
FROM monthly
ORDER BY month;

-- Q10: orphan contacts (point to a company that does not exist)
SELECT ct.contact_id, ct.name
FROM contacts AS ct
LEFT JOIN companies AS c ON c.company_id = ct.company_id
WHERE c.company_id IS NULL;

-- Q11: top 2 companies per industry by LATEST score
WITH latest AS (
    SELECT ls.company_id, ls.icp_score
    FROM lead_scores AS ls
    WHERE ls.scored_at = (
        SELECT MAX(scored_at) FROM lead_scores WHERE company_id = ls.company_id
    )
),
ranked AS (
    SELECT c.industry, c.company_name, l.icp_score,
           ROW_NUMBER() OVER (PARTITION BY c.industry ORDER BY l.icp_score DESC) AS rn
    FROM companies AS c
    JOIN latest AS l ON l.company_id = c.company_id
)
SELECT industry, company_name, icp_score
FROM ranked
WHERE rn <= 2
ORDER BY industry, icp_score DESC;

-- BONUS B1: upsert (insert or update) keyed on a UNIQUE column.
-- Same idea as your gtm_engine/webhooks.py INSERT OR IGNORE, but it UPDATES on conflict.
-- A unique index on email only works once the data is clean, which is why Q7 comes first.
-- (Run on a copy: rows 105/106 would clash. Here we create it on a fresh column set.)
CREATE TABLE contacts_clean (
    email     TEXT PRIMARY KEY,
    name      TEXT,
    job_title TEXT
);
INSERT INTO contacts_clean VALUES ('mike@cloudtech.com', 'Mike', 'CTO');
INSERT INTO contacts_clean (email, name, job_title)
VALUES ('mike@cloudtech.com', 'Mike', 'CTO and Founder')
ON CONFLICT (email) DO UPDATE SET job_title = excluded.job_title;
SELECT * FROM contacts_clean;
