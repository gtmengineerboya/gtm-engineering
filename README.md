# GTM Engineering — 30-day hands-on project

Build and explain a safe, synthetic Go-To-Market automation workflow with
Python, APIs, CRM concepts, SQL, AI-assisted research, n8n, testing, and
operations. The repository teaches each concept in a small exercise and joins
the useful pieces in an offline capstone.

> **Safety:** all new examples default to mock, local, or dry-run behavior.
> They do not send prospect messages or automatically write to HubSpot. Never
> commit a secret or use a real prospect in a sample fixture.

## 30-day table of contents

| Day | Topic | Materials |
|---:|---|---|
| 1 | GTM funnel and lead data | [day-01](day-01/) |
| 2 | Lead enrichment basics | [day-02](day-02/) |
| 3 | REST APIs and scoring | [day-03](day-03/) |
| 4 | SQLite and SQL | [day-04](day-04/) |
| 5 | GTM data model | [day-05](day-05/) |
| 6 | Lead intelligence and AI practice | [day-06](day-06/) |
| 7 | Advanced ICP scoring | [day-07](day-07/) |
| 8 | AI research and CRM-ready records | [day-08](day-08/) |
| 9 | HubSpot API examples | [day-09](day-09/) |
| 10 | Enrichment and qualification | [day-10](day-10/) |
| 11 | Personalized outreach review | [day-11](day-11/) |
| 12 | Guarded HubSpot sync | [day-12](day-12/) |
| 13 | Local pipeline API | [day-13](day-13/) |
| 14 | CRM normalization and safe upserts | [day-14](day-14/) |
| 15 | Reliable HTTP integrations | [day-15](day-15/) |
| 16 | n8n pipeline orchestration | [day-16](day-16/) |
| 17 | Funnel qualification and routing | [day-17](day-17/) |
| 18 | Duplicate review | [day-18](day-18/) |
| 19 | AI research and evidence controls | [day-19](day-19/) |
| 20 | Outreach quality evaluation | [day-20](day-20/) |
| 21 | CRM association integrity | [day-21](day-21/) |
| 22 | Analytical SQL and PostgreSQL concepts | [day-22](day-22/) |
| 23 | GTM and revenue metrics | [day-23](day-23/) |
| 24 | Local webhook receiver | [day-24](day-24/) |
| 25 | Offline tests and CI | [day-25](day-25/) |
| 26 | Observability and operations | [day-26](day-26/) |
| 27 | Security, privacy, and reliability | [day-27](day-27/) |
| 28 | Synthetic end-to-end capstone | [day-28](day-28/) |
| 29 | Portfolio and interview practice | [day-29](day-29/) |
| 30 | Assessment and completion matrix | [day-30](day-30/) |

Learning sequence and checkpoints: [30-day roadmap](notes/30-day-roadmap.md).
Evidence for each day's deliverables: [completion matrix](notes/30-day-completion-matrix.md).
Audit of the original repository and implementation decisions:
[Day 14–30 audit](notes/day-14-30-audit.md).

## Prerequisites and Windows setup

- Windows 10/11 and PowerShell.
- Python 3.12 or 3.14; this repository was audited with Python 3.14.7 in
  `.venv`.
- Optional for later lessons: local Ollama and n8n. HubSpot credentials are
  only needed if you deliberately choose a guarded live lesson.

For a new environment:

```powershell
Set-Location C:\gtm-engineering
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

For the already-configured environment, use the same interpreter:

```powershell
Set-Location C:\gtm-engineering
.\.venv\Scripts\python.exe --version
```

`requirements.txt` lists the runtime packages used by the API, HTTP, and
existing `.env` examples. The offline test suite uses Python's built-in
`unittest`.

## Environment variables and secrets

See [.env.example](.env.example) for variable names and safe placeholder
values. Do not overwrite your existing root or `day-09/.env` files. Configure
real values locally in your process environment only when a live lesson needs
them. Never paste secrets into chat, source code, workflow JSON, test fixtures,
or Git.

The HubSpot examples use `HUBSPOT_ACCESS_TOKEN` or `HUBSPOT_TOKEN`. Day 21 also
requires association category/type values verified from the current portal;
the code does not guess them. `WEBHOOK_SHARED_SECRET` is optional and enables
HMAC validation for the local webhook.

## Architecture

```text
Synthetic CSV
  -> validation and normalization
  -> deterministic ICP score and lifecycle/routing
  -> evidence-only research fallback (optional local Ollama on Day 19)
  -> outreach draft and deterministic review
  -> human approval gate
  -> CRM dry-run plan (no integrated capstone live write)
  -> metrics, local reports, and run summaries
