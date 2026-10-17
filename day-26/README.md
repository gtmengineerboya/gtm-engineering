# Day 26 — Observability and operations

Create a read-only summary from Day 13's historical run log:

```powershell
C:\gtm-engineering\.venv\Scripts\python.exe C:\gtm-engineering\day-26\operations_report.py
```

It reports run/status counts, total processed leads, failures, and average
duration without copying detailed log messages or editing the tracked
historical CSV. The report is local under `day-26\output\`.

Day 13 already records run IDs, status, counts, duration, and details. Its
run-state API remains in memory and has no retention policy; this is acceptable
for a local demo but not a durable production job store. Troubleshooting: a
missing or changed CSV header produces an explicit error.
