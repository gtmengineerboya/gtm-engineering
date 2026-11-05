# SQL skills map for GTM engineering

**What this is:** every SQL skill your projects use or need, sorted into four
groups so you can see what you have learned, what you must use daily, what to
strengthen and what to add. At the bottom is a hands-on practice set that runs on
your machine in seconds.

**How I built it:** I read `day-04` (`gtm_database.py`, `sql_basics.md`,
`queries.sql`), `day-22` (`funnel_analysis.sql`, `run_sql.py`), and the SQLite code in
`gtm_engine/webhooks.py`.

**An honest finding first:** `day-04/queries.sql` is not a runnable query file. It is
mostly commented-out examples with lesson text pasted in, so you have no clean
file of queries you wrote and ran. Your real SQL practice lives in
`day-04/sql_basics.md` (steps 1 to 13) and the four queries in `day-22`. The practice
set in this folder fixes that.

| Tag | Meaning |
|---|---|
| **LEARNED** | You have written or run it |
| **DAILY** | You will use it constantly in a GTM engineer job |
| **STRENGTHEN** | You touched it but it is thin |
| **ADD** | Not in your repo yet, and the market expects it |

---

## 1. LEARNED: what your code already proves

| Skill | Where you used it | Test yourself |
|---|---|---|
| Design tables with primary and foreign keys | `day-04/gtm_database.py` (companies, contacts, lead_scores, activities) | What stops a contact pointing at a missing company? (Careful: SQLite does not enforce foreign keys unless you turn them on.) |
| `SELECT`, `WHERE`, `ORDER BY` | `day-04/sql_basics.md` steps 4 to 5 | `WHERE` vs `HAVING`? |
| `INSERT` and `UPDATE` | `day-04/sql_basics.md` steps 1 to 3, 6 | What happens to an `UPDATE` with no `WHERE`? |
| `COUNT` and `GROUP BY` | `day-04/sql_basics.md` steps 7 to 8, `day-22/funnel_analysis.sql` | `COUNT(*)` vs `COUNT(column)`? |
| `CASE WHEN` | `day-04/sql_basics.md` step 9, `day-22` | How do you count rows meeting a condition? |
| `INNER JOIN` across two or three tables | `day-04/sql_basics.md` steps 10 to 12 | When does a row disappear from an `INNER JOIN`? |
| A CTE (`WITH`) | `day-22/funnel_analysis.sql` | Why a CTE instead of a nested query? |
| Conversion rate with `NULLIF` | `day-22/funnel_analysis.sql` | Why `1.0 *` and why `NULLIF`? |
| Parameterised queries from Python | `gtm_engine/webhooks.py`, `day-22/run_sql.py` (`?` placeholders, `executemany`) | What is SQL injection and how do `?` stop it? |
| Dedupe with a primary key | `gtm_engine/webhooks.py` (`INSERT OR IGNORE`) | How does this make a webhook safe to receive twice? |

---

## 2. DAILY: the ten queries GTM engineers write all the time

| # | Daily question | Pattern needed | Practice question |
|---|---|---|---|
| 1 | Which accounts match our ICP? | `WHERE` with `AND`, `ORDER BY` | Q1 |
| 2 | Which accounts have no contacts yet? | `LEFT JOIN`, `COUNT` | Q2 |
| 3 | Which leads never got touched? | Anti-join (`LEFT JOIN ... IS NULL`) | Q3 |
| 4 | What is each lead's current score? | Window function `ROW_NUMBER` | Q5 |
| 5 | Which source wins the most deals? | `CASE`, `COALESCE`, `NULLIF` | Q6 |
| 6 | Are these two contacts the same person? | Normalise, `GROUP BY`, `HAVING` | Q7 |
| 7 | How long from first touch to deal? | Date arithmetic | Q8 |
| 8 | Is pipeline growing month over month? | `GROUP BY` month, `LAG` | Q9 |
| 9 | Which records are broken? | Orphan check | Q10 |
| 10 | Top N per segment | `ROW_NUMBER ... PARTITION BY` | Q11 |

---

## 3. STRENGTHEN: learned but thin

1. **`LEFT JOIN` and `NULL` handling.** `NULL` is "unknown", not zero or empty.
   `NULL = NULL` is not true. Use `IS NULL`, `COALESCE`, and be careful with
   `COUNT`. Practice: Q2, Q3, Q6, Q10.
2. **Join fan-out.** Joining to a table with many rows per company multiplies rows and
   inflates sums and counts. Practice: Q4 (a deliberate trap).
3. **`HAVING` and subqueries.** You have the idea but not the habit. Practice: Q4, Q11.
4. **Dates.** Funnel work is all about time. Practice: Q8, Q9.
5. **Constraints and indexes.** You used a primary key. Add `UNIQUE`, `NOT NULL`
   and an index, and know why each exists. Practice: bonus B1.
6. **A real query file.** Keep every query you write in `my_answers.sql`, run it,
   and commit it. Queries you never run are not skills.

---

## 4. ADD: not in your repo, expected by the market

