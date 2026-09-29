-- What goes inside queries.sql?

-- We will practice the SQL concepts you just learned.

-- For example:

-- -- 1. Show all companies
-- SELECT *
-- FROM companies;


-- -- 2. Show only USA companies
-- SELECT *
-- FROM companies
-- WHERE country = 'USA';


-- -- 3. Show companies with more than 100 employees
-- SELECT company_name, employees
-- FROM companies
-- WHERE employees > 100;


-- -- 4. Sort companies by employees
-- SELECT company_name, employees
-- FROM companies
-- ORDER BY employees DESC;


-- -- 5. Count companies
-- SELECT COUNT(*)
-- FROM companies;

-- Then we'll add the more important GTM queries:

-- -- 6. Company + contact
-- SELECT
--     c.company_name,
--     ct.name,
--     ct.job_title
-- FROM companies AS c
-- JOIN contacts AS ct
--     ON c.company_id = ct.company_id;

-- And eventually:

-- -- 7. Company + ICP score
-- SELECT
--     c.company_name,
--     ls.icp_score
-- FROM companies AS c
-- JOIN lead_scores AS ls
--     ON c.company_id = ls.company_id;

-- And the key Day 4 GTM query:

-- -- 8. US companies with ICP score above 70
-- SELECT
--     c.company_name,
--     c.country,
--     ls.icp_score
-- FROM companies AS c
-- JOIN lead_scores AS ls
--     ON c.company_id = ls.company_id
-- WHERE c.country = 'USA'
--   AND ls.icp_score > 70;

-- Important: We don't need to put everything in queries.sql immediately. We'll build it step by step as you learn each query



-- INSERT INTO companies
-- (company_id, company_name, country, industry, employees)
-- VALUES
-- (1, 'Acme AI', 'USA', 'SaaS', 250),
-- (2, 'Beta Finance', 'India', 'Finance', 50),
-- (3, 'CloudTech', 'USA', 'SaaS', 500),
-- (4, 'DataWorks', 'UK', 'SaaS', 120);


Yes. Let's **finish Day 4 completely now**. We already have the `companies` table and 4 companies. We will finish the remaining tables, practice the required SQL, do the checkpoint, and then commit.

Your Day 4 roadmap covers the SQL operations and GTM database work we're doing here. 

## Step 1 — Create the contact data

You are currently at:

```text
sqlite>
```

Paste this:

```sql
INSERT INTO contacts
(contact_id, company_id, name, job_title, email)
VALUES
(101, 1, 'John', 'CEO', 'john@acme.ai'),
(102, 1, 'Sarah', 'VP Sales', 'sarah@acme.ai'),
(103, 3, 'Mike', 'CTO', 'mike@cloudtech.com'),
(104, 4, 'David', 'CEO', 'david@dataworks.co');
```

Then verify:

```sql
SELECT * FROM contacts;
```

You should get:

```text
101 | 1 | John  | CEO      | john@acme.ai
102 | 1 | Sarah | VP Sales | sarah@acme.ai
103 | 3 | Mike  | CTO      | mike@cloudtech.com
104 | 4 | David | CEO      | david@dataworks.co
```

Notice:

```text
John  → company_id 1 → Acme AI
Sarah → company_id 1 → Acme AI
Mike  → company_id 3 → CloudTech
David → company_id 4 → DataWorks
```

---

## Step 2 — Create ICP scores

Run:

```sql
INSERT INTO lead_scores
(score_id, company_id, icp_score)
VALUES
(1, 1, 85),
(2, 2, 40),
(3, 3, 92),
(4, 4, 65);
```

Check:

```sql
SELECT * FROM lead_scores;
```

Expected:

```text
1 | 1 | 85
2 | 2 | 40
3 | 3 | 92
4 | 4 | 65
```

---

## Step 3 — Create activities

Run:

```sql
INSERT INTO activities
(activity_id, company_id, activity_type)
VALUES
(1, 1, 'Email Open'),
(2, 1, 'Website Visit'),
(3, 3, 'Demo Request'),
(4, 4, 'LinkedIn Click'),
(5, 3, 'Email Open');
```

Check:

```sql
SELECT * FROM activities;
```

---

# Step 4 — Practice SELECT + WHERE

### All companies

```sql
SELECT *
FROM companies;
```

### Only USA companies

```sql
SELECT *
FROM companies
WHERE country = 'USA';
```

Expected:

```text
Acme AI
CloudTech
```

### SaaS companies

```sql
SELECT company_name, industry
FROM companies
WHERE industry = 'SaaS';
```

