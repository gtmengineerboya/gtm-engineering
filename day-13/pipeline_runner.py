
import csv
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "day-10" / "scored_leads.csv"
OUTREACH_SCRIPT = ROOT / "day-11" / "personalized_outreach.py"
REVIEW_FILE = ROOT / "day-11" / "outreach_review.csv"
LOG_FILE = ROOT / "day-13" / "run_logs.csv"

REQUIRED_COLUMNS = {
    "company_name",
    "personalized_message",
    "validation_status",
}

APPROVED_STATUSES = {"APPROVED_AI", "APPROVED_FALLBACK"}


def log_run(run_id, status, processed=0, approved=0,
            review_required=0, duration=0, details=""):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    exists = LOG_FILE.exists()

    with LOG_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "run_id",
                "timestamp_utc",
                "status",
                "leads_processed",
                "approved_messages",
                "review_required",
                "duration_seconds",
                "details",
            ],
        )

        if not exists or LOG_FILE.stat().st_size == 0:
            writer.writeheader()

        writer.writerow({
            "run_id": run_id,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "status": status,
            "leads_processed": processed,
            "approved_messages": approved,
            "review_required": review_required,
            "duration_seconds": round(duration, 2),
            "details": details,
        })


def check_ollama():
    url = "http://localhost:11434/api/tags"

    try:
        with urlopen(url, timeout=5) as response:
            if response.status != 200:
                raise RuntimeError(f"Ollama returned HTTP {response.status}")

            payload = json.loads(response.read().decode("utf-8"))
            models = [
                model.get("name", "")
                for model in payload.get("models", [])
            ]

            if not any(name.startswith("llama3.2:3b") for name in models):
                raise RuntimeError(
                    "Model llama3.2:3b was not found. Check `ollama list`."
                )

    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(
            "Ollama is unavailable. Check that Ollama is running."
        ) from exc


def validate_input():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input CSV not found: {INPUT_FILE}")

    with INPUT_FILE.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("Input CSV has no header row.")

        if "company_name" not in reader.fieldnames:
            raise ValueError(
                "Input CSV is missing company_name. "
                "Check the Day 10 field mapping."
            )

        rows = list(reader)

    if not rows:
        raise ValueError("Input CSV contains no lead rows.")

    return len(rows)


def validate_output():
    if not REVIEW_FILE.exists():
        raise FileNotFoundError(
            f"Outreach report was not created: {REVIEW_FILE}"
        )

    with REVIEW_FILE.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("Outreach report has no header row.")

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError(
                f"Outreach report is missing columns: {sorted(missing)}"
            )

        rows = list(reader)

    if not rows:
        raise ValueError("Outreach report contains no messages.")

    approved = 0
    review_required = 0

    for row in rows:
        status = (row.get("validation_status") or "").strip()
        message = (row.get("personalized_message") or "").strip()

        if status in APPROVED_STATUSES and message:
            approved += 1
        else:
            review_required += 1

    return len(rows), approved, review_required


def main():
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    started = time.monotonic()

    print(f"Run ID: {run_id}")
    print("Step 1/4: Checking input data...")
    processed = validate_input()
    print(f"Input contains {processed} leads.")

    print("Step 2/4: Checking local Ollama...")
    check_ollama()
    print("Ollama is available.")

    print("Step 3/4: Running AI outreach generation...")
    result = subprocess.run(
        [sys.executable, str(OUTREACH_SCRIPT)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=900,
    )

    if result.stdout:
        print(result.stdout)

    if result.returncode != 0:
        raise RuntimeError(
            "Outreach script failed. "
            f"Exit code: {result.returncode}. "
            f"Error: {result.stderr[-2000:]}"
        )

    print("Step 4/4: Validating the generated report...")
    total, approved, review_required = validate_output()

    duration = time.monotonic() - started
    details = (
        "Report generated. Human review is required before any live outreach. "
        "HubSpot sync was not run."
    )

    log_run(
        run_id=run_id,
        status="SUCCESS",
        processed=total,
        approved=approved,
        review_required=review_required,
        duration=duration,
        details=details,
    )

    print("\nPipeline completed successfully.")
    print(f"Leads in report: {total}")
    print(f"Approved by code checks: {approved}")
    print(f"Review required: {review_required}")
    print(f"Report: {REVIEW_FILE}")
    print(f"Run log: {LOG_FILE}")
    print("HubSpot sync: NOT RUN; human review required.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"\nPIPELINE FAILED: {exc}", file=sys.stderr)
        try:
            log_run(
                run_id=datetime.now(timezone.utc).strftime(
                    "%Y%m%dT%H%M%SZ"
                ),
                status="FAILED",
                details=str(exc)[:1000],
            )
        except Exception as log_error:
            print(f"Could not write failure log: {log_error}", file=sys.stderr)
        sys.exit(1)
