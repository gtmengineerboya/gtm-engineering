# Day 19 — AI research with factuality controls

`research_leads.py` writes structured research for synthetic company profiles.
By default, it uses a deterministic offline fallback. Add `--ollama` only when
the local Ollama service is available and you intentionally want a model call:

```powershell
C:\gtm-engineering\.venv\Scripts\python.exe C:\gtm-engineering\day-19\research_leads.py
C:\gtm-engineering\.venv\Scripts\python.exe C:\gtm-engineering\day-19\research_leads.py --ollama
```

The JSON report is written under `day-19\output\`. Observed facts must copy
input field values exactly; hypotheses are explicitly labeled and cite input
fields. A bad response or unavailable Ollama produces a documented fallback.
Tests: `python -m unittest discover -s tests -p "test_days19_24.py" -v`.
Troubleshooting: check Ollama is running and has the configured model; fallback
is still a valid offline result, not proof that AI research ran.
