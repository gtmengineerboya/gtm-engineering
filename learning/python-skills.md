# Python skills map for GTM engineering

**What this is:** every Python skill your projects use or need, sorted into four
groups so you can see at a glance what you have learned, what you must use
daily, what to strengthen, and what to add.

**How I built it:** I read your code in `day-02` to `day-30`, `gtm_engine/` and
`tests/`, and searched it for which Python features appear. "Not found" below means
I searched the whole repo (excluding `.venv`) and found zero uses. Where I say you
"use" something, a file is named so you can check it yourself.

| Tag | Meaning |
|---|---|
| **LEARNED** | You have written working code that uses it |
| **DAILY** | You will use it constantly in a GTM engineer job |
| **STRENGTHEN** | You touched it but it is shaky, partial or messy in your code |
| **ADD** | Not in your repo yet, and the job market expects it |

A skill can be both LEARNED and DAILY. That is good: it means keep it sharp.

---

## 1. LEARNED: what your code already proves

For each row, the last column is a question you should be able to answer out loud
without looking. If you cannot, that skill is not yet yours.

| Skill | Where you used it | Test yourself |
|---|---|---|
| Read and write CSV | `day-17/route_leads.py` (`csv.DictReader`, `DictWriter`) | Why `encoding="utf-8-sig"` and `newline=""`? |
| JSON load and dump | `day-19/research_leads.py`, `day-16/pipeline_workflow.json` | `json.load` vs `json.loads`? |
| Paths with `pathlib` | `day-17/route_leads.py` (`Path(__file__).resolve()`) | Why not a plain relative path? (Your Day 4 database bug) |
| Functions, modules, a package | `gtm_engine/` | Why does `day-17` do `sys.path.insert`? What would be cleaner? |
| Dicts as records, `.get()` | `gtm_engine/crm.py` | `record["x"]` vs `record.get("x")`? |
| String cleaning | `gtm_engine/crm.py` (`normalize_email`, `normalize_domain`) | `casefold()` vs `lower()`? |
| Regular expressions | `gtm_engine/deduplication.py` (`normalize_name`) | What does `[^a-z0-9]` match? |
| Validation by raising errors | `gtm_engine/research.py` (`validate_research`) | When `raise ValueError` vs return `False`? |
| HTTP with `requests` | `day-09/*.py`, `gtm_engine/http_client.py` | What does `raise_for_status()` do? |
| Retries, backoff, idempotency | `gtm_engine/http_client.py` | Why is a POST not retried without an Idempotency-Key? |
| Secrets and environment variables | `gtm_engine/config.py`, `gtm_engine/security.py` | Why is `.env` in `.gitignore`? |
| Command-line tools | `day-17/route_leads.py` (`argparse`) | What does `if __name__ == "__main__":` protect? |
| Type hints | `from __future__ import annotations`, `Protocol` in `gtm_engine/crm.py` | Does Python enforce them at runtime? |
| Hashing and HMAC | `gtm_engine/webhooks.py` (`verify_signature`) | Why `hmac.compare_digest` and not `==`? |
| SQLite from Python | `gtm_engine/webhooks.py`, `day-04/gtm_database.py` | Why `?` placeholders instead of f-strings in SQL? |
| Unit tests and mocks | `tests/*.py` (`unittest`, `Mock`, `patch`) | What does `patch` replace, and when does it restore it? |
| FastAPI basics | `day-13/pipeline_api.py`, `gtm_engine/webhooks.py` | What does a `409` mean in your pipeline API? |
| Threads and locks | `day-13/pipeline_api.py` | Why a `Lock` around starting a run? |
| UTC timestamps | `gtm_engine/webhooks.py` (`datetime.now(timezone.utc)`) | Why store UTC? |

---

## 2. DAILY: what you will do every day on the job

These are the ten things GTM engineers actually do in Python. Columns show what
you already have and what is still missing.

| # | Daily task | You already have | Still missing |
|---|---|---|---|
| 1 | Pull records from a vendor API, all pages | `requests` calls, retries | **Pagination** (none found in your repo) |
| 2 | Reshape messy JSON into clean fields | Dict handling, `.get()` | Comprehensions on nested data, pydantic |
| 3 | Clean and dedupe CSV exports | `csv`, `normalize_*`, `deduplication.py` | **pandas** (none found) |
| 4 | Waterfall enrichment: try provider A, then B, then C | Retry logic | A reusable waterfall function with cost and timeout tracking |
| 5 | Call an LLM and trust the result safely | `research.py` schema checks, Ollama | pydantic validation, retries on bad JSON, evals |
| 6 | Receive webhooks and respond fast | `webhooks.py` with HMAC and dedupe | Background processing, retries from the sender side |
| 7 | Run jobs on a schedule | GitHub Actions CI | Scheduled jobs, alerts on failure |
| 8 | Debug from logs when something broke at 2 a.m. | Run logs CSV | **The `logging` module** (none found, many `print` calls) |
| 9 | Write small tools teammates can run | `argparse` scripts | Clear errors, `--dry-run` everywhere, README per tool |
| 10 | Read a new vendor's docs and ship in a day | Day 9 to 12 HubSpot work | Practice on 3 different vendor APIs |

---

## 3. STRENGTHEN: learned but not yet job-grade

1. **Script hygiene in Days 6 to 12.** Several scripts run at import time, call
   `exit()`, and use `load_dotenv("day-09/.env")`, which breaks if you start from a
   different folder. Your newer `gtm_engine/` code is much better. Bring the old
   code up to that standard.
2. **`print` instead of logging.** `day-08/ai_research.py` alone has dozens of
   `print` calls. Real systems need levels (info, warning, error) and files.
