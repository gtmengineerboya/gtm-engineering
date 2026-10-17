# Day 18 — Data quality and deduplication

Run the review-only duplicate detector:

```powershell
C:\gtm-engineering\.venv\Scripts\python.exe C:\gtm-engineering\day-18\dedupe_leads.py
```

It normalizes email and domain values, reports matching records, and marks
every candidate for human review. It never deletes, merges, or updates data.
Review output is under `day-18\output\`; the CSV in this folder is synthetic
test input. Tests:
`python -m unittest discover -s tests -p "test_days14_18.py" -v`.

Troubleshooting: blank identifiers are not treated as evidence of a duplicate.
Do not convert a possible match into an automatic merge without checking all
fields and a human approval process.
