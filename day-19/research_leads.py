"""Create structured evidence-based research from synthetic records."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gtm_engine.research import research_with_ollama


DAY_DIR = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ollama", action="store_true",
                        help="Opt in to call local Ollama.")
    args = parser.parse_args()
    records = json.loads(
        (DAY_DIR / "sample_records.json").read_text(encoding="utf-8")
    )
    results = [
        research_with_ollama(record, enabled=args.ollama)
        for record in records
    ]
    output = DAY_DIR / "output" / "research_results.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Processed {len(results)} records. Results: {output}")


if __name__ == "__main__":
    main()
