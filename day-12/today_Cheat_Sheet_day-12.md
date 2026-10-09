# GTM Engineering — Daily Cheat Sheet
**Date:** 9 October 2026
**Project:** `C:\gtm-engineering`
**Focus:** AI-personalized outreach, validation, and HubSpot CRM synchronization

---

## 1. Today's goal

Complete the Day 11–12 workflow so the GTM pipeline can:

1. Read and score synthetic company records.
2. Generate personalized outreach messages with a local LLM.
3. validate messages and create a review report.
4. Sync approved messages to existing HubSpot company records using exact domain matches.
5. Verify that the CRM values were actually updated.

> **Important:** The companies use synthetic names and `.example.com` domains. This demonstrates that the pipeline mechanics work; it does not establish real-world prospect conversion or validate actual company details.

## 2. Work completed

### Day 11 — AI outreach generation and review

- Used the local Ollama model `llama3.2:3b`.
- Sent generation requests to `http://localhost:11434/api/generate`.
- Generated outreach messages from the scored lead data.
- Added deterministic checks and retry/fallback behavior.
- Produced `day-11/outreach_review.csv` with the message, validation status, and reason.
- Last reported result:
  - 11 leads processed
  - 4 AI-generated messages passed checks
  - 7 fallback messages approved
  - 0 messages marked `REVIEW_REQUIRED`

**Interpretation:** Passing code checks does not guarantee that a message is factually correct. Human review is still required before sending outreach.

### Day 12 — HubSpot synchronization

- Updated `day-12/hubspot_ai_sync.py` to read `day-11/outreach_review.csv`.
- Restricted updates to approved messages.
- Matched existing HubSpot companies by **exact domain**, not company name, because duplicate company names existed.
- Updated only the `outreach_message` property in this version of the script.
- Used a dry run before applying changes.
- Used `--apply` for live updates.
- Read the property back from HubSpot to verify the update.
- Last reported result: 11 successful updates, 0 skipped, 0 failed. The generated `day-12/sync_results.csv` recorded successful read-back verification.

## 3. Files to know

| File | Purpose |
|---|---|
| `day-10/lead_enrichment.py` | Enriches company records and maps source fields such as `company` to `company_name`. |
| `day-10/companies.csv` | Synthetic source-company data, if present in the local project. |
| `day-10/scored_leads.csv` | Scored and qualified synthetic leads. |
| `day-11/personalized_outreach.py` | Generates and validates AI-assisted outreach. |
| `day-11/outreach_review.csv` | Review report with message and validation columns. |
| `day-12/hubspot_ai_sync.py` | Dry-run/live HubSpot message synchronization and read-back verification. |
| `day-12/sync_results.csv` | Per-record sync outcomes. |
| `day-09/.env` | Local credentials/configuration file. **Never commit or share it.** |

File names can vary if you have renamed or reorganized your local project. Check `dir day-11` or `dir day-12` if a path is missing.

## 4. Commands used / useful troubleshooting commands

Run these in **Windows PowerShell** from the project root:

```powershell
# Move to the repository
cd C:\gtm-engineering

# Check current directory and files
Get-Location
dir
dir day-11
dir day-12

# Check Git changes before committing
git status
git diff -- day-11/personalized_outreach.py day-12/hubspot_ai_sync.py
git diff --check

# Run AI outreach generation
python day-11/personalized_outreach.py

# Preview HubSpot sync without making live changes
python day-12/hubspot_ai_sync.py

# Apply approved messages to HubSpot
python day-12/hubspot_ai_sync.py --apply

# Check Python version
python --version

# Check that the local Ollama endpoint is reachable
Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get

# Check whether the Ollama model is installed
ollama list

# Test whether the requests package is installed
python -c "import requests; print(requests.__version__)"

# Install requests only if the import above fails
python -m pip install requests

# Review the sync result report
Import-Csv day-12/sync_results.csv | Format-Table -AutoSize

# Review outreach status counts
Import-Csv day-11/outreach_review.csv |
  Group-Object validation_status |
  Select-Object Name, Count

# Check whether the .env file is tracked by Git
git ls-files day-09/.env

# Check whether Git sees the .env file as ignored
git check-ignore day-09/.env
```

