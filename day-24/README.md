# Day 24 — Webhooks and event-driven automation

Start the service on loopback only:

```powershell
Set-Location C:\gtm-engineering
C:\gtm-engineering\.venv\Scripts\python.exe -m uvicorn day-24.webhook_api:app --host 127.0.0.1 --port 8001
```

Send a synthetic local event from another PowerShell window:

```powershell
$body = '{"event_id":"demo-001","event_type":"lead.created","data":{"source":"synthetic"}}'
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8001/webhooks/events -ContentType 'application/json' -Body $body
```

Repeating the same event ID returns `duplicate`; only ID, event type, and
receipt time are stored. The body is limited to 64 KiB. To enable HMAC
validation, set `WEBHOOK_SHARED_SECRET` before starting the server and send
`X-Webhook-Signature: sha256=<hex HMAC-SHA256 of the exact raw body>`.
The first synthetic request returns `accepted`; repeating `demo-001` returns
`duplicate`.

Do not bind to a public interface or expose the service to the internet.
Tests: `python -m unittest discover -s tests -p "test_days19_24.py" -v`.
Troubleshooting: a signature is sensitive to every byte, including whitespace;
use the exact request body for signing.
