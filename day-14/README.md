# Day 14 — HubSpot CRM data processing

Learn to validate contact rows, normalize email/domain values, and identify
contacts by unique email before deciding whether to create or update. The
`gtm_engine.crm` module is shared so later lessons can reuse the rules.

Run from any PowerShell working directory:

```powershell
C:\gtm-engineering\.venv\Scripts\python.exe C:\gtm-engineering\day-14\crm_processing.py
```

This is a dry run: it validates the synthetic CSV and prints the intended
upserts without making API requests. Live mode requires an environment token
and an explicit second action:

```powershell
C:\gtm-engineering\.venv\Scripts\python.exe C:\gtm-engineering\day-14\crm_processing.py --apply
```

Only type `APPLY` after reviewing the displayed plan. Never use real prospects
for this exercise. Contact writes perform read-back verification; company
association is intentionally a separate Day 21 exercise. Live batches are
limited to 10 validated records per invocation.

Test offline from the repository root:

```powershell
C:\gtm-engineering\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_days14_18.py" -v
```

Troubleshooting: an invalid or blank email/domain is rejected before live mode.
Missing credentials matter only after choosing live mode. See
[`learning_notes.md`](learning_notes.md) and [`checkpoint.md`](checkpoint.md).
