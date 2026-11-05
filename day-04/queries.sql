-- Day 4 practice queries. Every statement here is runnable SQL.
--
-- Needs: day-04/gtm_database.py to have created the tables, and the sample rows from
-- day-04/sql_basics.md steps 1-3 (companies, contacts, lead_scores, activities).
--
-- Run every query in this file (from the repo root, in the sqlite3 shell):
--   sqlite3 gtm.db
--   .read day-04/queries.sql
-- Or open gtm.db and paste one query at a time to study its result.
--
-- A fuller, messier practice set lives in learning/sql-practice/.

-- 1. All companies
SELECT * FROM companies;

-- 2. Only US companies
SELECT * FROM companies WHERE country = 'USA';

-- 3. Companies with more than 100 employees
SELECT company_name, employees FROM companies WHERE employees > 100;

-- 4. Largest companies first
SELECT company_name, employees FROM companies ORDER BY employees DESC;

-- 5. How many companies are there?
SELECT COUNT(*) AS company_count FROM companies;

-- 6. Each contact with their company (INNER JOIN: contacts with no company would drop out)
SELECT c.company_name, ct.name, ct.job_title
FROM companies AS c
JOIN contacts AS ct ON c.company_id = ct.company_id;

-- 7. Each company with its ICP score
SELECT c.company_name, ls.icp_score
FROM companies AS c
JOIN lead_scores AS ls ON c.company_id = ls.company_id;

-- 8. The key Day 4 GTM query: US companies with an ICP score above 70
SELECT c.company_name, c.country, ls.icp_score
FROM companies AS c
JOIN lead_scores AS ls ON c.company_id = ls.company_id
WHERE c.country = 'USA'
  AND ls.icp_score > 70;

-- 9. Companies per country
SELECT country, COUNT(*) AS company_count
FROM companies
GROUP BY country
ORDER BY company_count DESC;

-- 10. Label each company by size
SELECT company_name,
       CASE
           WHEN employees >= 200 THEN 'Large'
           WHEN employees >= 100 THEN 'Mid'
           ELSE 'Small'
       END AS size_band
FROM companies;
