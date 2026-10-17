"""Produce a non-destructive duplicate review CSV."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gtm_engine.deduplication import review_duplicates


DAY_DIR = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DAY_DIR / "sample_leads.csv")
    parser.add_argument("--output", type=Path,
                        default=DAY_DIR / "output" / "duplicate_review.csv")
    args = parser.parse_args()
    with args.input.open(newline="", encoding="utf-8-sig") as file:
        records = list(csv.DictReader(file))
    reviews = review_duplicates(records)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = list(reviews[0]) if reviews else [
        "record_number", "possible_match_record", "match_key",
        "normalized_key", "review_status", "safe_merge_candidate", "reason",
    ]
    with args.output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(reviews)
    print(f"Found {len(reviews)} candidate pairs; no records were changed.")


if __name__ == "__main__":
    main()
