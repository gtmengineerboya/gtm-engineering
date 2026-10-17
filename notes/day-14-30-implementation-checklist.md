# Days 14–30 implementation checklist

This checklist tracks concrete deliverables for the continuation. Day-specific
README, learning notes, and checkpoints belong in each day's folder.

| Day | Deliverables | Status |
|---|---|---|
| 14 | Validate and normalize CRM leads; dry-run-first create/update planner; mocked CRM tests; synthetic CSV. | Complete; offline tests pass |
| 15 | Reusable timeout/retry/backoff HTTP client and failure-path tests. | Complete; offline tests pass |
| 16 | Day 13 architecture guide and credential-free n8n workflow export/manual test guide. | Complete; poller/JSON tests pass; UI import remains manual |
| 17 | Deterministic lifecycle qualification/routing and decision CSV. | Complete; boundary tests and CLI pass |
| 18 | Duplicate review and safe merge-candidate rules; no destructive merge. | Complete; tests and CLI pass |
| 19 | Ollama research JSON schema, evidence validation, fallback, and offline tests. | Complete; fallback and mocked error tests pass |
| 20 | Deterministic outreach-quality evaluation and human review gate. | Complete; offline tests pass |
| 21 | CRM association integrity with explicit association configuration, dry-run, and read-back tests. | Complete; dry-run and fake-client tests pass |
| 22 | Portable SQL lessons and runnable SQLite funnel queries. | Complete; SQLite execution verified |
| 23 | Unit-aware funnel/revenue metrics with CSV and Markdown reports. | Complete; tests and sample reports pass |
| 24 | Local authenticated-capable webhook receiver with durable event-id deduplication and synthetic tests. | Complete; offline validation/idempotency tests pass |
| 25 | Offline standard-library test suite, test configuration, and CI workflow. | Complete; 42 tests pass |
| 26 | Read-only run-log/health operations report and redaction. | Complete; historical log preserved |
| 27 | Configuration validation, safe limits, privacy/security guidance, and repository ignore audit. | Complete; offline tests pass |
| 28 | Offline synthetic end-to-end pipeline with human approval and CRM dry-run boundaries. | Complete; capstone test and CLI pass |
| 29 | Portfolio overview, architecture, synthetic metrics, interview Q&A, and demo walkthrough. | Complete; documentation reviewed |
| 30 | Final assessment, all-days completion matrix, test evidence, and manual setup limitations. | Complete; results documented below |

## Verification gates

1. Keep Days 1–13 and their historical data intact; correct only verified,
   directly related defects.
2. Run each new group with `.venv\Scripts\python.exe -m unittest` before
   starting the next group.
3. Mock external integrations. Do not read local secret files or call live
   CRM/Ollama services as a side effect of tests.
4. Run the full offline suite and inspect Git status/diff before reporting
   completion. Do not commit or push.
