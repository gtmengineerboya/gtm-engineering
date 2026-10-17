# Day 15 — Reliable API integrations

`gtm_engine.http_client.request_with_retries` sets a timeout and uses a bounded
exponential delay for transient errors. It retries common read methods and
idempotent `PUT`/`DELETE` calls, but retries `POST` only when an
`Idempotency-Key` header is supplied. A final HTTP error is raised to the
caller instead of being hidden.

Run the fully offline retry demonstration:

```powershell
C:\gtm-engineering\.venv\Scripts\python.exe C:\gtm-engineering\day-15\reliable_api_demo.py
```

Expected output: `Final status: 200; attempts: 2`. Run tests from the repository
root with `python -m unittest discover -s tests -p "test_days14_18.py" -v`.
Troubleshooting: retrying a non-idempotent POST can create duplicates; add a
server-supported idempotency key or do not retry it.
