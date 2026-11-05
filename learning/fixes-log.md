# Fixes log: what was wrong in the original project and what to learn from it

Review everything with `git diff` before you commit. Nothing is committed yet.

## Why this file exists
The `learning/` folder is a map plus clean practice. This log is the other half:
the real mistakes in your own code, fixed in place, with the lesson for each.

## Fixes (day-02 to day-13, plus day-22 SQL)

| Problem in the original | Fix | What to learn |
|---|---|---|
| Relative file paths ("companies.csv") only worked from the script's own folder. day-10/icp_scoring.py crashed from the repo root. | Anchor paths: Path(__file__).resolve().parent / "file.csv" | Scripts must work from any folder. Never trust the current working directory. |
| Code ran at import time (no __main__ guard). Importing advanced_scoring.py from a test printed the whole demo. | Demo moved under the guard. Files with big prompt/SQL strings got a refuse-import guard so strings were not altered. | Separate reusable functions from code that runs. Tests import; they must not trigger side effects. |
| exit() used in scripts. | sys.exit(1) | exit() is for the interactive shell. Scripts return a real exit code so automation sees failure. |
| requests calls with no timeout (can hang forever). | 30s for APIs, 120s for slow local Ollama calls (day-06, day-08, matching day-11). | Every network call needs a timeout, chosen from how slow the service really is. |
| day-04/gtm_database.py: relative DB path, connection left open. | DB_PATH anchored to repo, closing(...) context, PRAGMA foreign_keys = ON, importable function plus main guard. | SQLite ignores foreign keys unless enabled. Always close connections. |
| day-04/queries.sql was not runnable (comments and pasted lesson text). | 10 real queries: filter, ORDER BY, COUNT, JOINs, GROUP BY, CASE. | A query file must run top to bottom. |
| day-10 lead_enrichment.py / icp_scoring.py used paths relative to the current folder. | Anchored to script and repo root. Output byte-identical to before. | Same path lesson. |
| pytest.ini had no test location. | Added testpaths = tests. | Tell pytest where tests live. |
| day-22/funnel_analysis.sql counted each lead only at its current stage, so conversion rates were wrong (MQL to SQL showed 50%, should be 60% on the sample). | Cumulative counts using IN (...) for the current and later stages. | A funnel is cumulative: someone who is now a Customer also passed MQL, SQL and Opportunity. |
| day-13/pipeline_runner.py accepted an old outreach report as success if the new run wrote nothing. | Report must be modified during this run (validate_output(run_started_at)). Test: tests/test_day13_runner.py. | After a step that should produce a file, prove the file is new. Existence is not evidence. |
| day-13 runner and API both had a 900s timeout, so the API could kill the runner mid-run. | Runner's outreach step now times out at 780s, so it logs the failure and stops its own child first. | Inner timeouts must be shorter than outer ones. |

## Side effects you might notice
- Day 7 demo no longer prints when imported (still prints when run directly).
- Day 10 messages show absolute paths.
- My first pass accidentally converted files to Windows line endings (CRLF), which made git diff show every line changed. Reversed; the diff now shows only real changes.

## Not touched
day-13/*, day-11/personalized_outreach.py, day-12/hubspot_ai_sync.py, gtm_engine/*, tests, and every .env file (never opened).

## Verified vs not
- Verified: every changed .py compiles. Offline scripts (day-04 DB and queries, day-10 scoring) give the same results before and after, tested on throwaway copies.
- Not run live: HubSpot, Ollama and n8n scripts. Checked for syntax and import safety only. Run them against a test account.

## Still open on purpose (your drills)
Pagination, logging, pydantic validation, pandas, retries in the Day 6-12 scripts. See python-skills.md drills D1-D12.
