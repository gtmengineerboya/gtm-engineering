"""Demonstrate association planning without guessing HubSpot schema IDs."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gtm_engine.associations import association_plan
from gtm_engine.config import read_secret


class HubSpotAssociationClient:
    def __init__(self, token: str):
        self.session = requests.Session()
        self.headers = {"Authorization": f"Bearer {token}"}
        self.base = "https://api.hubapi.com/crm/v4/objects/contacts"

    def verify_objects(self, contact_id, company_id):
        for object_type, object_id in (
            ("contacts", contact_id),
            ("companies", company_id),
        ):
            response = self.session.get(
                f"https://api.hubapi.com/crm/v3/objects/"
                f"{object_type}/{object_id}",
                headers=self.headers,
                timeout=15,
            )
            response.raise_for_status()

    def associate(self, contact_id, company_id, category, type_id):
        response = self.session.put(
            f"{self.base}/{contact_id}/associations/companies/{company_id}",
            headers=self.headers,
            json=[{
                "associationCategory": category,
                "associationTypeId": type_id,
            }],
            timeout=15,
        )
        response.raise_for_status()

    def read_associations(self, contact_id):
        response = self.session.get(
            f"{self.base}/{contact_id}/associations/companies",
            headers=self.headers,
            timeout=15,
        )
        response.raise_for_status()
        return response.json().get("results", [])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--contact-id", required=True)
    parser.add_argument("--company-id", required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    category = os.getenv("HUBSPOT_CONTACT_COMPANY_ASSOCIATION_CATEGORY")
    raw_type_id = os.getenv("HUBSPOT_CONTACT_COMPANY_ASSOCIATION_TYPE_ID")
    type_id = int(raw_type_id) if raw_type_id else None
    plan = association_plan(
        args.contact_id,
        args.company_id,
        category,
        type_id,
        live=args.apply,
    )
    print(plan)
    if not args.apply:
        print("Dry run only; no HubSpot requests were made.")
        return
    if input("Type APPLY to update HubSpot: ") != "APPLY":
        print("Cancelled.")
        return
    token = None
    for name in ("HUBSPOT_ACCESS_TOKEN", "HUBSPOT_TOKEN"):
        if os.getenv(name):
            try:
                token = read_secret(name)
                break
            except ValueError:
                continue
    if not token:
        raise RuntimeError(
            "Set a non-placeholder HubSpot token in the process environment"
        )
    from gtm_engine.associations import associate_and_verify
    status = associate_and_verify(
        HubSpotAssociationClient(token),
        args.contact_id,
        args.company_id,
        category,
        type_id,
    )
    print(status)


if __name__ == "__main__":
    main()
