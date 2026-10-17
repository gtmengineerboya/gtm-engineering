# Demo walkthrough (about five minutes)

1. Show the root README and explain that Days 1–30 are a learning repository.
2. Run `day-28/run_capstone.py` and open `day-28/output/capstone_report.csv`.
3. Trace one synthetic record through normalization, score, lifecycle, owner
   queue, evidence facts, message-quality status, approval gate, and CRM dry run.
4. Show `python -m unittest discover -s tests -v` and explain mock-based API and
   webhook checks.
5. Explain that n8n import, Ollama availability, and HubSpot schema/token setup
   are local/manual and were not needed for the offline demo.

Do not use real prospect data or claim that a synthetic score is a conversion
result. Do not activate the n8n workflow or run a live CRM write during a demo.
