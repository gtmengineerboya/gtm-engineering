# 30-day GTM Engineering roadmap

Suggested pace: 1.5–3 hours per day. Read the day's README, run its example,
inspect the implementation, complete the checkpoint, and record questions
before moving on.

| Day | Learning objective | Suggested time | Checkpoint |
|---:|---|---:|---|
| 1 | Explain a GTM funnel and identify company/contact/lead fields. | 1.5h | Draw Lead → Customer stages and define one property per stage. |
| 2 | Read and transform lead data with Python. | 1.5h | Explain each input and output field in the enrichment CSV. |
| 3 | Understand an HTTP request/response and deterministic scoring. | 2h | Describe status code, JSON payload, and score reason. |
| 4 | Create a SQLite schema and run basic SQL. | 2h | Query a company and its associated contact. |
| 5 | Model GTM entities and relationships. | 1.5h | Explain why a contact and company are separate records. |
| 6 | Combine enrichment, lead intelligence, and outreach practice. | 2h | Identify which fields are source facts versus generated text. |
| 7 | Apply and explain ICP scoring rules. | 1.5h | Run the scoring example and verify the known 100-point case. |
| 8 | Structure AI research and CRM-ready data. | 2h | Name one limitation that must be disclosed. |
| 9 | Inspect API integration and idempotency examples safely. | 2h | Explain why live scripts are not imported in tests. |
| 10 | Enrich and qualify leads with deterministic rules. | 2h | Recalculate a score and explain the threshold. |
| 11 | Generate/review outreach drafts with local AI. | 2h | Identify a reason an automated draft must be reviewed. |
| 12 | Understand guarded HubSpot sync and read-back verification. | 2h | Explain dry-run versus explicit apply mode. |
| 13 | Follow a pipeline run through FastAPI and run logs. | 2h | Describe the run ID and in-memory state limitation. |
| 14 | Normalize and validate CRM fields; plan contact upserts. | 2h | Run dry-run and identify the unique email key. |
| 15 | Add timeout, bounded retries, backoff, and idempotency. | 2h | Explain why an unsafe POST is not retried. |
| 16 | Orchestrate FastAPI through n8n and poll one run. | 2h | Identify trigger, run ID, polling, and timeout behavior. |
| 17 | Qualify and route synthetic leads with auditable reasons. | 1.5h | Route an invalid score and explain why it stays unqualified. |
| 18 | Find duplicate candidates without deleting records. | 1.5h | Explain why a candidate match is not an automatic merge. |
| 19 | Separate AI research facts, hypotheses, and limitations. | 2h | Alter a fact to an unsupported value and run validation. |
| 20 | Evaluate outreach deterministically and require human review. | 1.5h | Explain what an automated pass does not guarantee. |
| 21 | Verify CRM associations using account-specific schema. | 2h | Find a real association type in a sandbox, but do not write. |
| 22 | Query funnel/source/stage data with portable SQL. | 2h | Explain one SQLite/PostgreSQL difference. |
| 23 | Calculate funnel and revenue metrics with units. | 2h | Explain CAC, LTV, MRR, ARR, and zero-denominator handling. |
| 24 | Accept and deduplicate local synthetic webhooks. | 2h | Send the same synthetic event twice and observe the duplicate. |
| 25 | Run offline unit tests and inspect CI. | 2h | Explain one mocked failure-path test. |
| 26 | Summarize run health and inspect reliability trade-offs. | 1.5h | Describe one useful operational metric and one data-minimizing choice. |
| 27 | Protect credentials, minimize logs, validate inputs, and redact output. | 2h | Confirm local secrets are ignored and never displayed. |
| 28 | Run the synthetic end-to-end capstone. | 2.5h | Trace one row and point out the human/CRM safety gates. |
| 29 | Present the project accurately as a portfolio example. | 2h | Deliver the walkthrough without claiming real business outcomes. |
| 30 | Re-run tests, review limitations, and plan next skills. | 2h | Complete the matrix and explain what was not tested live. |

Full implementation and validation status: [completion matrix](30-day-completion-matrix.md).
