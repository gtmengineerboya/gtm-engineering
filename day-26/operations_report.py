"""Summarize Day 13 run logs without editing the historical log."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gtm_engine.operations import summarize_run_log


def main():
    source = ROOT / "day-13" / "run_logs.csv"
    summary = summarize_run_log(source)
    output = Path(__file__).resolve().parent / "output"
    output.mkdir(parents=True, exist_ok=True)
    (output / "operations_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    print(f"Read-only report: {output / 'operations_summary.json'}")


if __name__ == "__main__":
    main()