3. **Everyday collection idioms.** List comprehensions, `sorted(key=...)`,
   `enumerate`, `zip`, `set` operations and `any`/`all` appear only a handful of
   times. They are how Python reads fluently, so practise until they are automatic.
4. **Testing depth.** You use `unittest` only. Teams use **pytest** (fixtures,
   `parametrize`, `tmp_path`). Your `pytest.ini` exists but only one file uses it.
5. **Types are written but never checked.** Run a type checker (`mypy` or
   `pyright`) so the hints actually catch bugs.
6. **Records as loose dicts.** Everything is `dict[str, str]`. Typos in a key
   name fail silently. Move to dataclasses or pydantic models.
7. **HTTP depth.** You handle `Retry-After` well, but you have only used
   synchronous `requests` and never a `Session` for many calls.

---

## 4. ADD: not in your repo, expected by the market

| Skill | Why it matters | First small win |
|---|---|---|
| **pandas** | Standard for cleaning, merging and de-duplicating lead lists | Re-do Day 18 duplicate detection in 15 lines of pandas |
| **pydantic** | Validates API payloads and LLM JSON with clear errors | Replace `validate_research` with a model |
| **logging** | Debuggable, auditable pipelines | Add file logging with your existing redaction |
| **Pagination and rate limits** | Every real CRM and enrichment API paginates | Fetch all HubSpot contacts using the `after` cursor |
| **async and `httpx`** | Enrich hundreds of rows in parallel without hitting limits | Fetch 20 URLs, 5 at a time |
| **Generators (`yield`)** | Stream large files without loading all rows | Write a CSV chunk reader |
| **dataclasses** | Lightweight typed records | Model a `Lead` |
| **Postgres from Python** (`psycopg`) | Where real GTM data lives | Connect and run `sql-practice/answers.sql` on Postgres |
| **JavaScript basics** | n8n code nodes and many automation tools use JavaScript, and job posts list it with Python | Read and tweak a 20-line n8n code node |
| **Scheduling and alerting** | Production means it runs without you | Scheduled GitHub Action that posts failures to Slack |

---

## 5. Twelve drills, in order

Do these in your repo. Each is small, testable and builds a portfolio habit.
"Done when" is your pass mark.

| # | Drill | Files | Done when |
|---|---|---|---|
| D1 | Make `day-09/csv_to_hubspot_idempotent.py` import-safe: functions, a `main()` guard, no `exit()`, no relative `.env` path | `day-09/csv_to_hubspot_idempotent.py` | Importing it prints nothing and calls nothing; 3 new tests pass |
| D2 | Replace `print` with `logging` in one script, writing to a file, with `redact_sensitive_text` applied | `day-08/ai_research.py`, `gtm_engine/security.py` | Log file has levels, no secrets |
| D3 | Write `fetch_all(url, token)` that follows `paging.next.after` and stops safely | new `gtm_engine/pagination.py` | Test with a mock returning 3 pages; then a real test account |
| D4 | Rebuild duplicate review with pandas and compare outputs | `day-18/`, `gtm_engine/deduplication.py` | Same matches as the current module on the sample CSV |
| D5 | Replace `validate_research` with a pydantic model | `gtm_engine/research.py` | Existing tests still pass |
| D6 | Convert one test class to pytest with `parametrize` | `tests/test_days14_18.py` | `pytest` runs it and the old runner still works |
| D7 | Rewrite 5 `for` loops in Day 6 scripts as comprehensions or built-ins | `day-06/*.py` | Same outputs, fewer lines, still readable |
| D8 | Fetch 20 URLs concurrently with `httpx` and a limit of 5 at a time | new `drills/async_fetch.py` | Faster than sequential; no more than 5 in flight |
| D9 | Add a test that a webhook with a bad signature is rejected | `gtm_engine/webhooks.py`, `tests/test_days19_24.py` | Test fails if you break `verify_signature` |
| D10 | Write `waterfall(providers, record)` with a per-provider timeout, a log line and a cost counter | new `gtm_engine/waterfall.py` | 4 tests: first hit, fallback, all fail, timeout |
| D11 | Write your own retry decorator using `functools.wraps` | new `gtm_engine/retry.py` | Same behaviour as `request_with_retries` for a plain function |
| D12 | Run `mypy` on `gtm_engine/` and fix the first 10 findings | `gtm_engine/` | Ten fewer type errors, tests still pass |

**Rule for every drill:** write the test first or alongside, run it, then commit.
If you are stuck for more than 30 minutes, bring me the error and we debug together.

---

## 6. Self-assessment tracker

Score honestly. 0 = cannot do it. 1 = can follow code that does it. 2 = can write
it with the docs open. 3 = can write it from memory and explain it to someone else.
Fill the last two columns yourself and re-score every two weeks.

| Skill | Target by week 12 | Level now | Date re-scored |
|---|---|---|---|
| Collections and comprehensions | 3 | | |
| Functions, modules, imports | 3 | | |
| Files, CSV, JSON, pathlib | 3 | | |
| Errors and validation | 3 | | |
| HTTP, auth, retries | 3 | | |
| Pagination and rate limits | 3 | | |
| pandas | 2 | | |
| pydantic and dataclasses | 2 | | |
| logging | 3 | | |
| pytest and mocks | 3 | | |
| async and `httpx` | 2 | | |
| Postgres from Python | 2 | | |
| FastAPI and webhooks | 2 | | |
| Type checking | 2 | | |

## 7. When to do what (matches the 12-week plan)

- **Phase 0 (week 1):** D1, D6
- **Phase 1 (weeks 2 to 4):** D3, D4, D10
- **Phase 2 (weeks 5 to 8):** D2, D7, D11
- **Phase 3 (weeks 9 to 10):** D5, D8
- **Phase 4 (weeks 11 to 12):** D9, D12

Related file: `sql-skills.md`.