```

Reusable, tested rules live in [gtm_engine](gtm_engine/). Day folders contain
the executable lesson and synthetic input; generated local reports are ignored
under each `day-*/output/` directory.

## Run the safe end-to-end demo

```powershell
Set-Location C:\gtm-engineering
.\.venv\Scripts\python.exe .\day-28\run_capstone.py
```

The run reads only `day-28\synthetic_leads.csv` and writes a report under
`day-28\output\`. It reports zero CRM writes, zero messages sent, and a required
human-approval status. It works without Ollama, n8n, or HubSpot credentials.

Other useful examples:

```powershell
.\.venv\Scripts\python.exe .\day-14\crm_processing.py
.\.venv\Scripts\python.exe .\day-17\route_leads.py
.\.venv\Scripts\python.exe .\day-18\dedupe_leads.py
.\.venv\Scripts\python.exe .\day-22\run_sql.py
.\.venv\Scripts\python.exe .\day-23\metrics_report.py
```

## Tests

From the repository root:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Or from any working directory:

```powershell
C:\gtm-engineering\.venv\Scripts\python.exe C:\gtm-engineering\day-25\run_tests.py
```

Tests use synthetic data and mocks; they do not contact HubSpot, Ollama, or
n8n. The GitHub Actions workflow runs the same suite on Windows and Linux.

## Review and publish safely

These are instructions only; no commit or push was made as part of this work.
Review the unstaged and staged diffs before committing:

```powershell
Set-Location C:\gtm-engineering
git status --short
git diff --check
git diff
git add -A
git diff --cached --check
git status --short
git diff --cached
```

Only if the staged diff contains the changes you intend to publish:

```powershell
git commit -m "Complete GTM engineering Days 14-30" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
git push origin main
```

## FastAPI and n8n

Start the Day 13 API on loopback:

```powershell
Set-Location C:\gtm-engineering
.\.venv\Scripts\python.exe -m uvicorn day-13.pipeline_api:app --host 127.0.0.1 --port 8000
```

Health check: `http://127.0.0.1:8000/health`. Day 16 includes a
credential-free workflow export. Import it manually in the local n8n UI, check
the local URL, and execute it only when Day 13 inputs and Ollama are ready.
The workflow is inactive in its export; no import or activation is claimed.
The Python polling client starts one run and polls that run ID with a timeout.
If n8n runs in a container, change the URL to an address reachable from that
container.

## Troubleshooting

- **Import errors:** activate/use `.venv` or invoke its Python executable
  explicitly; install requirements with `-m pip install -r requirements.txt`.
- **CSV/file not found:** lesson scripts resolve files relative to their own
  location; check that the repository files have not been moved independently.
- **Day 13 returns 409:** another run is active; wait rather than submitting a
  second trigger.
- **Ollama unavailable:** Days 19 and 28 have offline deterministic paths;
  Day 13 itself requires its existing local Ollama integration.
- **HubSpot errors:** default to dry run, verify token scopes and schema, then
  review planned changes. Do not add a token to a command or file in Git.
- **n8n cannot reach FastAPI:** confirm both services are running and adjust
  the API host address for the n8n process/container.

## Known limitations and future improvements

- Day 13 retains run state in process memory and has no durable queue/retention.
- Day 14/21 live adapters are guarded examples; portal-specific scopes,
  properties, and association schema must be verified manually.
- Day 19 model output is schema-checked but still needs human factual review.
- Automated outreach checks are not a quality guarantee; no message sender is
  included.
- The capstone does not perform live CRM writes or send messages.
- n8n workflow import/activation, HubSpot live writes, and local Ollama use
  require deliberate manual setup and were not run by the offline suite.