---

# Step 5 — ORDER BY

Largest companies first:

```sql
SELECT company_name, employees
FROM companies
ORDER BY employees DESC;
```

Expected order:

```text
CloudTech    500
Acme AI      250
DataWorks    120
Beta Finance 50
```

---

# Step 6 — UPDATE

Let's say Acme AI actually has 300 employees.

Run:

```sql
UPDATE companies
SET employees = 300
WHERE company_id = 1;
```

Verify:

```sql
SELECT *
FROM companies
WHERE company_id = 1;
```

You should see:

```text
1 | Acme AI | USA | SaaS | 300
```

This demonstrates:

```text
UPDATE
  ↓
SET
  ↓
WHERE
```

---

# Step 7 — COUNT

How many companies?

```sql
SELECT COUNT(*)
FROM companies;
```

Result:

```text
4
```

How many USA companies?

```sql
SELECT COUNT(*)
FROM companies
WHERE country = 'USA';
```

Result:

```text
2
```

---

# Step 8 — GROUP BY

How many companies are in each country?

```sql
SELECT country, COUNT(*)
FROM companies
GROUP BY country;
```

Expected:

```text
India | 1
UK    | 1
USA   | 2
```

This is useful for GTM reporting.

---

# Step 9 — CASE

Classify companies based on size:

```sql
SELECT
    company_name,
    employees,
    CASE
        WHEN employees >= 500 THEN 'Enterprise'
        WHEN employees >= 100 THEN 'Mid-Market'
        ELSE 'SMB'
    END AS segment
FROM companies;
```

Expected:

```text
Acme AI       | 300 | Mid-Market
Beta Finance  | 50  | SMB
CloudTech     | 500 | Enterprise
DataWorks     | 120 | Mid-Market
```

Remember:

```text
Python:
if / elif / else

SQL:
CASE / WHEN / ELSE
```

---

# Step 10 — Your first real JOIN

Now combine companies and contacts:

```sql
SELECT
    c.company_name,
    ct.name,
    ct.job_title
FROM companies AS c
INNER JOIN contacts AS ct
    ON c.company_id = ct.company_id;
```

Expected:

```text
Acme AI    | John  | CEO
Acme AI    | Sarah | VP Sales
CloudTech  | Mike  | CTO
DataWorks  | David | CEO
```

This is the concept you asked about earlier:

```text
Sarah.company_id = 1
Acme.company_id  = 1

1 = 1
↓
Sarah → Acme AI
```

---

# Step 11 — JOIN + ICP score

Now combine **companies + contacts + scores**:

```sql
SELECT
    c.company_name,
    ct.name,
    ct.job_title,
    ls.icp_score
FROM companies AS c
JOIN contacts AS ct
    ON c.company_id = ct.company_id
JOIN lead_scores AS ls
    ON c.company_id = ls.company_id;
```

Now your GTM data is connected:

```text
Company
   ↓
Contact
   ↓
ICP Score
```

---

# Step 12 — Important GTM query

The roadmap's Day 4 checkpoint asks for US companies with an ICP score above 70. 

Run:

```sql
SELECT
    c.company_name,
    c.country,
    ls.icp_score
FROM companies AS c
JOIN lead_scores AS ls
    ON c.company_id = ls.company_id
WHERE c.country = 'USA'
  AND ls.icp_score > 70;
```

Expected:

```text
Acme AI   | USA | 85
CloudTech | USA | 92
```

**This is a real GTM-style query:** you're filtering accounts based on geography and ICP fit.

---

# Step 13 — Final Day 4 checkpoint

Before we commit, answer these **without looking back**:

### Q1

What is the difference between a **PRIMARY KEY** and a **FOREIGN KEY**?

### Q2

What does this do?

```sql
SELECT *
FROM companies
WHERE country = 'USA';
```

### Q3

What is the difference between `INNER JOIN` and `LEFT JOIN`?

### Q4

Why does Sarah belong to Acme AI?

```text
Sarah.company_id = 1
Acme.company_id = 1
```

### Q5

What does `GROUP BY` do?

### Q6

What is `CASE` used for?

### Q7 — GTM interview question

Explain this query in simple English:

```sql
SELECT
    c.company_name,
    ls.icp_score
FROM companies AS c
JOIN lead_scores AS ls
    ON c.company_id = ls.company_id
WHERE ls.icp_score > 70;
```

Send me your **7 answers**. I'll check them, and if they're correct, we'll do the **final Day 4 Git commit**.
