"""Write deterministic lifecycle and owner decisions for sample leads."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gtm_engine.funnel import route


DAY_DIR = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DAY_DIR / "sample_leads.csv")
    parser.add_argument("--output", type=Path,
                        default=DAY_DIR / "output" / "routing_decisions.csv")
    args = parser.parse_args()
    with args.input.open(newline="", encoding="utf-8-sig") as file:
        leads = list(csv.DictReader(file))
    if not leads:
        raise ValueError("Input CSV has no lead rows")
    decisions = [route(lead) for lead in leads]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(decisions[0]))
        writer.writeheader()
        writer.writerows(decisions)
    print(f"Routed {len(decisions)} leads to {args.output}")


if __name__ == "__main__":
    main()
