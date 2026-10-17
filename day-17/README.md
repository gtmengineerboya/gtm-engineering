# Day 17 — GTM funnel and lead routing

Run `route_leads.py` to assign lifecycle stages and deterministic owner queues
from synthetic lead data. Explicit demo requests become SQLs; valid high ICP
scores become MQLs; invalid scores remain unqualified and include a reason.
No CRM writes occur.

```powershell
C:\gtm-engineering\.venv\Scripts\python.exe C:\gtm-engineering\day-17\route_leads.py
```

The report is written under `day-17\output\`. Tests:
`python -m unittest discover -s tests -p "test_days14_18.py" -v`.
Troubleshooting: check the score range and exact buying-signal text before
changing routing rules.