**Troubleshooting notes**

- **Ollama connection error:** Ensure Ollama is running, then run `ollama list` and test `/api/tags`.
- **Model not found:** Pull the model only if needed: `ollama pull llama3.2:3b`.
- **Missing Python package:** Test the import first; install the missing package in the active Python environment.
- **HubSpot authentication failure:** Check that the token variable is set in `day-09/.env` and that the token has the required CRM permissions. Do not paste the token into chat or terminal screenshots.
- **No exact-domain match:** Check that the input domain and HubSpot domain are identical. Do not fall back to company-name matching when duplicates are possible.
- **Update fails:** Read the error in `day-12/sync_results.csv`, verify the HubSpot property name, permissions, and API response.
- **Line-ending warning (LF/CRLF):** This is commonly a Git line-ending notice, not necessarily a failure. Check `git diff` and `git status`.
- **Hosted parallelism error in Azure Pipelines:** This was a separate earlier lab issue; it is not part of today's HubSpot sync. Do not assume it is resolved by today's work.

## 5. What changed to reach the goal

1. **Field mapping:** The lead enrichment flow maps the source `company` field to `company_name`, so downstream steps use a consistent company-name field.
2. **AI personalization:** The outreach script uses Ollama rather than requiring a paid hosted LLM API.
3. **Validation and fallback:** Messages are checked; when an AI message fails checks, a fallback message can be used.
4. **Reviewable output:** `outreach_review.csv` makes messages and validation outcomes inspectable before CRM updates.
5. **Safer CRM matching:** Exact domain matching avoids updating the wrong record when company names are duplicated.
6. **Controlled updates:** Dry-run mode previews changes; `--apply` explicitly enables live updates.
7. **Read-back verification:** The script fetches the value after updating and records whether it matches.

## 6. Safe Git workflow

First inspect what will be committed:

```powershell
cd C:\gtm-engineering
git status
git diff --check
git diff --stat
```

Confirm secrets are not staged. Do not use `git add .` until you have reviewed every changed and untracked file. If appropriate, stage only the source files and non-sensitive reports you intend to preserve:

```powershell
git add day-11/personalized_outreach.py day-12/hubspot_ai_sync.py
# Add reports only if they contain no secrets or personal/prospect data:
# git add day-11/outreach_review.csv day-12/sync_results.csv

git status
git diff --cached --check
git diff --cached
```

If the staged diff is correct:

```powershell
git commit -m "Complete AI outreach validation and HubSpot sync"
git push
```

If `day-09/.env` appears in the staged changes, unstage it before proceeding:

```powershell
git restore --staged day-09/.env
```

If it was already committed or pushed, removing it from a later commit is not enough; rotate/revoke the exposed credential and clean the repository history as appropriate.

## 7. Human review checklist

Before using this workflow on real prospects, verify each message:

- [ ] Uses only verified company facts.
- [ ] Does not invent company initiatives, pain points, or recent events.
- [ ] Gives a credible reason for contacting the prospect.
- [ ] Is professional, concise, and relevant.
- [ ] Includes a clear, low-pressure call to action.
- [ ] Has no misleading claims or promises.
- [ ] Is appropriate under applicable privacy, marketing, and anti-spam rules.

Do not send messages to the synthetic `.example.com` records. Test with real, lawfully sourced prospect data only after verifying it.

## 8. Definition of done for this workflow

- [x] AI outreach generated for 11 synthetic leads.
- [x] Validation/review report created.
- [x] HubSpot dry run performed.
- [x] Approved messages synced to existing records by exact domain.
- [x] HubSpot values read back for verification.
- [ ] Human review of the actual message text completed.
- [ ] Git changes reviewed, committed, and pushed (confirm with `git status`).

## 9. Next action

Run:

```powershell
cd C:\gtm-engineering
git status
```

Review the output before staging files. Keep `.env`, access tokens, and any sensitive data out of Git. After the repository state is confirmed, continue to the next GTM Engineering milestone.
