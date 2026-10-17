# Day 22 — PostgreSQL concepts and analytical SQL

Run four portable analytics queries against a temporary, in-memory SQLite
database:

```powershell
C:\gtm-engineering\.venv\Scripts\python.exe C:\gtm-engineering\day-22\run_sql.py
```

The queries show funnel counts, ICP quality by stage, source performance, and
average stage duration. The included duration values are already in days;
timestamp arithmetic differs between SQLite and PostgreSQL, so production
queries should use the target database's date functions. The core `CASE`,
`COUNT`, `SUM`, `AVG`, `GROUP BY`, and ordering concepts are portable.

No PostgreSQL server or paid database is required. Troubleshooting: the script
creates its sample schema in memory and requires no existing `gtm.db`.
