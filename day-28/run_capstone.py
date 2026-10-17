"""Run the safe synthetic GTM revenue-engine demo."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gtm_engine.capstone import run_capstone


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ollama", action="store_true",
                        help="Opt in to local Ollama research.")
    args = parser.parse_args()
    day_dir = Path(__file__).resolve().parent
    result = run_capstone(
        day_dir / "synthetic_leads.csv",
        day_dir / "output",
        use_ollama=args.ollama,
    )
    print(f"Run: {result['run_id']} ({result['status']})")
    print(f"Leads: {result['leads_processed']}")
    print("CRM writes: 0; messages sent: 0; human approval required.")
    print(f"Report: {result['report']}")


if __name__ == "__main__":
    main()
