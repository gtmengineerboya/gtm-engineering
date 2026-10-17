# Day 28 — Final end-to-end GTM revenue engine

Run the offline capstone:

```powershell
C:\gtm-engineering\.venv\Scripts\python.exe C:\gtm-engineering\day-28\run_capstone.py
```

Flow: synthetic CSV → validation/normalization → deterministic score →
lifecycle/routing → evidence-only research fallback → outreach draft →
quality checks → human approval required → CRM dry-run plan → CSV report and
run summary. Generated files are under `day-28\output\`.

Expected safety summary: **CRM writes 0; messages sent 0; human approval
required**. The local fallback makes this runnable without Ollama. The report
contains synthetic sample data only. Test with
`python -m unittest discover -s tests -p "test_days25_30.py" -v`.

Add `--ollama` to opt in to local Ollama research. The outreach draft and human
approval gate remain unchanged; no messages are sent and no CRM write occurs.

Troubleshooting: invalid email/domain fields are rejected before report
creation. The capstone does not invoke the Day 12 live sync or send messages.
