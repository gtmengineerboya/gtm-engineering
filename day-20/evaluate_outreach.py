"""Create a human-review report from synthetic outreach drafts."""

from __future__ import annotations

import csv
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gtm_engine.outreach import evaluate_message, model_judgment


DAY_DIR = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ollama", action="store_true",
                        help="Opt in to a local model judgment.")
    args = parser.parse_args()
    with (DAY_DIR / "sample_messages.csv").open(
        newline="", encoding="utf-8-sig"
    ) as file:
        rows = list(csv.DictReader(file))
    output_rows = []
    for row in rows:
        result = evaluate_message(
            row["company_name"],
            row["message"],
            [row.get("evidence_phrase", "")],
        )
        judgment = model_judgment(
            row["message"],
            [row.get("evidence_phrase", "")],
            enabled=args.ollama,
        )
        output_rows.append({
            **row,
            "automated_status": result["status"],
            "reasons": "; ".join(result["reasons"]),
            "human_review_required": "YES",
            "model_judgment": json.dumps(judgment, ensure_ascii=True),
        })
    output = DAY_DIR / "output" / "outreach_quality_review.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(output_rows[0]))
        writer.writeheader()
        writer.writerows(output_rows)
    print(
        f"Reviewed {len(rows)} drafts; none were sent. "
        f"Ollama requested: {args.ollama}. Report: {output}"
    )


if __name__ == "__main__":
    main()
