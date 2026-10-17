# Day 27 — Security, privacy, and reliability

The project ignores local environment files, virtual environments, caches,
SQLite databases, and newly generated per-day output folders. `.env.example`
contains variable names and placeholders only. Existing `.env` files stay
local and are never read by this audit or test suite.

Run a safe configuration/redaction example:

```powershell
C:\gtm-engineering\.venv\Scripts\python.exe C:\gtm-engineering\day-27\security_checks.py
```

New HTTP calls use timeouts, input validation has bounds, the webhook supports
HMAC validation, and logs redact tokens and email addresses. Use only the
minimum HubSpot scopes for a lesson and inspect the current schema. No secrets
are displayed by the example. Troubleshooting: a placeholder environment value
is rejected without echoing its contents.

For the Day 14 contact example, use only contact read/write and company read
access needed for exact-domain lookup. Verify the permission names and scope
availability in your HubSpot portal before configuring any live token.
