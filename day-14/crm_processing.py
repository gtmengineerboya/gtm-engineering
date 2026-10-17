"""Day 14: normalize synthetic CRM inputs and plan safe HubSpot upserts."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gtm_engine.crm import (
    HubSpotGateway,
    dry_run_plan,
    execute_live_upserts,
    hubspot_token,
    read_leads,
)


DAY_DIR = Path(__file__).resolve().parent
INPUT_FILE = DAY_DIR / "sample_leads.csv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true",
                        help="Opt in to live HubSpot writes.")
    args = parser.parse_args()
    leads = read_leads(INPUT_FILE)
    plan = dry_run_plan(leads)
    print(f"Validated records: {len(leads)}")
    print(f"Planned contact upserts: {len(plan)} (matched by unique email)")
    for item in plan:
        print(f" - {item['email']} | {item['company_name']} | "
              f"company domain lookup: {item['domain_lookup']}")
    if not args.apply:
        print("DRY RUN only. No HubSpot requests were made.")
        return

    if len(leads) > 10:
        raise ValueError(
            "Live mode is limited to 10 records per invocation; "
            "review and split the input deliberately."
        )
    confirmation = input(
        "Live CRM writes will create/update contacts. Type APPLY to continue: "
    )
    if confirmation != "APPLY":
        print("Cancelled; no HubSpot requests were made.")
        return
    result = execute_live_upserts(leads, HubSpotGateway(hubspot_token()))
    output = DAY_DIR / "output" / "crm_write_results.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(result[0]))
        writer.writeheader()
        writer.writerows(result)
    print(f"Verified live results saved to: {output}")


if __name__ == "__main__":
    main()
