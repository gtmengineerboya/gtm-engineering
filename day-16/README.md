# Day 16 — Orchestrating the pipeline with n8n

This day documents the real Day 13 FastAPI contract and includes an
importable, credential-free n8n workflow. It starts exactly one pipeline run,
then polls that run's status; it never starts another run while polling. The
standalone Python client has a bounded timeout and raises on an API error.

Start FastAPI in one PowerShell window:

```powershell
Set-Location C:\gtm-engineering
C:\gtm-engineering\.venv\Scripts\python.exe -m uvicorn day-13.pipeline_api:app --host 127.0.0.1 --port 8000
```

In a second window, run the client:

```powershell
C:\gtm-engineering\.venv\Scripts\python.exe C:\gtm-engineering\day-16\pipeline_status_client.py --timeout 900
```

In n8n, import `day-16/pipeline_workflow.json`, keep the default local
`127.0.0.1` URL when n8n runs on the same host, then manually run it. If n8n is
in a container, replace the URL with the host address reachable from that
container. Review the JSON before activation. A workflow export is not proof
that it was imported or activated. The pipeline itself still needs Day 10/11
files and local Ollama.

Workflow nodes: manual trigger → one `POST /run-pipeline` → three-second wait
→ `GET /run-status/{run_id}` → loop while `running` → success/failure output.
The exported workflow has a 15-minute execution timeout and separate error
outputs for trigger/status HTTP failures. The standalone Python client also
has a caller-controlled timeout; timing out does not cancel a run already
accepted by FastAPI.

Use either the n8n workflow or the Python trigger-and-poll client for a run,
not both. Troubleshooting: a 409 means another run is active; wait for it to
finish instead of retrying the trigger. For a failed status, inspect the
returned run details and local logs.
