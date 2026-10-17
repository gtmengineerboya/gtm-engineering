# Repository audit: Days 14â€“30

Audit date: 2026-10-15
Repository: `C:\gtm-engineering`
Python environment: `.venv`, Python 3.14.7
Git status at audit start: clean

## Current repository

The repository contains `day-01` through `day-13`, a root README, and four
foundation notes. It does not yet contain a root roadmap, completion matrix,
`.env.example`, a dependency manifest, pytest configuration, or a CI workflow.
No Day 14â€“30 folders existed at the start of this audit.

### Existing learning work

| Days | Verified contents and reusable work |
|---|---|
| 1â€“5 | Synthetic/sample lead CSV, introductory Python/API scripts, deterministic scoring, SQLite setup, SQL exercises, and a JSON GTM data model. The Day 4 database script uses a working-directory-relative database path. |
| 6 | Company/lead generation, enrichment, lead intelligence, AI analysis, outreach examples, and sample CSV outputs. |
| 7 | ICP scoring and an example scoring script. Running `day-07/test_scoring.py` currently stops with `NameError: calculate_score is not defined`; the script does not import the function it calls. |
| 8 | AI research, personalization, CRM-ready lead transformation, and CSV examples. These provide prior art but include exploratory code that is not yet a reusable, tested library. |
| 9 | HubSpot request examples, CSV imports, and company/contact association examples. Some scripts execute requests or mutations at module level and are not safe to import as test modules. |
| 10 | CSV enrichment and deterministic ICP scoring. `icp_scoring.py` reads and writes filenames relative to the current working directory, so its commands depend on where PowerShell is started. |
| 11 | Ollama-based outreach generation, deterministic message checks, retries/fallback behavior, and review CSV/XLSX outputs. The main script is organized into functions but is an end-to-end executable, not a standalone tested package. |
| 12 | HubSpot company matching/update, dry-run as the default, explicit `--apply`, and read-back verification. The script reads `day-09/.env`; it requires local credentials for live use and must not be run during offline testing. |
| 13 | `pipeline_runner.py` uses paths derived from `Path(__file__).resolve()`, validates Day 10/11 files, checks Ollama, launches Day 11, and logs success/failure. It explicitly does not run a HubSpot sync. `pipeline_api.py` exposes health/run/status endpoints, rejects a concurrent run with a lock, launches the runner in a daemon thread, and keeps run state in process memory. That state is lost on restart and is unbounded for the lifetime of the process; this is suitable for the local lesson, not durable production orchestration. |

The Day 13 run log is an existing tracked operational artifact with historical
rows. Preserve it; do not truncate or replace it. Existing CSV/XLSX learning
outputs are tracked and should be distinguished from newly generated local
reports rather than blindly removed.

## Configuration, paths, and safety observations

- `.gitignore` excludes `.env`, `gtm.db`, and `__pycache__/`, but does not yet
  cover common Python caches, virtual environments, temporary outputs, or
  private generated reports.
- Root `.env` and `day-09/.env` are ignored and are not tracked. Their contents
  were not inspected. Preserve the existing `day-09/.env` locally.
- There is no `.env.example`; add only variable names and safe placeholders.
- The configured `.venv` has FastAPI, requests, and supporting packages, but no
  pytest or `python-dotenv`. Prefer standard-library `unittest` for the offline
  curriculum and avoid adding a runtime dependency just for tests.
- Several early scripts use relative paths or perform work at import time.
  New lessons should use paths derived from `Path(__file__).resolve()` and
  guard executable entry points with `if __name__ == "__main__":`.
- Day 9/12 examples can contact or mutate HubSpot. Do not execute them during
  routine verification. All new CRM code will be mockable and dry-run by
  default; no live operation or paid enrichment is part of this work.
- Never read, print, copy, or commit either local `.env` file. Do not include
  credentials in workflow JSON or reports.

## Baseline verification

- Ran `.venv\Scripts\python.exe day-07\test_scoring.py`: **failed** with
  `NameError: calculate_score is not defined`. This is the only pre-change
  test command executed during the audit.
- Did not run scripts that contact Ollama, HubSpot, or other external APIs.
- Did not run Day 13 end-to-end because it requires Ollama and overwrites its
  review output/appends to the historical run log.

## Reusable architecture and planned additions

Keep the existing Days 1â€“13 intact except for narrowly scoped corrections
needed to make their tests/configuration coherent. Reuse Day 10's deterministic
scoring concepts, Day 11's evidence-aware copy validation, Day 12's exact-domain
matching and guarded write/read-back pattern, and Day 13's path resolution and
run logging. Do not import executable scripts with live side effects into new
code.

| Day | Planned practical implementation |
|---|---|
| 14 | Validate/normalize synthetic CRM records; mockable contact/company lookups; safe dry-run; opt-in flag and confirmation for live writes. |
| 15 | Reusable HTTP request/retry behavior with bounded retries, timeouts, backoff, rate-limit handling, and mocked tests. |
| 16 | Document Day 13 and provide a credential-free importable n8n workflow plus manual import/poll/failure instructions. |
| 17 | Deterministic funnel qualification/routing, reasons, CSV output, and boundary tests. |
| 18 | Normalized duplicate detection and a review-only report; no deletion or automatic merge. |
| 19 | Ollama research output schema with evidence/hypothesis separation, validation, and deterministic offline fallback. |
| 20 | Deterministic outreach-quality checks and human-review report; no send capability. |
| 21 | Mock-first CRM association/read-back workflow based only on verified configured schema; document where live schema confirmation is needed. |
| 22 | Portable analytical SQL and runnable SQLite examples, with PostgreSQL-only notes. |
| 23 | Unit-labelled GTM metrics, zero/missing-data handling, CSV plus Markdown reporting from synthetic inputs. |
| 24 | Local FastAPI webhook receiver with validation, event idempotency, and synthetic tests; no public exposure. |
| 25 | Offline standard-library test suite and CI workflow; tests require no CRM token, Ollama, or paid service. |
| 26 | Run/health operational summary and log redaction, evaluated against Day 13's existing log design. |
| 27 | Safe configuration, input limits, timeout/log-redaction checks, and documented secret/scope practices without reading local secrets. |
| 28 | Synthetic end-to-end pipeline with deterministic local components, human-approval boundary, default dry-run, and no outreach. |
| 29 | Portfolio architecture, synthetic test metrics, interview Q&A, and demo walkthrough based only on implemented behavior. |
| 30 | Reproducible validation, final assessment, complete 30-day matrix, known limitations, and manual-service setup report. |

Each new day will have a practical README, implementation/data/tests as
appropriate, beginner-friendly learning notes, and a checkpoint with answers.
Root navigation will link every day and include Windows PowerShell commands.

## Risks and decisions

1. **Live CRM risk:** Keep live writes out of tests and the capstone. Any new
   live write path must require deliberate opt-in and a confirmation prompt.
2. **Local-state risk:** Preserve all existing files and historical reports;
   ignore future private/local reports without hiding reproducible fixtures.
3. **External service risk:** Make Ollama and n8n examples optional and document
   manual UI actions. Test core behavior offline with mocks/synthetic inputs.
4. **Windows path risk:** Resolve project paths from each script's own location.
5. **Scope risk:** The new curriculum will be implemented in verified groups,
   not generated as one large untested code dump. Any feature that cannot be
   run because a local service is absent will be identified as not run rather
   than reported as passing.
