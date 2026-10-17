# Day 25 — Automated testing and CI

The repository uses Python's built-in `unittest`, so the offline suite needs no
test-only package. From the repository root:

```powershell
C:\gtm-engineering\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Tests cover CRM validation/dry-run behavior, API retry rules, routing,
deduplication, research validation/fallback, outreach review, association
read-back, metrics, webhook idempotency/signatures, polling, redaction, and the
end-to-end capstone. No test requires HubSpot credentials, Ollama, n8n, or a
paid service. GitHub Actions runs the same command on Windows and Linux.

Troubleshooting: always run the command from the repository root so unittest
discovers `tests`; focused selectors are documented in Days 14–24.
