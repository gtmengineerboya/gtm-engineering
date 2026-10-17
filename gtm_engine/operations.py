"""Read-only aggregation of the historical Day 13 run log."""

from __future__ import annotations

import csv
import statistics
from pathlib import Path
from typing import Any


def summarize_run_log(path: Path) -> dict[str, Any]:
    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        required = {
            "status", "leads_processed", "duration_seconds",
        }
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("Run log is missing required columns")
        rows = list(reader)
    durations = []
    for row in rows:
        try:
            durations.append(float(row["duration_seconds"]))
        except (TypeError, ValueError):
            continue
    statuses: dict[str, int] = {}
    for row in rows:
        status = (row.get("status") or "UNKNOWN").strip().upper()
        statuses[status] = statuses.get(status, 0) + 1
    return {
        "run_count": len(rows),
        "status_counts": statuses,
        "leads_processed_total": sum(
            int(row.get("leads_processed") or 0)
            for row in rows
            if (row.get("leads_processed") or "").isdigit()
        ),
        "average_duration_seconds": (
            statistics.fmean(durations) if durations else None
        ),
        "failure_count": statuses.get("FAILED", 0),
    }