| Skill | Why it matters | First small win |
|---|---|---|
| **Window functions** (`ROW_NUMBER`, `LAG`, running totals) | Latest-record and trend questions come up constantly | Q5, Q9, Q11 |
| **Upsert** (`ON CONFLICT DO UPDATE`) | Idempotent loads into the CRM or warehouse | Bonus B1 |
| **PostgreSQL** specifics (`DATE_TRUNC`, `ILIKE`, `FILTER`, `JSONB`) | Most real GTM data stores run Postgres or a similar warehouse | Re-run every answer on a free hosted Postgres |
| **Query plans and indexes** (`EXPLAIN`) | Know why a query is slow | Run `EXPLAIN` on Q8 and add an index |
| **Data modelling** (fact vs dimension tables, history tables, snapshots) | CRMs overwrite history; analysis needs it kept | Design a `lead_score_history` table |
| **Identity resolution in SQL** (normalise email and domain, fuzzy match) | The data-quality core of the job; you built this in Python on Day 18 | Redo Q7 for company domains |
| **SOQL** (Salesforce's query language) | Looks like SQL but has different join rules | Run 5 SOQL queries in a free developer org |
| **Warehouse dialects** (BigQuery, Snowflake) | Syntax differs for dates and arrays | Port Q9 to one of them |
| **dbt** (optional, later) | Version-controlled, tested SQL transformations | Read one dbt tutorial in phase 4 |

---

## 5. The practice set

Everything is in `learning/sql-practice/`:

| File | Purpose |
|---|---|
| `seed.sql` | Five synthetic tables (companies, contacts, lead_scores, activities, deals) with realistic mess built in |
| `my_answers.sql` | Your file. Write your answers here |
| `answers.sql` | Answer key with comments on the traps. Open it only after you try |
| `run_practice.py` | Rebuilds the database and runs any `.sql` file. Cannot damage anything |

**Run your answers:**

```powershell
Set-Location C:\gtm-engineering
.\.venv\Scripts\python.exe learning\sql-practice\run_practice.py
```

**Check against the key:**

```powershell
.\.venv\Scripts\python.exe learning\sql-practice\run_practice.py learning\sql-practice\answers.sql
```

**The mess built into the data (find it yourself):** one company has two score
rows, two contacts are the same person with different casing and spaces, one
contact points to a company that does not exist, and a few fields are `NULL`.

### The 11 questions

Write each in `my_answers.sql` under its `-- Q` heading. The hint tells you which
tool to reach for, not the answer.

| # | Question | Hint |
|---|---|---|
| Q1 | List US companies with more than 100 employees, largest first. | `WHERE ... AND`, `ORDER BY ... DESC` |
| Q2 | Show contacts per company, including companies with none (show 0). | `LEFT JOIN`; which count ignores `NULL`? |
| Q3 | Which companies have had no activity at all? | `LEFT JOIN`, then `IS NULL` |
| Q4 | Average ICP score by industry, only industries with 2 or more score rows. Then notice what the count really counts. | `GROUP BY`, `HAVING` |
| Q5 | Each company's latest score. | `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ... DESC)` |
| Q6 | Win rate by lead source (won divided by won plus lost). Treat a missing source as "unknown". Open deals should not count. | `CASE`, `COALESCE`, `NULLIF` |
| Q7 | Find duplicate contacts once email is trimmed and lowercased. | `LOWER(TRIM(...))`, `GROUP BY`, `HAVING COUNT(*) > 1` |
| Q8 | For each deal, days from the company's first activity to the deal being created. | `MIN(activity_date)`, `julianday()` |
| Q9 | Pipeline created per month, and the change from the previous month. | `substr(created_at, 1, 7)`, `LAG` |
| Q10 | Contacts whose company does not exist. | `LEFT JOIN`, `IS NULL` on the other side |
| Q11 | Top 2 companies per industry by their latest score. | Latest score first (Q5), then `ROW_NUMBER` per industry |

**Bonus B1:** build a table keyed on email and write an insert that updates the row
if the email already exists. The answer key shows the pattern.

### Make it real after you finish

1. Run every answer on a free hosted Postgres. Fix what breaks. Note each
   difference in a file called `learning/sql-dialect-notes.md`.
2. Write three new questions of your own about the data and answer them.
3. Redo Q5 on your real HubSpot test data once Phase 1 of the roadmap is live.

---

## 6. Self-assessment tracker

0 = cannot do it. 1 = can follow a query that does it. 2 = can write it with the
docs open. 3 = can write it from memory and explain it. Fill the last two columns
yourself and re-score every two weeks.

| Skill | Target by week 12 | Level now | Date re-scored |
|---|---|---|---|
| Filtering and sorting | 3 | | |
| Joins (inner and left) | 3 | | |
| `NULL` handling | 3 | | |
| Aggregation and `HAVING` | 3 | | |
| `CASE` and conditional counts | 3 | | |
| CTEs and subqueries | 3 | | |
| Window functions | 3 | | |
| Dates | 2 | | |
| Constraints, indexes, upserts | 2 | | |
| Reading a query plan | 2 | | |
| PostgreSQL | 2 | | |
| SOQL | 2 | | |
| Data modelling | 2 | | |

## 7. When to do what (matches the 12-week plan)

- **Phase 0 (week 1):** Q1 to Q4, and the self-assessment
- **Phase 1 (weeks 2 to 4):** Q5 to Q8, move to Postgres, start SOQL
- **Phase 2 (weeks 5 to 8):** Q9 to Q11, B1, scoring in SQL on real signals
- **Phase 3 (weeks 9 to 10):** data modelling and history tables
- **Phase 4 (weeks 11 to 12):** `EXPLAIN`, indexes, one dashboard query set

Related file: `python-skills.md`.
