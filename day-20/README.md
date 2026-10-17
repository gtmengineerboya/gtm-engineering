# Day 20 — AI outreach quality evaluation

Evaluate copy with deterministic checks for length, company-name relevance,
generic openings, and unsupported claims:

```powershell
C:\gtm-engineering\.venv\Scripts\python.exe C:\gtm-engineering\day-20\evaluate_outreach.py
```

The CSV under `day-20\output\` records a status and reasons. Passing means only
that the listed checks passed; every row still requires a human review. This
exercise contains no send function and never contacts a prospect. Tests:
`python -m unittest discover -s tests -p "test_days19_24.py" -v`.

Troubleshooting: deterministic rules can miss nuance and can flag harmless
wording; edit rules only with examples and keep human approval before outreach.

For an optional model judgment of tone, clarity, call-to-action quality,
personalization, and grounding, add `--ollama`. It reads only the synthetic
draft file and reports unavailable or malformed model output separately.
Model ratings do not override deterministic failures or human review.
