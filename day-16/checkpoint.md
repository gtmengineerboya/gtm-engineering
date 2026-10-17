# Day 16 checkpoint

1. **Why does polling use a run ID?** It observes one execution without
   triggering more executions.
2. **What does HTTP 409 mean here?** A different run is already active; wait
   rather than submit another trigger.
3. **What is not automatic?** Importing/activating the workflow in the local
   n8n UI and starting FastAPI/Ollama require deliberate local actions.

Practice: run `/health`, then review `pipeline_workflow.json` and identify its
single trigger and status request.
