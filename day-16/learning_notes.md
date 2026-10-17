# Day 16 learning notes

n8n is the visual coordinator; FastAPI is the local service contract and the
Python runner does the work. The POST response contains a `run_id`. Polling
must use that same ID, not call POST repeatedly. Otherwise, every retry might
start another job.

The Python client sends one trigger request, then requests
`GET /run-status/{run_id}` until it sees `success` or `failed`. A monotonic
clock makes the timeout independent of wall-clock changes. HTTP failures and
unexpected status strings are surfaced. The n8n export uses no credentials;
manual import and execution remain user actions.

Day 13 keeps status in memory, so a service restart loses run history. That is
an intentional local-demo limitation, not durable orchestration.
