

from pathlib import Path
from threading import Lock, Thread
from datetime import datetime, timezone
import subprocess
import sys
import uuid

from fastapi import FastAPI, HTTPException

ROOT = Path(__file__).resolve().parent.parent
PIPELINE = ROOT / "day-13" / "pipeline_runner.py"

app = FastAPI(title="GTM Pipeline API")

lock = Lock()
runs = {}


@app.get("/health")
def health():
    return {"status": "ok", "service": "gtm-pipeline"}


def execute_pipeline(run_id):
    try:
        result = subprocess.run(
            [sys.executable, str(PIPELINE)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=900,
            check=False,
        )

        with lock:
            runs[run_id].update({
                "status": "success" if result.returncode == 0 else "failed",
                "return_code": result.returncode,
                "stdout": result.stdout[-4000:],
                "stderr": result.stderr[-4000:],
            })
    except subprocess.TimeoutExpired:
        with lock:
            runs[run_id].update({
                "status": "failed",
                "error": "Pipeline exceeded 15 minutes",
            })
    except Exception as exc:
        with lock:
            runs[run_id].update({
                "status": "failed",
                "error": str(exc),
            })


@app.post("/run-pipeline", status_code=202)
def run_pipeline():
    with lock:
        if any(r["status"] == "running" for r in runs.values()):
            raise HTTPException(
                status_code=409,
                detail="A pipeline run is already in progress",
            )

        run_id = str(uuid.uuid4())
        runs[run_id] = {
            "status": "running",
            "started_at": datetime.now(timezone.utc).isoformat(),
        }

    Thread(target=execute_pipeline, args=(run_id,), daemon=True).start()

    return {"run_id": run_id, "status": "running"}


@app.get("/run-status/{run_id}")
def run_status(run_id: str):
    with lock:
        run = runs.get(run_id)

    if run is None:
        raise HTTPException(status_code=404, detail="Run ID not found")

    return {"run_id": run_id, **run}

